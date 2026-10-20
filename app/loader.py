"""Carga de documentos: PDF, TXT y Markdown."""
import re
from pathlib import Path

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def fix_pdf_lines(text):
    """
    pypdf corta los párrafos en varias líneas. Uno las líneas de un mismo párrafo,
    pero dejo el salto de línea después de los títulos (líneas cortas sin punto final),
    así el título no queda pegado a la primera oración.
    """
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"\d+\.", line):  # número de sección suelto, ej: "4."
            result.append(line + " ")
            continue
        is_title = len(line) < 60 and not line.endswith((".", ",", ":", ";"))
        result.append(line + ("\n" if is_title or line.endswith(".") else " "))
    return "".join(result).strip()


def load_document(path):
    """
    Lee un archivo y devuelve una lista de "páginas".
    Cada página es un dict: {"source": nombre_archivo, "page": número o None, "text": texto}
    Los TXT y MD se tratan como una sola página.
    """
    path = Path(path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Formato no soportado: {ext}. Usá PDF, TXT o MD.")

    if ext == ".pdf":
        reader = PdfReader(str(path))
        pages = []
        for number, page in enumerate(reader.pages, start=1):
            text = fix_pdf_lines(page.extract_text() or "")
            if text:
                pages.append({"source": path.name, "page": number, "text": text})
        return pages

    text = path.read_text(encoding="utf-8")
    return [{"source": path.name, "page": None, "text": text}]


def load_folder(folder):
    """Carga todos los documentos soportados de una carpeta (ordenados por nombre)."""
    folder = Path(folder)
    pages = []
    for path in sorted(folder.iterdir()):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            pages.extend(load_document(path))
    return pages
