import pytest
from fastapi import status
from app import models


base_url = "/api/v1/vote"

@pytest.fixture
def test_vote(test_posts, session, test_create_user):
  new_vote = models.Vote(post_id = test_posts[3].id, user_id=test_create_user["user_id"])

  session.add(new_vote)
  session.commit()


def test_vote_on_post(authorized_client, test_posts):
  vote_data = {
    "post_id": test_posts[0].id,
    "direction": 1
  }

  res = authorized_client.post(f"{base_url}/", json=vote_data)

  assert res.status_code == status.HTTP_201_CREATED


def test_vote_twice_on_post(authorized_client, test_create_user, test_posts, test_vote):
  vote_data = {
    "post_id": test_posts[3].id,
    "direction": 1
  }

  res = authorized_client.post(f"{base_url}/", json=vote_data)

  assert res.status_code == status.HTTP_409_CONFLICT


def test_delete_vote_on_post(authorized_client, test_create_user, test_posts, test_vote):
  vote_data = {
    "post_id": test_posts[3].id,
    "direction": 0
  }

  res = authorized_client.post(f"{base_url}/", json=vote_data)

  assert res.status_code == status.HTTP_201_CREATED


def test_delete_vote_on_post_non_exist(authorized_client, test_create_user, test_posts):
  vote_data = {
    "post_id": test_posts[3].id,
    "direction": 0
  }

  res = authorized_client.post(f"{base_url}/", json=vote_data)

  assert res.status_code == status.HTTP_404_NOT_FOUND


def test_unauthenticated_user_cannot_vote(client, test_create_user, test_posts):
  vote_data = {
    "post_id": test_posts[3].id,
    "direction": 0
  }

  res = client.post(f"{base_url}/", json=vote_data)

  assert res.status_code == status.HTTP_401_UNAUTHORIZED  
