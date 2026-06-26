from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.embedding.embedder import EmbeddingService

app = FastAPI(title="Vietnamese Embedding Service API")

class EmbeddingRequest(BaseModel):
    texts: list[str]

# Initialize embedder service at startup
try:
    embedder = EmbeddingService()
except Exception as e:
    print(f"CRITICAL: Failed to initialize EmbeddingService: {e}")
    embedder = None

@app.get("/health", tags=["Health Check"])
def health_check():
    if embedder is None:
        return {"status": "unhealthy", "error": "Embedding service model failed to load"}
    return {"status": "ok"}

@app.post("/embedding", tags=["Embedding"])
async def embedding(request: EmbeddingRequest):
    if embedder is None:
        raise HTTPException(status_code=500, detail="Embedding service is not available (model failed to load)")
    texts = request.texts
    if not texts:
        raise HTTPException(status_code=400, detail="The input list of texts cannot be empty")
    try:
        embeddings = embedder.get_embeddings(texts)
        return {"embedding": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {str(e)}")