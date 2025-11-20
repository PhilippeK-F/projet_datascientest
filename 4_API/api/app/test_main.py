from fastapi.testclient import TestClient
from .main import app
import base64
import os

client = TestClient(app)

def test_health():
    response = client.get('/health')
    data = response.json()
    assert data.get('message') == "L'API est fonctionnelle."

def get_basic_auth_header(username: str, password: str):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

def test_historical():
    headers = get_basic_auth_header(os.getenv("API_USER"), os.getenv("API_PASSWORD"))
    response = client.get('/historical', params={'symbol': 'BTCUSDT', 'limit': '10'}, headers=headers)
    assert response.status_code == 200

def test_latest():
    headers = get_basic_auth_header(os.getenv("API_USER"), os.getenv("API_PASSWORD"))
    response = client.get('/latest', params={'symbol': 'BTCUSDT'}, headers=headers)
    assert response.status_code == 200

def test_predict():
    headers = get_basic_auth_header(os.getenv("API_USER"), os.getenv("API_PASSWORD"))
    response = client.post('/predict', params={'symbol': 'BTCUSDT', 'interval': '1h'}, headers=headers)
    assert response.status_code == 200
