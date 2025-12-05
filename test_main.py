"""
Tests for the Flask application.
Run with: pytest
"""
import pytest
from main import app, conversations, SYSTEM_PROMPT


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Chatbot Absurde' in response.data


def test_chat_missing_message(client):
    """Test chat endpoint with missing message"""
    response = client.post('/api/chat', 
        json={'conversation_id': 'test1'},
        content_type='application/json'
    )
    assert response.status_code == 400


def test_chat_empty_message(client):
    """Test chat endpoint with empty message"""
    response = client.post('/api/chat',
        json={'message': '', 'conversation_id': 'test2'},
        content_type='application/json'
    )
    assert response.status_code == 400


def test_chat_message_too_long(client):
    """Test chat endpoint with overly long message"""
    long_message = 'a' * 1001
    response = client.post('/api/chat',
        json={'message': long_message, 'conversation_id': 'test3'},
        content_type='application/json'
    )
    assert response.status_code == 400


def test_reset_conversation(client):
    """Test reset endpoint"""
    response = client.post('/api/reset',
        json={'conversation_id': 'test4'},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_404_not_found(client):
    """Test 404 error"""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_security_headers(client):
    """Test security headers are present"""
    response = client.get('/')
    assert 'X-Content-Type-Options' in response.headers
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert 'X-Frame-Options' in response.headers
    assert response.headers['X-Frame-Options'] == 'DENY'
