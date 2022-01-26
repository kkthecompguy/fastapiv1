from fastapi import status
import pytest
from app import schemas

base_url = "/api/v1/posts"

def test_get_all_posts(authorized_client, test_posts):
  res = authorized_client.get(f"{base_url}/")
  def validate(post):
    return schemas.PostOut(**post)
  post_map = map(validate, res.json().get("data"))
  assert res.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_all_posts(client, test_posts):
  res = client.get(f"{base_url}/")
  assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_posts(client, test_posts):
  res = client.get(f"{base_url}/detail/{test_posts[0].id}")
  assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_non_exist(authorized_client, test_posts):
  res = authorized_client.get(f"{base_url}/detail/{len(test_posts) + 1}")
  assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post_detail(authorized_client, test_posts):
  res = authorized_client.get(f"{base_url}/detail/{test_posts[0].id}")
  post = schemas.PostOut(**res.json().get("data"))
  assert post.Post.id == test_posts[0].id
  assert res.status_code == status.HTTP_200_OK



@pytest.mark.parametrize("title, content, published", [
  ("title four", "content four", True),
  ("title five", "content five", True),
  ("title six", "content six", True),
])
def test_create_post(authorized_client, test_posts, title, content, published):
  post_data = {
    "title": title,
    "content": content,
    "published": published
  }
  res = authorized_client.post(f"{base_url}/create", json=post_data)
  assert res.status_code == status.HTTP_201_CREATED


def test_unauthorized_user_create_post(client):
  post_data = {
    "title": "title",
    "content": "content",
    "published": True
  }
  res = client.post(f"{base_url}/create", json=post_data)
  assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_delete_post(client, test_create_user, test_posts):
  res = client.delete(f"{base_url}/delete/{test_posts[0].id}")
  assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_success_user_delete_post(authorized_client, test_create_user, test_posts):
  res = authorized_client.delete(f"{base_url}/delete/{test_posts[0].id}")
  assert res.status_code == status.HTTP_204_NO_CONTENT


def test_user_delete_post_non_exist(authorized_client, test_create_user, test_posts):
  res = authorized_client.delete(f"{base_url}/delete/{len(test_posts) + 1}")
  assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(authorized_client, test_create_user, test_posts):
  res = authorized_client.delete(f"{base_url}/delete/{test_posts[3].id}")
  assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_create_user, test_posts):
  post_data = {
    "title": "updated title",
    "content": "updated content",
  }
  res = authorized_client.put(f"{base_url}/edit/{test_posts[0].id}", json=post_data)

  assert res.status_code == status.HTTP_200_OK


def test_update_other_user_post(authorized_client, test_create_user, test_user, test_posts):
  post_data = {
    "title": "updated title",
    "content": "updated content",
  }

  res = authorized_client.put(f"{base_url}/edit/{test_posts[3].id}", json=post_data)

  assert res.status_code == status.HTTP_403_FORBIDDEN



def test_unauthorized_user_update_post(client, test_create_user, test_posts):
  post_data = {
    "title": "updated title",
    "content": "updated content",
  }
  res = client.put(f"{base_url}/edit/{test_posts[0].id}", json=post_data)
  assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_delete_post_non_exist(authorized_client, test_create_user, test_posts):
  post_data = {
    "title": "updated title",
    "content": "updated content",
  }
  res = authorized_client.put(f"{base_url}/edit/{len(test_posts) + 1}", json=post_data)
  assert res.status_code == status.HTTP_404_NOT_FOUND
