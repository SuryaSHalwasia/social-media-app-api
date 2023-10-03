import os
import sys
from fastapi.testclient import TestClient
import app.config as config
import app.database

from app.main import app
import app.schemas as schemas
from app.database import get_db, Base
import pytest

# Get the parent directory of the current script (tests directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

import app.models as models
# Add the parent directory to the Python path
sys.path.append(parent_dir)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2 as ps

from psycopg2.extras import RealDictCursor

from app.config import settings
from app.ouath2 import create_access_token
from app.models import Post
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(settings.DB_USERNAME, settings.DB_PASSWORD,
                                                            settings.DB_HOSTNAME,settings.DB_PORT, 
                                                            settings.DB_TEST)

while True:
    try:
        conn = ps.connect(host = settings.DB_HOSTNAME, database = settings.DB_NAME,
                          user = settings.DB_USERNAME, password = settings.DB_PASSWORD, 
                          cursor_factory= RealDictCursor)
        cur = conn.cursor()
        print("Connection successful.")
        break
    except Exception as err:
        print("Connection failed as {}".format(err))
        time.sleep(2)

engine = create_engine( SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    #before test runs
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #after test runs


@pytest.fixture()
def test_user(client):
    user_data = {"email":"s@gmail.com",
                 "password":"pops123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user_second(client):
    user_data = {"email":"shalwasia@gmail.com",
                 "password":"checksum"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def test_posts(test_user, session, test_user_second):
    posts_data = [
        {
            "title" : "My favorite book",
            "body" : " I wanna share with you guys my favorite book - Great Expectations",
            "user_id" : test_user["id"]
        },
        {
            "title" : "My favorite movie",
            "body" : " I wanna share with you guys my favorite movie - Interstellar",
            "user_id" : test_user["id"]
        },
        {
            "title" : "My favorite series",
            "body" : " I wanna share with you guys my favorite series - Breaking Bad",
            "user_id" : test_user_second["id"]
        }]
    
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    post = list(post_map)


    session.add_all(post)
    session.commit()

    posts = session.query(models.Post).all()
    return posts