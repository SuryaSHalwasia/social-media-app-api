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
