"""
Vector store simple hecho con NumPy.

Para pocos miles de fragmentos no hace falta una base vectorial: guardo la
matriz de embeddings en un .npy y los textos en un .json. La búsqueda es
similitud coseno (producto punto, porque los vectores están normalizados).
"""
import json
from pathlib import Path

import numpy as np


class VectorStore:
    def __init__(self):
        self.chunks = []
        self.embeddings = None

    def __len__(self):
        return len(self.chunks)

    def add(self, chunks, embeddings):
        self.chunks = list(chunks)
        self.embeddings = np.asarray(embeddings, dtype=np.float32)

    def search(self, query_vector, top_k=4):
        """Devuelve [(chunk, score), ...] ordenado de mayor a menor score."""
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        scores = self.embeddings @ query_vector
        best = np.argsort(scores)[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in best]

    def save(self, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        np.save(folder / "embeddings.npy", self.embeddings)
        with open(folder / "chunks.json", "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)

    def load(self, folder):
        folder = Path(folder)
        self.embeddings = np.load(folder / "embeddings.npy")
        with open(folder / "chunks.json", encoding="utf-8") as f:
            self.chunks = json.load(f)

    @staticmethod
    def exists(folder):
        folder = Path(folder)
        return (folder / "embeddings.npy").exists() and (folder / "chunks.json").exists()
