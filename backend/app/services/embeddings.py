from typing import List
from app.core.config import settings
from app.core.logging import logger
import httpx


class EmbeddingService:
    def __init__(self):
        self.provider = settings.EMBEDDING_PROVIDER  # "openai", "ollama", or "huggingface"
        
        if self.provider == "openai":
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.EMBEDDING_MODEL
        elif self.provider == "ollama":
            self.ollama_url = settings.OLLAMA_URL
            self.model = settings.EMBEDDING_MODEL
        elif self.provider == "huggingface":
            self.hf_api_key = settings.HUGGINGFACE_API_KEY
            self.model = settings.EMBEDDING_MODEL
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            if self.provider == "openai":
                return await self._embed_openai(texts)
            elif self.provider == "ollama":
                return await self._embed_ollama(texts)
            elif self.provider == "huggingface":
                return await self._embed_huggingface(texts)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    async def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        """OpenAI embeddings"""
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        embeddings = [item.embedding for item in response.data]
        logger.info(f"Generated {len(embeddings)} embeddings via OpenAI")
        return embeddings
    
    async def _embed_ollama(self, texts: List[str]) -> List[List[float]]:
        """Ollama embeddings (free, local)"""
        embeddings = []
        async with httpx.AsyncClient() as client:
            for text in texts:
                response = await client.post(
                    f"{self.ollama_url}/api/embeddings",
                    json={"model": self.model, "prompt": text},
                    timeout=30.0
                )
                response.raise_for_status()
                embeddings.append(response.json()["embedding"])
        logger.info(f"Generated {len(embeddings)} embeddings via Ollama")
        return embeddings
    
    async def _embed_huggingface(self, texts: List[str]) -> List[List[float]]:
        """Hugging Face embeddings (free API)"""
        embeddings = []
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        async with httpx.AsyncClient() as client:
            for text in texts:
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{self.model}",
                    headers=headers,
                    json={"inputs": text},
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], list):
                        embeddings.append(result[0])
                    else:
                        embeddings.append(result)
                else:
                    embeddings.append(result)
        logger.info(f"Generated {len(embeddings)} embeddings via Hugging Face")
        return embeddings
    
    async def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query"""
        embeddings = await self.embed_texts([query])
        return embeddings[0]


embedding_service = EmbeddingService()
