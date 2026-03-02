import { useState, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Send, Loader2, FileText, Filter } from 'lucide-react';
import { api, QueryResponse, DocumentMetadata } from '../services/api';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  sources?: QueryResponse['sources'];
  processingTime?: number;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [uploadedDocs, setUploadedDocs] = useState<DocumentMetadata[]>([]);
  const [selectedDocId, setSelectedDocId] = useState<string>('');

  useEffect(() => {
    const saved = localStorage.getItem('uploadedDocs');
    if (saved) setUploadedDocs(JSON.parse(saved));
  }, []);

  const queryMutation = useMutation({
    mutationFn: api.query,
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          id: data.query_id,
          type: 'assistant',
          content: data.answer,
          sources: data.sources,
          processingTime: data.processing_time,
        },
      ]);
    },
    onError: (error) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          type: 'assistant',
          content: `Error: ${error.message || 'Failed to get response. Please try again.'}`,
        },
      ]);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || queryMutation.isPending) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    
    // Build filters if a document is selected
    const filters = selectedDocId ? { doc_id: selectedDocId } : undefined;
    
    queryMutation.mutate({
      query: input,
      top_k: 5,
      use_reranking: true,
      filters,
    });
    setInput('');
  };

  return (
    <div className="h-[calc(100vh-12rem)] flex flex-col glass-effect rounded-2xl">
      {/* Document Filter */}
      {uploadedDocs.length > 0 && (
        <div className="p-4 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <Filter className="w-5 h-5 text-slate-600" />
            <select
              value={selectedDocId}
              onChange={(e) => setSelectedDocId(e.target.value)}
              className="flex-1 px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
            >
              <option value="">All Documents</option>
              {uploadedDocs.map((doc) => (
                <option key={doc.doc_id} value={doc.doc_id}>
                  {doc.filename}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">
                Start a Conversation
              </h3>
              <p className="text-slate-600">
                Ask questions about your uploaded documents
              </p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl rounded-2xl px-6 py-4 ${
                  message.type === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-white border border-slate-200'
                }`}
              >
                <div className="prose prose-sm max-w-none">
                  {message.type === 'user' ? (
                    <p className="text-white m-0">{message.content}</p>
                  ) : (
                    <>
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-slate-200">
                          <p className="text-xs font-semibold text-slate-600 mb-2">
                            Sources ({message.sources.length})
                          </p>
                          <div className="space-y-2">
                            {message.sources.slice(0, 3).map((source, idx) => (
                              <div
                                key={source.chunk_id}
                                className="text-xs bg-slate-50 p-2 rounded border border-slate-200"
                              >
                                <div className="flex items-center gap-2 mb-1">
                                  <span className="font-semibold text-primary-600">
                                    [{idx + 1}]
                                  </span>
                                  <span className="text-slate-500">
                                    Score: {source.score.toFixed(3)}
                                  </span>
                                </div>
                                <p className="text-slate-700 line-clamp-2 m-0">
                                  {source.content}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      {message.processingTime && (
                        <p className="text-xs text-slate-500 mt-2 m-0">
                          Processed in {message.processingTime.toFixed(2)}s
                        </p>
                      )}
                    </>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
        {queryMutation.isPending && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 rounded-2xl px-6 py-4">
              <Loader2 className="w-5 h-5 animate-spin text-primary-600" />
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-6 border-t border-slate-200">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="flex-1 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={queryMutation.isPending}
          />
          <button
            type="submit"
            disabled={!input.trim() || queryMutation.isPending}
            className="px-6 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
