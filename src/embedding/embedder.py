from sentence_transformers import SentenceTransformer
from src.utils.helpers import load_config

class EmbeddingService:
    def __init__(self):
        config = load_config()
        self.model_name = config.get("model", {}).get("embedding_name", "AITeamVN/Vietnamese_Embedding")
        # Initialize SentenceTransformer. It automatically detects and uses CUDA if available.
        self.model = SentenceTransformer(self.model_name)
    
    def embedding(self, text: str) -> list[float]:
        if not text:
            return []
        return self.model.encode(text).tolist()

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return self.model.encode(texts).tolist()

if __name__ == "__main__":
    service = EmbeddingService()
    print(service.model_name)