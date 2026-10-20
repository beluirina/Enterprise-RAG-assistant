"""Test de regresión: si un cambio empeora mucho la calidad, este test falla."""
from pathlib import Path

from app.rag import RAGPipeline
from eval.run_eval import evaluate, load_questions

DOCS = Path(__file__).resolve().parent.parent / "data" / "docs"


def test_quality_does_not_drop(tmp_path):
    rag = RAGPipeline(docs_dir=DOCS, index_dir=tmp_path)
    rag.build_index()
    metrics, _ = evaluate(rag, load_questions(), top_k=4)

    assert metrics["hit_at_4"] >= 95
    assert metrics["answer_accuracy"] >= 80
    assert metrics["correct_abstention_rate"] >= 75
    assert metrics["false_abstention_rate"] <= 10
