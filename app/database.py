from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2 as ps

from psycopg2.extras import RealDictCursor

from app.config import settings
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(settings.DB_USERNAME, settings.DB_PASSWORD,
                                                            settings.DB_HOSTNAME,settings.DB_PORT, 
                                                            settings.DB_NAME)

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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()