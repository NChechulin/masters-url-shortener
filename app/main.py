from fastapi import FastAPI
from app.routers import links, auth
from app.database import Base, engine

app = FastAPI(
    title="URL Shortener",
    description="A small service for creating shortened URLs with auth and analytics",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(links.router, prefix="", tags=["Links"])
app.include_router(auth.router, prefix="", tags=["Auth"])
