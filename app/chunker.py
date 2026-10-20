"""
División de documentos en fragmentos (chunks).

Estrategia: separo el texto en oraciones y las voy juntando hasta llegar
a ~CHUNK_SIZE palabras. Cada chunk nuevo repite la última oración del
anterior (overlap) para no perder contexto en los cortes.
"""
import re


def split_sentences(text):
    """Separa el texto en oraciones / líneas y limpia símbolos de markdown."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    sentences = []
    pending_number = ""  # para no separar "4." de "Anticipos"
    for part in parts:
        part = part.strip().lstrip("#-*• ").strip()
        part = re.sub(r"\s+", " ", part)
        if re.fullmatch(r"\d+\.", part):
            pending_number = part + " "
        elif part:
            sentences.append(pending_number + part)
            pending_number = ""
    return sentences


def chunk_text(text, chunk_size=120, overlap_sentences=1):
    """Devuelve una lista de strings, cada uno de ~chunk_size palabras."""
    sentences = split_sentences(text)
    chunks = []
    current = []
    current_words = 0

    for sentence in sentences:
        words = len(sentence.split())
        if current and current_words + words > chunk_size:
            chunks.append("\n".join(current))
            # overlap: arranco el siguiente chunk con las últimas oraciones
            current = current[-overlap_sentences:] if overlap_sentences > 0 else []
            current_words = sum(len(s.split()) for s in current)
        current.append(sentence)
        current_words += words

    if current:
        chunks.append("\n".join(current))
    return chunks


def chunk_pages(pages, chunk_size=120, overlap_sentences=1):
    """Recibe las páginas del loader y devuelve chunks con su metadata."""
    chunks = []
    for page in pages:
        for i, text in enumerate(chunk_text(page["text"], chunk_size, overlap_sentences)):
            page_label = f"p{page['page']}" if page["page"] else "p1"
            chunks.append(
                {
                    "id": f"{page['source']}#{page_label}-{i}",
                    "source": page["source"],
                    "page": page["page"],
                    "text": text,
                }
            )
    return chunks
