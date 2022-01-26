from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


DB_USER = settings.database_username
DB_PASSWORD = settings.database_password
HOSTNAME = settings.database_hostname
DB_NAME = settings.database_name
DB_PORT = settings.database_port

# # SQLALCHEMY_DATABASE_URL = "postgresql://kosam:root@localhost:5432/fastapi_test"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOSTNAME}:{DB_PORT}/{DB_NAME}_test"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
  db = TestSessionLocal()
  try:
    yield db
  finally:
    db.close()


@pytest.fixture(scope="function")
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestSessionLocal()
  try:
      yield db
  finally:
      db.close()


@pytest.fixture
def client(session):
  def override_get_db():
    try:
        yield session
    finally:
        session.close()
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)
  


@pytest.fixture
def test_create_user(client):
  user_data = {
    "email": "test@gmail.com",
    "password": "password",
    "user_id": 1
  }
  res = client.post("/api/v1/users/create", json=user_data)
  assert res.status_code == 201
  return user_data


@pytest.fixture
def test_user(client):
  user_data = {
    "email": "test1@gmail.com",
    "password": "password",
    "user_id": 2
  }
  res = client.post("/api/v1/users/create", json=user_data)
  assert res.status_code == 201
  return user_data


@pytest.fixture
def token(test_create_user):
  return create_access_token({"user_id": test_create_user["user_id"]})


@pytest.fixture
def authorized_client(client, token):
  client.headers = {
    **client.headers,
    "Authorization": f"Bearer {token}"
  }
  return client


@pytest.fixture
def test_posts(test_create_user, session, test_user):
  posts_data = [
    {
      "title": "first title",
      "content": "first content",
      "owner_id": test_create_user["user_id"]
    },
    {
      "title": "second title",
      "content": "second content",
      "owner_id": test_create_user["user_id"]
    },
    {
      "title": "third title",
      "content": "third content",
      "owner_id": test_create_user["user_id"]
    },
    {
      "title": "fourth title",
      "content": "fourth content",
      "owner_id": test_user["user_id"]
    }
  ]

  def create_post_model(post):
    return models.Post(**post)

  post_map = map(create_post_model, posts_data)

  posts_list = list(post_map)  

  session.add_all(posts_list)
  session.commit()
  posts = session.query(models.Post).all()
  return posts