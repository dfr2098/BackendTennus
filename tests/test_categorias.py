from fastapi.testclient import TestClient
from sqlmodel import Session

from ..models import Categoria


def test_validacion_nombre(client: TestClient):
    response = client.post('/categorias/create', json={'nombre': 'sa'})
    data = response.json()
    print(data)

    assert response.status_code == 422

def test_se_puede_crear_una_categoria(client: TestClient):
    response = client.post("/categorias/create", json={"nombre": "Mi categoria"})
    data = response.json()

    assert response.status_code == 201
    assert data['id'] == 1

def test_se_pueden_leer_las_categorias(session: Session, client: TestClient):
    session.add(Categoria(nombre="clonazepam"))
    session.commit()

    response = client.get("/categorias/")
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == 1
    assert data[0]['nombre'] == 'clonazepam'
