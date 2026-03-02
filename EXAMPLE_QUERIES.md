# Example Queries

## Sample Questions to Try

Once you've uploaded the sample document (or your own documents), try these queries:

### General Questions

1. "What is the Advanced RAG Pipeline?"
2. "What are the key features of this system?"
3. "How does the system work?"
4. "What technologies are used in this project?"

### Technical Questions

5. "Explain the architecture of the system"
6. "What embedding model is used?"
7. "How does the chunking process work?"
8. "What is hybrid search?"
9. "How does reranking improve results?"

### Use Case Questions

10. "What are the use cases for this system?"
11. "How can this be used for enterprise knowledge management?"
12. "What industries can benefit from this?"
13. "How does it help with customer support?"

### Performance Questions

14. "What is the expected query response time?"
15. "How many concurrent users can it handle?"
16. "What are the performance metrics?"

### Security Questions

17. "What security features are included?"
18. "How is data protected?"
19. "What authentication methods are supported?"

### Configuration Questions

20. "How do I configure the chunk size?"
21. "What parameters can be adjusted?"
22. "How do I change the embedding model?"

### Troubleshooting Questions

23. "What should I do if queries are slow?"
24. "How do I fix upload failures?"
25. "What are common issues and solutions?"

### Future Features

26. "What features are planned for the future?"
27. "Will it support multiple languages?"
28. "Can it handle images and tables?"

## Advanced Query Patterns

### Comparative Questions
- "Compare dense and sparse retrieval methods"
- "What's the difference between chunking strategies?"

### How-To Questions
- "How do I deploy this to production?"
- "How do I add a new document format?"
- "How do I customize the UI?"

### Best Practices
- "What are best practices for document upload?"
- "How should I structure my queries?"
- "What's the optimal chunk size?"

### Analytical Questions
- "Analyze the system architecture"
- "Explain the data flow in the pipeline"
- "What are the bottlenecks?"

## Testing Different Parameters

### Top-K Variations
Try the same query with different `top_k` values:
- top_k: 3 (focused results)
- top_k: 5 (balanced)
- top_k: 10 (comprehensive)

### With/Without Reranking
Compare results with:
- use_reranking: true
- use_reranking: false

### Filtered Queries
Use metadata filters:
```json
{
  "query": "What are the features?",
  "filters": {
    "doc_type": "pdf"
  }
}
```

## Complex Queries

### Multi-Part Questions
"What are the key features of the RAG pipeline, and how do they compare to traditional search systems?"

### Specific Detail Requests
"List all the technologies used in the backend with their version numbers"

### Contextual Questions
"Based on the architecture, what would be the best way to scale this system?"

### Synthesis Questions
"Summarize the entire system in three paragraphs"

## Expected Response Quality

### Good Responses Should Include:
- Direct answer to the question
- Relevant context from documents
- Source citations [1], [2], etc.
- Accurate information
- Clear, well-structured text

### If Response Quality is Poor:
1. Try rephrasing the question
2. Be more specific
3. Check if relevant documents are uploaded
4. Adjust top_k parameter
5. Enable reranking

## Query Tips

### For Best Results:
1. **Be Specific**: "What embedding model is used?" vs "Tell me about embeddings"
2. **Use Keywords**: Include important terms from your documents
3. **Ask One Thing**: Break complex questions into parts
4. **Provide Context**: Reference specific topics when needed
5. **Check Sources**: Review the cited chunks for accuracy

### Avoid:
1. Extremely vague questions
2. Questions about information not in documents
3. Multiple unrelated questions in one query
4. Very long, rambling questions

## Evaluation Criteria

Rate responses on:
- **Relevance**: Does it answer the question?
- **Accuracy**: Is the information correct?
- **Completeness**: Are all aspects covered?
- **Sources**: Are citations provided?
- **Clarity**: Is it easy to understand?

## Sample API Calls

### Basic Query
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key features?",
    "top_k": 5,
    "use_reranking": true
  }'
```

### With Filters
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the architecture",
    "top_k": 3,
    "use_reranking": true,
    "filters": {
      "doc_type": "txt"
    }
  }'
```

### Minimal Query
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is RAG?"
  }'
```

## Benchmarking Queries

Use these to test performance:

1. **Simple**: "What is this?"
2. **Medium**: "Explain the key features and their benefits"
3. **Complex**: "Compare the different retrieval methods and explain when to use each"
4. **Very Complex**: "Analyze the entire system architecture, identify potential bottlenecks, and suggest optimizations"

## Fun Queries to Try

1. "Tell me a joke about RAG systems" (tests creativity)
2. "What's the most important feature?" (tests ranking)
3. "Explain this to a 5-year-old" (tests simplification)
4. "What's missing from this system?" (tests analysis)

## Monitoring Query Performance

Track these metrics:
- Response time
- Number of sources retrieved
- Relevance scores
- User satisfaction
- Cache hit rate

## Continuous Improvement

1. Collect user feedback on responses
2. Identify common query patterns
3. Optimize retrieval parameters
4. Improve document chunking
5. Fine-tune prompts
6. Add domain-specific knowledge

Happy querying! 🚀
