from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

DATABASE_URL = "postgresql://urluser:Bjz3N1nO90Ghocp1tO9Pjb0nEAU6Y5Xc@dpg-cvkop0be5dus73bsdcug-a.frankfurt-postgres.render.com/url_shortener_hqlz"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
