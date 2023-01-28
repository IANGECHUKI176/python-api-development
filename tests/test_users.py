from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     assert response.json().get("message") == "Welcome to my api pal"
#     assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "bob@gmail.com", "password": "123456"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "bob@gmail.com"
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert response.status_code == 200
    assert id == test_user['id']
    assert login_response.token_type == "bearer"


@pytest.mark.parametrize("email, password,status_code", [
    ("bob@gmail.com", "wrong password", 403),
    ("wrong email", "123456", 403),
    ("wrong email", "wrong password", 403),
    (None, "123456", 422),
    ("bob@gmail.com", None, 422),
])
def test_invalid_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
