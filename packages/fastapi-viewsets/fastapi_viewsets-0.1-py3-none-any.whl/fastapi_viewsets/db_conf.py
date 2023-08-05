import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
SEPARATOR = os.path.sep
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR += SEPARATOR
load_dotenv(f"{BASE_DIR}.env")

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL') or f"sqlite:///{BASE_DIR}foo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(engine)

def get_session():
    return SessionLocal()
