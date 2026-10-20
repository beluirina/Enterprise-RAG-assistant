import pytest

from app.chunker import chunk_pages, chunk_text, split_sentences
from app.loader import load_document, load_folder


def test_load_markdown(tmp_path):
    f = tmp_path / "nota.md"
    f.write_text("# Título\n\nHola mundo.", encoding="utf-8")
    pages = load_document(f)
    assert len(pages) == 1
    assert pages[0]["source"] == "nota.md"
    assert pages[0]["page"] is None
    assert "Hola mundo" in pages[0]["text"]


def test_load_pdf_keeps_page_numbers(conftest_docs_dir):
    pages = load_document(conftest_docs_dir / "politica_gastos_viaticos.pdf")
    assert [p["page"] for p in pages] == [1, 2, 3]
    assert "ARS 30.000" in pages[1]["text"]


def test_unsupported_format_raises(tmp_path):
    f = tmp_path / "planilla.xlsx"
    f.write_bytes(b"123")
    with pytest.raises(ValueError):
        load_document(f)


def test_load_folder_reads_all_docs(conftest_docs_dir):
    sources = {p["source"] for p in load_folder(conftest_docs_dir)}
    assert {"politica_vacaciones.md", "codigo_de_conducta.pdf", "guia_onboarding.txt"} <= sources


def test_split_sentences_removes_markdown():
    sentences = split_sentences("## Título\n\n- Primer punto. Segunda oración.")
    assert sentences == ["Título", "Primer punto.", "Segunda oración."]


def test_chunks_respect_size_and_overlap():
    text = " ".join(f"Esta es la oración número {i}." for i in range(50))  # 6 palabras c/u
    chunks = chunk_text(text, chunk_size=30, overlap_sentences=1)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c.split()) <= 36  # tamaño + una oración de overlap
    # la última oración de un chunk se repite al principio del siguiente
    assert chunks[0].splitlines()[-1] == chunks[1].splitlines()[0]


def test_chunk_pages_adds_metadata():
    pages = [{"source": "doc.pdf", "page": 2, "text": "Una oración corta."}]
    chunks = chunk_pages(pages)
    assert chunks == [{"id": "doc.pdf#p2-0", "source": "doc.pdf", "page": 2, "text": "Una oración corta."}]


@pytest.fixture
def conftest_docs_dir():
    from app import config

    return config.DOCS_DIR
