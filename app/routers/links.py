from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Link
from app.schemas import LinkCreateModel, LinkUpdateModel, LinkDetailsModel
from app.redis_client import redis_client
from app.routers.auth import get_user
from datetime import datetime
from fastapi.responses import RedirectResponse
from app.models import User
import random
import string


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_code(n=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=n))


@router.post("/links/shorten", response_model=LinkDetailsModel)
def create_short_link(
    link: LinkCreateModel,
    db: Session = Depends(get_db),
    user: User = Depends(get_user),
):
    short_code = generate_short_code()

    if link.custom_alias:
        existing = db.query(Link).filter_by(custom_alias=link.custom_alias).first()
        if existing:
            raise HTTPException(status_code=400, detail="Custom alias already taken")

    new_link = Link(
        short_code=short_code,
        custom_alias=link.custom_alias,
        original_url=link.original_url,
        user_id=user.id,
        expires_at=link.expiration,
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    redis_client.set(name=short_code, value=link.original_url, keepttl=link.expiration)

    return new_link


@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    original_url = redis_client.get(short_code)
    if original_url:
        link = db.query(Link).filter((Link.code == short_code)).first()
        if link:
            link.clicks += 1
            link.last_access = datetime.now(datetime.timezone.utc)
            db.commit()
        return RedirectResponse(original_url)

    link = db.query(Link).filter((Link.code == short_code)).first()

    if not link:
        raise HTTPException(status_code=404, detail="Not found")

    if link.expiration and datetime.now(datetime.timezone.utc) > link.expiration:
        raise HTTPException(status_code=410, detail="Link expired")

    redis_client.set(short_code, link.original_url)

    link.clicks += 1
    link.last_access = datetime.now(datetime.timezone.utc)
    db.commit()

    return RedirectResponse(link.original_url)


@router.delete("/links/{short_code}")
def delete(
    short_code: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_user),
):
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link or link.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(link)
    db.commit()
    redis_client.delete(short_code)

    return {"detail": "Deleted"}


@router.put("/links/{short_code}", response_model=LinkDetailsModel)
def update(
    short_code: str,
    data: LinkUpdateModel,
    db: Session = Depends(get_db),
    user: User = Depends(get_user),
):
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link or link.user_id != user.id:
        raise HTTPException(status_code=403)

    link.original_url = data.original_url
    db.commit()
    redis_client.set(short_code, link.original_url)

    return link


@router.get("/links/{short_code}/stats", response_model=LinkDetailsModel)
def statistics(
    short_code: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_user),
):
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link or link.user_id != user.id:
        raise HTTPException(status_code=403)

    return link
