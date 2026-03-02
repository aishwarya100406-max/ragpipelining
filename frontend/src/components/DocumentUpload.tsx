import { useState, useCallback, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Upload, FileText, CheckCircle, XCircle, Loader2, Trash2 } from 'lucide-react';
import { api, DocumentMetadata } from '../services/api';

export default function DocumentUpload() {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedDocs, setUploadedDocs] = useState<DocumentMetadata[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem('uploadedDocs');
    if (saved) setUploadedDocs(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem('uploadedDocs', JSON.stringify(uploadedDocs));
  }, [uploadedDocs]);

  const uploadMutation = useMutation({
    mutationFn: api.uploadDocument,
    onSuccess: (data) => {
      setUploadedDocs((prev) => [data, ...prev]);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: api.deleteDocument,
    onSuccess: (_, docId) => {
      setUploadedDocs((prev) => prev.filter(doc => doc.doc_id !== docId));
    },
  });

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      uploadMutation.mutate(e.dataTransfer.files[0]);
    }
  }, [uploadMutation]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      uploadMutation.mutate(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div className="glass-effect rounded-2xl p-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">
          Upload Documents
        </h2>

        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
            dragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-slate-300 hover:border-primary-400'
          }`}
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            onChange={handleFileInput}
            accept=".pdf,.docx,.txt,.md,.py,.js,.ts"
            disabled={uploadMutation.isPending}
          />

          <div className="space-y-4">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
              {uploadMutation.isPending ? (
                <Loader2 className="w-8 h-8 text-primary-600 animate-spin" />
              ) : (
                <Upload className="w-8 h-8 text-primary-600" />
              )}
            </div>

            <div>
              <p className="text-lg font-semibold text-slate-800 mb-2">
                {uploadMutation.isPending
                  ? 'Processing document...'
                  : 'Drop your files here'}
              </p>
              <p className="text-sm text-slate-600">
                or{' '}
                <label
                  htmlFor="file-upload"
                  className="text-primary-600 hover:text-primary-700 cursor-pointer font-medium"
                >
                  browse
                </label>
              </p>
            </div>

            <p className="text-xs text-slate-500">
              Supports: PDF, DOCX, TXT, Markdown, Code files
            </p>
          </div>

          {uploadMutation.isError && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
              <XCircle className="w-5 h-5" />
              <span className="text-sm">Upload failed. Please try again.</span>
            </div>
          )}
        </div>
      </div>

      {/* Uploaded Documents */}
      {uploadedDocs.length > 0 && (
        <div className="glass-effect rounded-2xl p-8">
          <h3 className="text-xl font-bold text-slate-800 mb-4">
            Uploaded Documents ({uploadedDocs.length})
          </h3>

          <div className="space-y-3">
            {uploadedDocs.map((doc) => (
              <div
                key={doc.doc_id}
                className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-xl hover:shadow-md transition-shadow"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <FileText className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="font-medium text-slate-800">{doc.filename}</p>
                    <p className="text-sm text-slate-600">
                      {doc.chunks_count} chunks • {(doc.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <button
                    onClick={() => deleteMutation.mutate(doc.doc_id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Delete document"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
