import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.json
    assert 'hostname' in response.json