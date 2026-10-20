"""Configuración del proyecto. Todo se puede cambiar con variables de entorno o un archivo .env"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Carpetas
DOCS_DIR = Path(os.getenv("DOCS_DIR", BASE_DIR / "data" / "docs"))
INDEX_DIR = Path(os.getenv("INDEX_DIR", BASE_DIR / "storage"))

# Chunking: tamaño aproximado de cada fragmento (en palabras)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "120"))
CHUNK_OVERLAP_SENTENCES = int(os.getenv("CHUNK_OVERLAP_SENTENCES", "1"))

# Recuperación
TOP_K = int(os.getenv("TOP_K", "4"))
# Si el fragmento más parecido tiene un score menor a esto, el sistema responde "no tengo información"
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.20"))

# Embeddings: "tfidf" (por defecto, no necesita descargas) o "sentence-transformers"
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "tfidf")
SENTENCE_MODEL = os.getenv("SENTENCE_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

# LLM: si hay API key se usa Claude, si no, un modo extractivo que funciona sin internet
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
