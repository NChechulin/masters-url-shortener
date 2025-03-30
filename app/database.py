from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from os import getenv

DATABASE_HOST = getenv("DATABASE_URL", "postgres")
DATABASE_URL = (
    f"postgresql://urluser:verysecurepassword@{DATABASE_HOST}:5432/url_shortener"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
