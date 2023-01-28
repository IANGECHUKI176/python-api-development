import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(user_id=test_user["id"], post_id=test_posts[0].id)
    session.add(new_vote)
    session.commit()
    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 1})

    assert response.status_code == 201
    assert response.json() == {'message': 'vote created'}


def test_vote_twice(authorized_client, test_posts, test_vote):
    response = authorized_client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 1})
    assert response.status_code == 409
    assert response.json() == {'detail': 'user with id:1 already voted for post with id:1'}


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 0})
    assert response.json() == {'message': 'vote deleted'}


def test_delete_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post('/vote/', json={'post_id': 100, 'dir': 0})
    assert response.status_code == 404
    assert response.json() == {'detail': 'post with id:100 not found'}


def test_vote_on_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post('/vote/', json={'post_id': 100, 'dir': 1})
    assert response.status_code == 404
    assert response.json() == {'detail': 'post with id:100 not found'}


def test_vote_unauthorized(client, test_posts):
    response = client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 1})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
