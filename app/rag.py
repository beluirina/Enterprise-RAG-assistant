"""
Pipeline RAG: une todas las piezas.

    documentos -> chunks -> embeddings -> vector store
    pregunta -> embedding -> top-k chunks -> (umbral) -> LLM -> respuesta + fuentes
"""
import json
import shutil
from pathlib import Path

from app import config
from app.chunker import chunk_pages
from app.embeddings import get_embedder
from app.generator import NO_INFO_MESSAGE, ClaudeGenerator, ExtractiveGenerator
from app.loader import load_document, load_folder
from app.vector_store import VectorStore


def text_for_embedding(chunk):
    # Agrego el nombre del documento al texto: ayuda a que "vacaciones" matchee con politica_vacaciones.md
    title = Path(chunk["source"]).stem.replace("_", " ")
    return f"{title}. {chunk['text']}"


class RAGPipeline:
    def __init__(self, docs_dir=None, index_dir=None, embedder=None, generator=None):
        self.docs_dir = Path(docs_dir or config.DOCS_DIR)
        self.index_dir = Path(index_dir or config.INDEX_DIR)
        self.embedder = embedder or get_embedder(config.EMBEDDING_BACKEND, config.SENTENCE_MODEL)
        self.store = VectorStore()

        if generator is not None:
            self.generator = generator
        elif config.ANTHROPIC_API_KEY:
            self.generator = ClaudeGenerator(config.ANTHROPIC_API_KEY, config.LLM_MODEL)
        else:
            self.generator = ExtractiveGenerator(self.embedder)

    # ---------- Indexación ----------

    def build_index(self):
        """Lee todos los documentos, los divide en chunks, genera embeddings y guarda el índice."""
        pages = load_folder(self.docs_dir)
        chunks = chunk_pages(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP_SENTENCES)
        if not chunks:
            raise ValueError(f"No hay documentos para indexar en {self.docs_dir}")

        texts = [text_for_embedding(c) for c in chunks]
        self.embedder.fit(texts)
        self.store.add(chunks, self.embedder.encode(texts))

        self.store.save(self.index_dir)
        self.embedder.save(self.index_dir)
        with open(self.index_dir / "meta.json", "w") as f:
            json.dump({"embedding_backend": self.embedder.name}, f)

        return {"documents": len({c["source"] for c in chunks}), "chunks": len(chunks)}

    def load_index(self):
        """Carga el índice guardado. Devuelve False si no existe o se creó con otro backend."""
        meta = self.index_dir / "meta.json"
        if not VectorStore.exists(self.index_dir) or not meta.exists():
            return False
        if json.loads(meta.read_text())["embedding_backend"] != self.embedder.name:
            return False
        self.store.load(self.index_dir)
        self.embedder.load(self.index_dir)
        return True

    def load_or_build(self):
        if not self.load_index():
            self.build_index()

    def add_document(self, file_path):
        """Copia un archivo nuevo a la carpeta de documentos y reconstruye el índice."""
        load_document(file_path)  # valida que se pueda leer antes de copiarlo
        destination = self.docs_dir / Path(file_path).name
        if Path(file_path).resolve() != destination.resolve():
            shutil.copy(file_path, destination)
        return self.build_index()

    def list_documents(self):
        counts = {}
        for c in self.store.chunks:
            counts[c["source"]] = counts.get(c["source"], 0) + 1
        return [{"name": name, "chunks": n} for name, n in sorted(counts.items())]

    # ---------- Consulta ----------

    def retrieve(self, question, top_k=None):
        top_k = top_k or config.TOP_K
        query_vector = self.embedder.encode([question])[0]
        results = self.store.search(query_vector, top_k)
        return [{**chunk, "score": round(score, 4)} for chunk, score in results]

    def ask(self, question, top_k=None):
        retrieved = self.retrieve(question, top_k)

        # Solo uso los fragmentos que superan el umbral mínimo de similitud
        sources = [r for r in retrieved if r["score"] >= config.MIN_SCORE]
        if not sources:
            return self._no_info()

        answer = self.generator.generate(question, sources)
        if answer is None:
            return self._no_info()

        return {
            "answer": answer,
            "has_answer": True,
            "sources": [
                {
                    "ref": i,
                    "document": s["source"],
                    "page": s["page"],
                    "chunk_id": s["id"],
                    "score": s["score"],
                    "text": s["text"],
                }
                for i, s in enumerate(sources, start=1)
            ],
            "generator": self.generator.name,
        }

    def _no_info(self):
        return {
            "answer": NO_INFO_MESSAGE,
            "has_answer": False,
            "sources": [],
            "generator": self.generator.name,
        }
