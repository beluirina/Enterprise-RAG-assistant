"""API REST del asistente. Correr con:  uvicorn app.main:app --reload"""
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.loader import SUPPORTED_EXTENSIONS
from app.rag import RAGPipeline

STATIC_DIR = Path(__file__).parent / "static"
MAX_UPLOAD_MB = 10

rag = RAGPipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    rag.load_or_build()  # al arrancar carga el índice (o lo crea si no existe)
    yield


app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Responde preguntas sobre la documentación interna de NovaTech, citando las fuentes.",
    version="1.0.0",
    lifespan=lifespan,
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, examples=["¿Cuántos días de vacaciones tengo?"])
    top_k: int = Field(4, ge=1, le=10)


class Source(BaseModel):
    ref: int
    document: str
    page: int | None
    chunk_id: str
    score: float
    text: str


class AskResponse(BaseModel):
    answer: str
    has_answer: bool
    sources: list[Source]
    generator: str


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "chunks_indexed": len(rag.store), "generator": rag.generator.name}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return rag.ask(request.question.strip(), request.top_k)


@app.get("/documents")
def list_documents():
    return rag.list_documents()


@app.post("/documents", status_code=201)
async def upload_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name  # evita rutas tipo ../../archivo
    if Path(filename).suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, f"Formato no soportado. Formatos válidos: {sorted(SUPPORTED_EXTENSIONS)}")

    content = await file.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"El archivo supera los {MAX_UPLOAD_MB} MB")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / filename
        tmp_path.write_bytes(content)
        try:
            stats = rag.add_document(tmp_path)
        except Exception as e:
            raise HTTPException(400, f"No se pudo procesar el archivo: {e}")

    return {"message": f"{filename} cargado e indexado", **stats}


@app.post("/reindex")
def reindex():
    return rag.build_index()
