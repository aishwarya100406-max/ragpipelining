# API Testing Guide

## Quick Test Commands

### 1. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "qdrant": true,
    "openai": true
  }
}
```

### 2. Upload Document

```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@sample-documents/sample.txt"
```

Expected response:
```json
{
  "doc_id": "uuid-here",
  "filename": "sample.txt",
  "doc_type": "txt",
  "size": 1234,
  "chunks_count": 5,
  "uploaded_at": "2024-01-01T00:00:00",
  "metadata": {}
}
```

### 3. Query Documents

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key features of the RAG pipeline?",
    "top_k": 5,
    "use_reranking": true
  }'
```

Expected response:
```json
{
  "answer": "The key features include...",
  "sources": [
    {
      "content": "chunk text...",
      "score": 0.95,
      "doc_id": "uuid",
      "chunk_id": "uuid",
      "metadata": {}
    }
  ],
  "query_id": "uuid",
  "processing_time": 1.23,
  "retrieval_method": "hybrid"
}
```

### 4. Get Metrics

```bash
curl http://localhost:8000/api/v1/metrics
```

### 5. Delete Document

```bash
curl -X DELETE http://localhost:8000/api/v1/documents/{doc_id}
```

## Python Testing Script

Create `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print("Health:", response.json())

def test_upload():
    with open("sample-documents/sample.txt", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        print("Upload:", response.json())
        return response.json()["doc_id"]

def test_query():
    data = {
        "query": "What is the RAG pipeline?",
        "top_k": 3,
        "use_reranking": True
    }
    response = requests.post(f"{BASE_URL}/query", json=data)
    result = response.json()
    print("Query:", result["answer"])
    print("Sources:", len(result["sources"]))

def test_metrics():
    response = requests.get(f"{BASE_URL}/metrics")
    print("Metrics:", response.json())

if __name__ == "__main__":
    test_health()
    doc_id = test_upload()
    test_query()
    test_metrics()
```

Run with:
```bash
python test_api.py
```

## JavaScript/Node.js Testing

Create `test_api.js`:

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const BASE_URL = 'http://localhost:8000/api/v1';

async function testHealth() {
  const response = await axios.get(`${BASE_URL}/health`);
  console.log('Health:', response.data);
}

async function testUpload() {
  const form = new FormData();
  form.append('file', fs.createReadStream('sample-documents/sample.txt'));
  
  const response = await axios.post(`${BASE_URL}/upload`, form, {
    headers: form.getHeaders()
  });
  console.log('Upload:', response.data);
  return response.data.doc_id;
}

async function testQuery() {
  const response = await axios.post(`${BASE_URL}/query`, {
    query: 'What is the RAG pipeline?',
    top_k: 3,
    use_reranking: true
  });
  console.log('Answer:', response.data.answer);
  console.log('Sources:', response.data.sources.length);
}

async function runTests() {
  await testHealth();
  await testUpload();
  await testQuery();
}

runTests().catch(console.error);
```

## Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "RAG Pipeline API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/health"
      }
    },
    {
      "name": "Upload Document",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/upload",
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "file",
              "type": "file",
              "src": "sample.txt"
            }
          ]
        }
      }
    },
    {
      "name": "Query",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/query",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"What is RAG?\",\n  \"top_k\": 5\n}"
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api/v1"
    }
  ]
}
```

## Load Testing

Using Apache Bench:

```bash
# Test query endpoint
ab -n 100 -c 10 -p query.json -T application/json \
  http://localhost:8000/api/v1/query
```

Using `wrk`:

```bash
wrk -t4 -c100 -d30s http://localhost:8000/api/v1/health
```

## Expected Performance

- Health check: < 50ms
- Document upload (1MB): < 5s
- Query (with 5 results): < 2s
- Metrics: < 100ms

## Common Issues

1. **Connection Refused**: Backend not running
2. **500 Error**: Check backend logs
3. **Slow Queries**: Check Qdrant performance
4. **Upload Fails**: Check file size and format
