import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # el "with" ejecuta el lifespan (crea el índice)
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["chunks_indexed"] > 0


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Asistente" in response.text


def test_ask_returns_answer_with_sources(client):
    response = client.post("/ask", json={"question": "¿Cuántas solicitudes por minuto permite la API de Pedidos?"})
    assert response.status_code == 200
    data = response.json()
    assert data["has_answer"]
    assert "100" in data["answer"]
    assert data["sources"][0]["document"] == "manual_api_pedidos.md"


def test_ask_without_information(client):
    data = client.post("/ask", json={"question": "¿Qué receta de empanadas recomiendan?"}).json()
    assert data["has_answer"] is False
    assert data["sources"] == []


def test_ask_validates_input(client):
    assert client.post("/ask", json={"question": ""}).status_code == 422
    assert client.post("/ask", json={"question": "hola que tal", "top_k": 50}).status_code == 422


def test_list_documents(client):
    names = [d["name"] for d in client.get("/documents").json()]
    assert "politica_vacaciones.md" in names


def test_upload_new_document_and_ask_about_it(client):
    content = "Política de Mascotas. Los empleados pueden traer perros a la oficina los días viernes.".encode()
    response = client.post("/documents", files={"file": ("politica_mascotas.txt", content, "text/plain")})
    assert response.status_code == 201

    data = client.post("/ask", json={"question": "¿Qué día puedo traer mi perro a la oficina?"}).json()
    assert data["has_answer"]
    assert "viernes" in data["answer"]
    assert data["sources"][0]["document"] == "politica_mascotas.txt"


def test_upload_rejects_unsupported_format(client):
    response = client.post("/documents", files={"file": ("datos.xlsx", b"123", "application/octet-stream")})
    assert response.status_code == 400
