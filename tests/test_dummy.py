# tests/test_dummy.py
import pytest
from app import app

# Use Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page returns correct message."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to SecureQuizPlatform" in response.data

def test_result_page(client):
    """Test the result page returns correct quiz ID."""
    response = client.get('/result/1')
    assert response.status_code == 200
    assert b"Result for Quiz ID: 1" in response.data