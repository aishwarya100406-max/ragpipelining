import axios from 'axios';

const API_BASE_URL = '/api/v1';

export interface QueryRequest {
  query: string;
  top_k?: number;
  use_reranking?: boolean;
  use_hyde?: boolean;
  filters?: Record<string, any>;
}

export interface RetrievedChunk {
  content: string;
  score: number;
  doc_id: string;
  chunk_id: string;
  metadata: Record<string, any>;
}

export interface QueryResponse {
  answer: string;
  sources: RetrievedChunk[];
  query_id: string;
  processing_time: number;
  retrieval_method: string;
}

export interface DocumentMetadata {
  doc_id: string;
  filename: string;
  doc_type: string;
  size: number;
  chunks_count: number;
  uploaded_at: string;
  metadata: Record<string, any>;
}

export interface HealthResponse {
  status: string;
  version: string;
  services: Record<string, boolean>;
}

export interface MetricsResponse {
  total_documents: number;
  total_chunks: number;
  total_queries: number;
  avg_response_time: number;
  cache_hit_rate: number;
}

export const api = {
  uploadDocument: async (file: File): Promise<DocumentMetadata> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  query: async (request: QueryRequest): Promise<QueryResponse> => {
    const response = await axios.post(`${API_BASE_URL}/query`, request);
    return response.data;
  },

  deleteDocument: async (docId: string): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/documents/${docId}`);
  },

  getHealth: async (): Promise<HealthResponse> => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },

  getMetrics: async (): Promise<MetricsResponse> => {
    const response = await axios.get(`${API_BASE_URL}/metrics`);
    return response.data;
  },

  listDocuments: async (): Promise<DocumentMetadata[]> => {
    const response = await axios.get(`${API_BASE_URL}/documents`);
    return response.data;
  }
};
