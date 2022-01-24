import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

DB_USER = settings.database_username
DB_PASSWORD = settings.database_password
HOSTNAME = settings.database_hostname
DB_NAME = settings.database_name
DB_PORT = settings.database_port

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOSTNAME}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



create_post_table = "CREATE TABLE IF NOT EXISTS posts(id serial PRIMARY KEY, title varchar(100) not null, content varchar(255) not null, published boolean default True, rating integer default 0, created_at timestamp default CURRENT_TIMESTAMP, updated_at timestamp default CURRENT_TIMESTAMP);"

while True:
  try:
    conn = psycopg2.connect(host = HOSTNAME, database = DB_NAME, user = DB_USER, password = DB_PASSWORD, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    # cursor.execute(create_post_table)
    print('database connection was successful')
    break
  except Exception as e:
    print('connecting to database failed')
    print('error', e)
    time.sleep(2)