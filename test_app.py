import pytest
from flask import session
from app import db, User
from time import sleep

def test_index_page(test_client):
    response = test_client.get('/')
    # print(response.data)
    assert response.status_code == 200
    #sleep(20) # ensure the page is loaded before checking the content
    assert b"All AI Prompts You need in One Marketplace" in response.data

def test_signup_page(test_client):
    response = test_client.post('/signup', data=dict(
        name='Test User',
        email='testuser_unique@example.com',  # Ensure unique email for each test run
        password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter_by(email='testuser_unique@example.com').first()
    assert user is not None
    assert user.fullName == 'Test User'

def test_login_logout_page(test_client):
    # Create unique user for this test
    user = User(fullName='Test User', email='testuser_unique@example.com', password='testpassword')
    if User.query.filter_by(email='testuser_unique@example.com').first() is None:
        db.session.add(user)
        db.session.commit()
    else:
        user = User.query.filter_by(email='testuser_unique@example.com').first()


    response = test_client.post('/login', data=dict(
        email='testuser_unique@example.com',
        password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert session['logged_in']
    assert session['current_user'] == 'Test User'

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert not session.get('logged_in')

def test_protected_page(test_client):
    response = test_client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

    # Log in with the unique user for this test
    test_client.post('/login', data=dict(
        email='testuser_unique@example.com',
        password='testpassword'
    ), follow_redirects=True)
    response = test_client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Profile' in response.data

def test_404_page(test_client):
    response = test_client.get('/nonexistent')
    assert response.status_code == 404
    assert b'404 Not Found' in response.data
