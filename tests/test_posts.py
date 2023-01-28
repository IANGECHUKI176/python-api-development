from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    posts = [schemas.PostOut(**post["Post"]) for post in response.json()]
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_post_by_id(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.get(f"/posts/{post_id}")
    post = schemas.PostOut(**response.json()['Post'])
    assert post.id == post_id
    assert response.status_code == 200


def test_unauthorized_user_get_post_by_id(client, test_posts):
    post_id = test_posts[0].id
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_one_post_not_exist(authorized_client):
    response = authorized_client.get("/posts/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'post with id:999 not found'}


@pytest.mark.parametrize("title, content, published", [
    ("First post", "This is my first post", True),
    ("Second post", "This is my second post", False),
    ("Third post", "This is my third post", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    post_data = {
        "title": title,
        "content": content,
        "published": published,
        "owner_id": test_user['id']
    }
    response = authorized_client.post("/posts/", json=post_data)
    post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user['id']


def test_create_post_published_true(authorized_client, test_user):
    post_data = {
        "title": "First post",
        "content": "This is my first post",
        "owner_id": test_user['id']
    }
    response = authorized_client.post("/posts/", json=post_data)
    post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert post.published == True


def test_unauthorized_user_create_post(client, test_user):
    post_data = {
        "title": "First post",
        "content": "This is my first post",
        "owner_id": test_user['id']
    }
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_post_success(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204


def test_unauthorized_user_delete_post(client, test_posts):
    post_id = test_posts[0].id
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_post_not_exist(authorized_client):
    response = authorized_client.delete("/posts/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'post with id:999 not found'}


def test_delete_post_not_owner(authorized_client, test_posts):
    post_id = test_posts[3].id
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 403
    assert response.json() == {'detail': 'you can only delete your own posts'}


def test_user_update_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    post_data = {
        "title": "First edited first post",
        "content": "This is my first post",
        "published": True
    }
    response = authorized_client.put(f"/posts/{post_id}", json=post_data)
    post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert post.title == post_data['title']
    assert post.content == post_data['content']
    assert post.published == post_data['published']


def test_unauthorized_user_update_post(client, test_posts):
    post_id = test_posts[0].id
    post_data = {
        "title": "First edited first post",
        "content": "This is my first post",
        "published": True
    }
    response = client.put(f"/posts/{post_id}", json=post_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_update_post_not_exist(authorized_client):
    post_data = {
        "title": "First edited first post",
        "content": "This is my first post",
        "published": True
    }
    response = authorized_client.put("/posts/999", json=post_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'post with id:999 not found'}


def test_update_post_not_owner(authorized_client, test_posts):
    post_id = test_posts[3].id
    post_data = {
        "title": "First edited first post",
        "content": "This is my first post",
        "published": True
    }
    response = authorized_client.put(f"/posts/{post_id}", json=post_data)
    assert response.status_code == 403
    assert response.json() == {'detail': 'you can only update your own posts'}

