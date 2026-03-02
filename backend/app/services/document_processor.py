from typing import List, Dict, Any, Tuple
import uuid
from datetime import datetime
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from docx import Document
import io
from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import DocumentType


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    async def process_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str
    ) -> Tuple[List[str], List[Dict[str, Any]], DocumentType]:
        """Process uploaded file and return chunks with metadata"""
        doc_id = str(uuid.uuid4())
        doc_type = self._detect_document_type(filename, content_type)
        
        # Extract text based on file type
        text = await self._extract_text(file_content, doc_type)
        
        # Split into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create metadata for each chunk
        metadatas = [
            {
                "doc_id": doc_id,
                "chunk_id": str(uuid.uuid4()),
                "chunk_index": i,
                "filename": filename,
                "doc_type": doc_type.value,
                "total_chunks": len(chunks),
                "uploaded_at": datetime.utcnow().isoformat()
            }
            for i in range(len(chunks))
        ]
        
        logger.info(f"Processed {filename}: {len(chunks)} chunks")
        return chunks, metadatas, doc_type
    
    def _detect_document_type(self, filename: str, content_type: str) -> DocumentType:
        """Detect document type from filename and content type"""
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.pdf') or 'pdf' in content_type:
            return DocumentType.PDF
        elif filename_lower.endswith('.docx') or 'word' in content_type:
            return DocumentType.DOCX
        elif filename_lower.endswith('.md'):
            return DocumentType.MARKDOWN
        elif any(filename_lower.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.go']):
            return DocumentType.CODE
        else:
            return DocumentType.TXT
    
    async def _extract_text(self, content: bytes, doc_type: DocumentType) -> str:
        """Extract text from different document types"""
        try:
            if doc_type == DocumentType.PDF:
                return self._extract_pdf(content)
            elif doc_type == DocumentType.DOCX:
                return self._extract_docx(content)
            else:
                return content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            raise
    
    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from PDF"""
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        return text
    
    def _extract_docx(self, content: bytes) -> str:
        """Extract text from DOCX"""
        docx_file = io.BytesIO(content)
        doc = Document(docx_file)
        text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text


document_processor = DocumentProcessor()
