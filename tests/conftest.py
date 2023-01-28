import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.test_database_username}:{settings.test_database_password}@" \
                          f"{settings.test_database_hostname}:{settings.test_database_port}/{settings.test_database_name}"
# when using sqlite database you have to use pass in this arg to the create_engine function
# connect_args={"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "bob@gmail.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {"email": "john@gmail.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_user, client):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(test_user, session, test_user2):
    post_data = [
        {
            "title": "First post",
            "content": "This is my first post",
            "owner_id": test_user['id']
        },
        {
            "title": "Second post",
            "content": "This is my second post",
            "owner_id": test_user['id']
        },
        {
            "title": "Third post",
            "content": "This is my third post",
            "owner_id": test_user['id']
        }, {
            "title": "Fourth post",
            "content": "This is my fourth post",
            "owner_id": test_user2['id']
        }
    ]

    def create_post(post):
        return models.Post(**post)

    post_map = map(create_post, post_data)
    session.add_all(list(post_map))
    # session.add_all(models.Post(**post) for post in post_data)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
