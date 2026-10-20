"""
Generación de la respuesta a partir de los fragmentos recuperados.

- ClaudeGenerator: usa la API de Anthropic. El prompt obliga a responder solo
  con la información de los fragmentos y a citar cada dato con [n].
- ExtractiveGenerator: no usa LLM. Elige las oraciones de los fragmentos que
  más se parecen a la pregunta. Sirve para correr el proyecto y los tests
  sin API key.
"""
import numpy as np

from app.chunker import split_sentences

NO_INFO_MESSAGE = (
    "No encontré información suficiente en la documentación para responder esa pregunta."
)
NO_INFO_TOKEN = "SIN_INFORMACION"

SYSTEM_PROMPT = f"""Sos un asistente que responde preguntas de empleados de NovaTech usando SOLO la documentación interna que se te da.

Reglas:
1. Respondé únicamente con información que esté en los fragmentos. No inventes datos.
2. Después de cada dato poné la cita del fragmento entre corchetes, por ejemplo [1] o [2].
3. Respondé en español, de forma clara y breve (máximo 4 oraciones).
4. Si los fragmentos no tienen la información para responder, respondé exactamente: {NO_INFO_TOKEN}"""


def format_context(sources):
    blocks = []
    for i, s in enumerate(sources, start=1):
        page = f", página {s['page']}" if s["page"] else ""
        blocks.append(f"[{i}] (Documento: {s['source']}{page})\n{s['text']}")
    return "\n\n".join(blocks)


class ClaudeGenerator:
    name = "claude"

    def __init__(self, api_key, model):
        import anthropic

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, question, sources):
        user_message = f"Fragmentos de la documentación:\n\n{format_context(sources)}\n\nPregunta: {question}"
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        answer = response.content[0].text.strip()
        if NO_INFO_TOKEN in answer:
            return None  # el modelo dijo que no tiene información
        return answer


class ExtractiveGenerator:
    name = "extractive"

    def __init__(self, embedder, max_sentences=3):
        self.embedder = embedder
        self.max_sentences = max_sentences

    def generate(self, question, sources):
        candidates = []  # (oración, número de fuente)
        for i, s in enumerate(sources, start=1):
            for sentence in split_sentences(s["text"]):
                # descarto títulos: son cortos o no terminan con punto
                if len(sentence.split()) >= 4 and sentence.endswith((".", "!", "?")):
                    candidates.append((sentence, i))
        if not candidates:
            return None

        vectors = self.embedder.encode([c[0] for c in candidates])
        query = self.embedder.encode([question])[0]
        scores = vectors @ query
        best = [i for i in np.argsort(scores)[::-1][: self.max_sentences] if scores[i] > 0]
        if not best:
            return None

        return " ".join(f"{candidates[i][0]} [{candidates[i][1]}]" for i in best)
