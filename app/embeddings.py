"""
Generación de embeddings.

Hay dos opciones:
- TfidfEmbedder (por defecto): vectores TF-IDF con scikit-learn. No necesita
  descargar modelos ni API keys, así el proyecto corre en cualquier máquina.
- SentenceTransformerEmbedder (opcional): embeddings semánticos con un modelo
  multilingüe. Entiende sinónimos mejor, pero descarga ~450 MB la primera vez.

Las dos clases tienen la misma interfaz: fit(), encode(), save(), load().
"""
import pickle
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbedder:
    name = "tfidf"

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            # n-gramas de caracteres (3 a 5 letras) en vez de palabras completas:
            # así "contraseña" y "contraseñas" se parecen aunque no sean la misma palabra.
            # En la evaluación funcionó mejor que usar palabras completas (ver README).
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True,
        )

    def fit(self, texts):
        self.vectorizer.fit(texts)

    def encode(self, texts):
        # TfidfVectorizer ya devuelve vectores normalizados (norma L2 = 1)
        return self.vectorizer.transform(texts).toarray().astype(np.float32)

    def save(self, folder):
        with open(Path(folder) / "tfidf.pkl", "wb") as f:
            pickle.dump(self.vectorizer, f)

    def load(self, folder):
        with open(Path(folder) / "tfidf.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)


class SentenceTransformerEmbedder:
    name = "sentence-transformers"

    def __init__(self, model_name):
        # Import acá adentro para que no sea obligatorio instalar la librería
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def fit(self, texts):
        pass  # el modelo ya viene entrenado

    def encode(self, texts):
        return np.asarray(self.model.encode(texts, normalize_embeddings=True), dtype=np.float32)

    def save(self, folder):
        pass

    def load(self, folder):
        pass


def get_embedder(backend="tfidf", model_name=None):
    if backend == "tfidf":
        return TfidfEmbedder()
    if backend == "sentence-transformers":
        return SentenceTransformerEmbedder(model_name)
    raise ValueError(f"Backend de embeddings desconocido: {backend}")
