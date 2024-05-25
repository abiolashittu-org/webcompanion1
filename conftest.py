import pytest
from app import app, db, User

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['WTF_CSRF_ENABLED'] = False

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='module')
def new_user():
    user = User(
        fullName='Test User',
        email='testuser@example.com',
        password='testpassword'
    )
    return user