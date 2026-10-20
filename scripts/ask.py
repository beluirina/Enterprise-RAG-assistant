"""
Hacer una pregunta desde la terminal, sin levantar la API.

Uso:  python scripts/ask.py "¿Cuántos días de vacaciones tengo?"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag import RAGPipeline  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python scripts/ask.py "tu pregunta"')
        sys.exit(1)

    rag = RAGPipeline()
    rag.load_or_build()
    result = rag.ask(" ".join(sys.argv[1:]))

    print(f"\nRespuesta ({result['generator']}):\n{result['answer']}\n")
    for s in result["sources"]:
        page = f", pág. {s['page']}" if s["page"] else ""
        print(f"  [{s['ref']}] {s['document']}{page}  (score {s['score']:.2f})")
