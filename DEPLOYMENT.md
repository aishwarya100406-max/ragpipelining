# Deployment Guide

## Production Deployment Checklist

### Pre-Deployment

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Use strong secrets and API keys
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Set up logging aggregation
- [ ] Configure rate limiting
- [ ] Review security settings

### Environment Variables (Production)

```bash
# API Keys (use secrets manager)
OPENAI_API_KEY=sk-prod-key
COHERE_API_KEY=prod-key

# Services (use managed services)
QDRANT_URL=https://your-qdrant-cluster.com
REDIS_URL=redis://your-redis-cluster:6379
DATABASE_URL=postgresql+asyncpg://user:pass@db-host:5432/rag_db

# App Config
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Deployment Options

### Option 1: Docker Compose (Simple)

1. Build images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Start services:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Check status:
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Option 2: Kubernetes (Scalable)

1. Create namespace:
```bash
kubectl create namespace rag-pipeline
```

2. Apply configurations:
```bash
kubectl apply -f k8s/
```

3. Check deployments:
```bash
kubectl get pods -n rag-pipeline
```

### Option 3: Cloud Platforms

#### AWS Deployment

**Backend (ECS/Fargate)**:
```bash
# Build and push image
docker build -t rag-backend ./backend
docker tag rag-backend:latest {account}.dkr.ecr.{region}.amazonaws.com/rag-backend:latest
docker push {account}.dkr.ecr.{region}.amazonaws.com/rag-backend:latest

# Deploy to ECS
aws ecs update-service --cluster rag-cluster --service rag-backend --force-new-deployment
```

**Frontend (S3 + CloudFront)**:
```bash
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket-name/
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

**Services**:
- Qdrant: Use Qdrant Cloud or self-hosted on EC2
- Redis: Use ElastiCache
- PostgreSQL: Use RDS

#### Google Cloud Platform

**Backend (Cloud Run)**:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/rag-backend
gcloud run deploy rag-backend --image gcr.io/PROJECT_ID/rag-backend --platform managed
```

**Frontend (Firebase Hosting)**:
```bash
cd frontend
npm run build
firebase deploy
```

#### Azure

**Backend (Container Instances)**:
```bash
az container create --resource-group rag-rg --name rag-backend \
  --image your-registry.azurecr.io/rag-backend:latest \
  --dns-name-label rag-backend --ports 8000
```

**Frontend (Static Web Apps)**:
```bash
cd frontend
npm run build
az staticwebapp create --name rag-frontend --resource-group rag-rg
```

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    # Frontend
    location / {
        root /var/www/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Process Management

### Using systemd

Create `/etc/systemd/system/rag-backend.service`:

```ini
[Unit]
Description=RAG Pipeline Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/rag-pipeline/backend
Environment="PATH=/opt/rag-pipeline/backend/venv/bin"
ExecStart=/opt/rag-pipeline/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rag-backend
sudo systemctl start rag-backend
sudo systemctl status rag-backend
```

### Using PM2

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Monitoring Setup

### Prometheus + Grafana

1. Add Prometheus endpoint to backend
2. Configure Prometheus scraping
3. Import Grafana dashboards
4. Set up alerts

### Application Monitoring

```python
# Add to backend
from prometheus_client import Counter, Histogram

query_counter = Counter('rag_queries_total', 'Total queries')
query_duration = Histogram('rag_query_duration_seconds', 'Query duration')
```

### Log Aggregation

**Using ELK Stack**:
- Elasticsearch for storage
- Logstash for processing
- Kibana for visualization

**Using Cloud Services**:
- AWS CloudWatch
- Google Cloud Logging
- Azure Monitor

## Backup Strategy

### Database Backups

```bash
# PostgreSQL
pg_dump -h localhost -U rag_user rag_db > backup.sql

# Automated with cron
0 2 * * * pg_dump -h localhost -U rag_user rag_db > /backups/rag_$(date +\%Y\%m\%d).sql
```

### Vector Store Backups

```bash
# Qdrant snapshot
curl -X POST http://localhost:6333/collections/documents/snapshots
```

## Security Hardening

1. **API Security**:
   - Implement rate limiting
   - Add API key authentication
   - Use HTTPS only
   - Validate all inputs

2. **Network Security**:
   - Configure firewall rules
   - Use VPC/private networks
   - Implement DDoS protection
   - Enable WAF

3. **Data Security**:
   - Encrypt data at rest
   - Encrypt data in transit
   - Implement access controls
   - Regular security audits

## Performance Optimization

1. **Caching**:
   - Redis for query results
   - CDN for static assets
   - Browser caching headers

2. **Database**:
   - Connection pooling
   - Query optimization
   - Index optimization

3. **Application**:
   - Async processing
   - Background tasks
   - Load balancing

## Scaling Strategy

### Horizontal Scaling

- Multiple backend instances behind load balancer
- Qdrant cluster for vector search
- Redis cluster for caching
- PostgreSQL read replicas

### Vertical Scaling

- Increase instance sizes
- Add more CPU/RAM
- Use faster storage

## Rollback Plan

1. Keep previous version tagged
2. Database migration rollback scripts
3. Quick rollback procedure documented
4. Health checks before full deployment

## Post-Deployment

- [ ] Verify all services are running
- [ ] Test critical user flows
- [ ] Check monitoring dashboards
- [ ] Review logs for errors
- [ ] Test backup restoration
- [ ] Update documentation
- [ ] Notify team of deployment

## Troubleshooting

### High Memory Usage
- Check for memory leaks
- Optimize chunk sizes
- Increase instance size

### Slow Queries
- Check Qdrant performance
- Optimize retrieval parameters
- Add caching

### Connection Errors
- Check service health
- Verify network connectivity
- Review firewall rules

## Support

For production issues:
1. Check monitoring dashboards
2. Review application logs
3. Check service health endpoints
4. Contact support team
