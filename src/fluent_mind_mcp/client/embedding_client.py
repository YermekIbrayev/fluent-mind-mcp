"""Embedding client for generating text embeddings using sentence-transformers.

Provides vector embeddings for semantic search functionality.

WHY: Core component for vector search - converts text to 384-dimensional embeddings
     using all-MiniLM-L6-v2 model for ChromaDB similarity search.
"""

from typing import Optional

from sentence_transformers import SentenceTransformer


class EmbeddingClient:
    """Client for generating text embeddings using sentence-transformers.

    Uses all-MiniLM-L6-v2 model (384 dimensions) optimized for semantic search.

    WHY: Provides fast (<50ms) embedding generation with high semantic accuracy
         for vector database search operations.
    """

    # Constants
    EMBEDDING_DIMENSIONS = 384
    DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        """Initialize embedding client with specified model.

        Args:
            model_name: HuggingFace model identifier

        WHY: all-MiniLM-L6-v2 provides optimal balance of speed, accuracy, and size
             for local MCP server use cases.
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.circuit_breaker: Optional[object] = None  # Placeholder for Phase 4

    def _ensure_model_loaded(self) -> None:
        """Lazy-load the sentence-transformers model on first use.

        WHY: Delays model loading until actually needed, reducing startup time.
        """
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)

    def _validate_text_input(self, text: str) -> None:
        """Validate text input for embedding generation.

        Args:
            text: Text to validate

        Raises:
            ValueError: If text is None, empty, or whitespace-only

        WHY: Centralized validation prevents invalid inputs early.
        """
        if text is None:
            raise ValueError("Cannot generate embedding for None input")
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty string")

    @property
    def _loaded_model(self) -> SentenceTransformer:
        """Get loaded model instance with type safety.

        Returns:
            Loaded SentenceTransformer model

        Raises:
            RuntimeError: If model failed to load

        WHY: Provides type-safe access to model with explicit error handling.
        """
        self._ensure_model_loaded()
        if self.model is None:
            raise RuntimeError(f"Failed to load model: {self.model_name}")
        return self.model

    def generate_embedding(self, text: str) -> list[float]:
        """Generate 384-dimensional embedding for input text.

        Args:
            text: Input text to embed

        Returns:
            List of 384 floats representing L2-normalized embedding

        Raises:
            ValueError: If text is None or empty string

        WHY: Single entry point for converting text to vector representation
             for ChromaDB storage and similarity search.
        """
        self._validate_text_input(text)

        # Generate embedding (automatically normalized by sentence-transformers)
        embedding = self._loaded_model.encode(text, normalize_embeddings=True)

        # Convert numpy array to list for JSON serialization
        return embedding.tolist()

    def batch_embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts efficiently.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings (each is 384-dimensional vector)

        WHY: Batch processing is 2x+ faster than individual calls due to
             GPU/CPU parallelization in sentence-transformers.
        """
        if not texts:
            return []

        # Batch encode with normalization
        embeddings = self._loaded_model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        # Convert numpy array to list of lists
        return embeddings.tolist()
