"""
Indexa todos los documentos de data/docs.

Uso:  python scripts/ingest.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag import RAGPipeline  # noqa: E402

if __name__ == "__main__":
    rag = RAGPipeline()
    stats = rag.build_index()
    print(f"Índice creado: {stats['documents']} documentos, {stats['chunks']} fragmentos")
    for doc in rag.list_documents():
        print(f"  - {doc['name']}: {doc['chunks']} fragmentos")
