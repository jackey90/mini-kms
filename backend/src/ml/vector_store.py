import json
import os
import numpy as np
import faiss
from src.config import settings


class VectorStore:
    """FAISS-based vector store with per-intent-space indexes, persisted to disk."""

    EMBEDDING_DIM = 1536  # text-embedding-3-small

    def __init__(self):
        self._indexes: dict[int, faiss.IndexFlatL2] = {}
        self._meta: dict[int, list[dict]] = {}  # intent_space_id -> chunk metadata

    def _index_path(self, intent_space_id: int) -> str:
        return os.path.join(settings.data_dir, "faiss", f"intent_{intent_space_id}.index")

    def _meta_path(self, intent_space_id: int) -> str:
        return os.path.join(settings.data_dir, "faiss", f"intent_{intent_space_id}_meta.json")

    def _load(self, intent_space_id: int) -> None:
        idx_path = self._index_path(intent_space_id)
        meta_path = self._meta_path(intent_space_id)

        if os.path.exists(idx_path) and os.path.exists(meta_path):
            self._indexes[intent_space_id] = faiss.read_index(idx_path)
            with open(meta_path, "r") as f:
                self._meta[intent_space_id] = json.load(f)["chunks"]
        else:
            self._indexes[intent_space_id] = faiss.IndexFlatL2(self.EMBEDDING_DIM)
            self._meta[intent_space_id] = []

    def _ensure_loaded(self, intent_space_id: int) -> None:
        if intent_space_id not in self._indexes:
            self._load(intent_space_id)

    def _persist(self, intent_space_id: int) -> None:
        faiss.write_index(self._indexes[intent_space_id], self._index_path(intent_space_id))
        with open(self._meta_path(intent_space_id), "w") as f:
            json.dump({"chunks": self._meta[intent_space_id]}, f)

    def add_document(
        self,
        intent_space_id: int,
        chunks: list[str],
        embeddings: list[list[float]],
        document_id: int,
        filename: str,
    ) -> int:
        """Add document chunks to the index. Returns number of chunks added."""
        self._ensure_loaded(intent_space_id)
        index = self._indexes[intent_space_id]
        meta = self._meta[intent_space_id]

        vectors = np.array(embeddings, dtype=np.float32)
        start_id = index.ntotal
        index.add(vectors)

        for i, chunk_text in enumerate(chunks):
            meta.append({
                "faiss_id": start_id + i,
                "document_id": document_id,
                "filename": filename,
                "chunk_text": chunk_text,
            })

        self._persist(intent_space_id)
        return len(chunks)

    def remove_document(self, intent_space_id: int, document_id: int) -> None:
        """Remove all chunks for a document. Rebuilds index (safe for MVP scale)."""
        self._ensure_loaded(intent_space_id)
        meta = self._meta[intent_space_id]

        remaining = [m for m in meta if m["document_id"] != document_id]
        if len(remaining) == len(meta):
            return  # nothing to remove

        # Rebuild index from remaining chunks
        new_index = faiss.IndexFlatL2(self.EMBEDDING_DIM)
        new_meta = []

        if remaining:
            # Re-embed and re-add is expensive; instead store embeddings in meta
            # For MVP: store original embeddings in meta to allow cheap rebuilds
            embeddings = [m.get("embedding", [0.0] * self.EMBEDDING_DIM) for m in remaining]
            vectors = np.array(embeddings, dtype=np.float32)
            new_index.add(vectors)
            for i, m in enumerate(remaining):
                new_meta.append({**m, "faiss_id": i})

        self._indexes[intent_space_id] = new_index
        self._meta[intent_space_id] = new_meta
        self._persist(intent_space_id)

    def search(
        self,
        intent_space_id: int | None,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[dict]:
        """Search for top-k similar chunks.

        If intent_space_id is None, search across all loaded indexes.
        Returns list of: {chunk_text, document_id, filename, distance, similarity}
        """
        query_vec = np.array([query_embedding], dtype=np.float32)
        results: list[dict] = []

        space_ids = list(self._indexes.keys()) if intent_space_id is None else [intent_space_id]

        for sid in space_ids:
            self._ensure_loaded(sid)
            index = self._indexes[sid]
            meta = self._meta[sid]

            if index.ntotal == 0:
                continue

            actual_k = min(k, index.ntotal)
            distances, indices = index.search(query_vec, actual_k)

            for dist, idx in zip(distances[0], indices[0]):
                if idx < 0 or idx >= len(meta):
                    continue
                chunk_meta = meta[idx]
                similarity = 1.0 / (1.0 + float(dist))
                results.append({
                    "chunk_text": chunk_meta["chunk_text"],
                    "document_id": chunk_meta["document_id"],
                    "filename": chunk_meta["filename"],
                    "distance": float(dist),
                    "similarity": similarity,
                })

        # Sort by distance (lower = better) and return top-k
        results.sort(key=lambda x: x["distance"])
        return results[:k]

    def add_document_with_embeddings_stored(
        self,
        intent_space_id: int,
        chunks: list[str],
        embeddings: list[list[float]],
        document_id: int,
        filename: str,
    ) -> int:
        """Add document chunks and store embeddings in meta for later rebuilds."""
        self._ensure_loaded(intent_space_id)
        index = self._indexes[intent_space_id]
        meta = self._meta[intent_space_id]

        vectors = np.array(embeddings, dtype=np.float32)
        start_id = index.ntotal
        index.add(vectors)

        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            meta.append({
                "faiss_id": start_id + i,
                "document_id": document_id,
                "filename": filename,
                "chunk_text": chunk_text,
                "embedding": embedding,
            })

        self._persist(intent_space_id)
        return len(chunks)


# Module-level singleton
vector_store = VectorStore()
