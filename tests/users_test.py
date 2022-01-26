from fastapi import status


base_url = "/api/v1/users"


def test_root(client):
  res = client.get("/")
  print(res.json())
  assert res.status_code == status.HTTP_200_OK



def test_create_user(client):
  request_body = {
    "email": "test@gmail.com",
    "password": "password"
  }
  res = client.post(f"{base_url}/create", json=request_body)
  assert res.status_code == status.HTTP_201_CREATED