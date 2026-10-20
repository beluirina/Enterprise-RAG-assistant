import pytest

from app.generator import NO_INFO_MESSAGE, NO_INFO_TOKEN, ClaudeGenerator
from app.rag import RAGPipeline


@pytest.fixture(scope="module")
def rag(tmp_path_factory):
    pipeline = RAGPipeline(index_dir=tmp_path_factory.mktemp("index"))
    pipeline.build_index()
    return pipeline


@pytest.mark.parametrize(
    "question, expected_doc",
    [
        ("¿Cuántos días de vacaciones tengo?", "politica_vacaciones.md"),
        ("¿Cuál es el límite de comidas en viajes nacionales?", "politica_gastos_viaticos.pdf"),
        ("¿Qué código devuelve la API si supero el límite de solicitudes?", "manual_api_pedidos.md"),
        ("¿Cuántos caracteres debe tener una contraseña?", "politica_seguridad_informatica.pdf"),
    ],
)
def test_retrieves_the_right_document(rag, question, expected_doc):
    assert rag.retrieve(question, top_k=1)[0]["source"] == expected_doc


def test_answer_includes_citations_and_sources(rag):
    result = rag.ask("¿Cuál es el límite de comidas en viajes nacionales?")
    assert result["has_answer"]
    assert "30.000" in result["answer"]
    assert "[1]" in result["answer"]
    assert result["sources"][0]["document"] == "politica_gastos_viaticos.pdf"
    assert result["sources"][0]["page"] == 2


def test_says_it_does_not_know(rag):
    result = rag.ask("¿Quién ganó el último mundial de fútbol?")
    assert not result["has_answer"]
    assert result["answer"] == NO_INFO_MESSAGE
    assert result["sources"] == []


def test_index_can_be_saved_and_loaded(rag):
    other = RAGPipeline(index_dir=rag.index_dir)
    assert other.load_index()
    assert len(other.store) == len(rag.store)


# ---------- Generador con Claude (con un cliente falso, sin llamar a la API) ----------

class FakeClient:
    def __init__(self, reply):
        self.reply = reply
        self.last_call = None
        self.messages = self

    def create(self, **kwargs):
        self.last_call = kwargs
        text = self.reply

        class Block:
            pass

        block = Block()
        block.text = text

        class Response:
            content = [block]

        return Response()


def make_claude_generator(reply):
    generator = ClaudeGenerator.__new__(ClaudeGenerator)  # evita crear el cliente real
    generator.client = FakeClient(reply)
    generator.model = "test-model"
    return generator


SOURCES = [{"source": "politica_vacaciones.md", "page": None, "text": "Menos de 5 años: 14 días corridos."}]


def test_claude_generator_sends_context_and_returns_answer():
    generator = make_claude_generator("Te corresponden 14 días corridos [1].")
    answer = generator.generate("¿Cuántos días tengo?", SOURCES)
    assert answer == "Te corresponden 14 días corridos [1]."
    prompt = generator.client.last_call["messages"][0]["content"]
    assert "[1] (Documento: politica_vacaciones.md)" in prompt
    assert "14 días corridos" in prompt


def test_claude_generator_handles_no_info():
    generator = make_claude_generator(NO_INFO_TOKEN)
    assert generator.generate("¿Cuál es el sueldo del CEO?", SOURCES) is None


def test_pipeline_uses_no_info_message_when_llm_refuses(rag):
    pipeline = RAGPipeline(index_dir=rag.index_dir, embedder=rag.embedder, generator=make_claude_generator(NO_INFO_TOKEN))
    pipeline.store = rag.store
    result = pipeline.ask("¿Cuántos días de vacaciones tengo?")
    assert not result["has_answer"]
    assert result["answer"] == NO_INFO_MESSAGE
