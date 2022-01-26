import pytest
from jose import jwt
from fastapi import status
from app.config import settings

base_url = "/api/v1/auth"



def test_login(client, test_create_user):
  request_body = {"email": test_create_user["email"], "password": test_create_user["password"]}
  res = client.post(f"{base_url}/login", json=request_body)

  payload = jwt.decode(res.json().get('access_token'), settings.secret_key, algorithms=[settings.algorithm])
  id: str = payload.get("user_id")
  print(id)
  assert res.json().get("token_type") == "bearer"
  assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("email, password, status_code", [
  ("wrongemail@gmail.com", "wrongpassword", 403),
  ("kosam@gmail.com", "wrongpassword", 403),
  (None, "wrongpassword", 422),
  ("test@gmail.com", None, 422)
])
def test_incorrect_login(test_create_user, client, email, password, status_code):
  res = client.post(f"{base_url}/login", json={"email": email, "password": password})

  assert res.status_code == status_code
