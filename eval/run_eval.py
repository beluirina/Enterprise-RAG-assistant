"""
Evaluación del asistente con un set de preguntas con respuesta esperada.

Mide tres cosas:
1. Recuperación: ¿el documento correcto aparece en el top-1 / top-k? (Hit@1, Hit@k)
2. Exactitud: ¿la respuesta contiene los datos esperados? (palabras clave)
3. Abstención: en preguntas sin respuesta en los documentos, ¿el sistema dice que no sabe?
   También cuenta cuántas veces se negó a responder algo que sí estaba documentado.

Uso:  python eval/run_eval.py
Genera eval/results.md y eval/results.json
"""
import json
import sys
import unicodedata
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config  # noqa: E402
from app.rag import RAGPipeline  # noqa: E402

EVAL_DIR = Path(__file__).parent


def normalize(text):
    """minúsculas y sin tildes, para comparar palabras clave"""
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def load_questions(path=EVAL_DIR / "questions.jsonl"):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def evaluate(rag, questions, top_k=None):
    top_k = top_k or config.TOP_K
    rows = []
    for q in questions:
        retrieved_docs = [r["source"] for r in rag.retrieve(q["question"], top_k)]
        result = rag.ask(q["question"], top_k)
        answer_norm = normalize(result["answer"])

        row = {
            "id": q["id"],
            "question": q["question"],
            "answerable": q["answerable"],
            "answer": result["answer"],
            "has_answer": result["has_answer"],
            "retrieved_docs": retrieved_docs,
        }
        if q["answerable"]:
            row["hit_at_1"] = retrieved_docs[:1] == [q["expected_doc"]]
            row["hit_at_k"] = q["expected_doc"] in retrieved_docs
            row["correct"] = result["has_answer"] and all(
                normalize(k) in answer_norm for k in q["expected_keywords"]
            )
            row["false_abstention"] = not result["has_answer"]
        else:
            row["correct"] = not result["has_answer"]
        rows.append(row)

    answerable = [r for r in rows if r["answerable"]]
    unanswerable = [r for r in rows if not r["answerable"]]

    def pct(items, key):
        return round(100 * sum(r[key] for r in items) / len(items), 1) if items else 0.0

    metrics = {
        "total_questions": len(rows),
        "answerable": len(answerable),
        "unanswerable": len(unanswerable),
        "hit_at_1": pct(answerable, "hit_at_1"),
        f"hit_at_{top_k}": pct(answerable, "hit_at_k"),
        "answer_accuracy": pct(answerable, "correct"),
        "false_abstention_rate": pct(answerable, "false_abstention"),
        "correct_abstention_rate": pct(unanswerable, "correct"),
    }
    return metrics, rows


def write_report(metrics, rows, generator, top_k):
    failures = [r for r in rows if not r["correct"]]
    lines = [
        "# Resultados de la evaluación",
        "",
        f"Fecha: {date.today()} · Embeddings: `{config.EMBEDDING_BACKEND}` · Generador: `{generator}` · top_k={top_k} · umbral={config.MIN_SCORE}",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Preguntas totales | {metrics['total_questions']} ({metrics['answerable']} con respuesta, {metrics['unanswerable']} sin respuesta) |",
        f"| Recuperación Hit@1 (doc correcto en el 1er lugar) | {metrics['hit_at_1']}% |",
        f"| Recuperación Hit@{top_k} (doc correcto en el top {top_k}) | {metrics[f'hit_at_{top_k}']}% |",
        f"| Exactitud de respuesta (contiene el dato esperado) | {metrics['answer_accuracy']}% |",
        f"| Abstención correcta (dice \"no sé\" cuando no hay info) | {metrics['correct_abstention_rate']}% |",
        f"| Abstención incorrecta (dice \"no sé\" pero sí había info) | {metrics['false_abstention_rate']}% |",
        "",
        f"## Errores ({len(failures)})",
        "",
        "| # | Pregunta | Esperado | Respuesta del sistema |",
        "|---|---|---|---|",
    ]
    for r in failures:
        expected = "responder" if r["answerable"] else "abstenerse"
        answer = r["answer"].replace("|", "/")[:140]
        lines.append(f"| {r['id']} | {r['question']} | {expected} | {answer} |")

    (EVAL_DIR / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (EVAL_DIR / "results.json").write_text(
        json.dumps({"metrics": metrics, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    rag = RAGPipeline()
    rag.load_or_build()
    metrics, rows = evaluate(rag, load_questions())
    write_report(metrics, rows, rag.generator.name, config.TOP_K)

    for key, value in metrics.items():
        print(f"{key:28} {value}")
    print("\nReporte completo en eval/results.md")
