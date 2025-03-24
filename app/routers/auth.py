from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models import User
from app.schemas import UserCreationModel, TokenModel
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"
TOKEN_EXPIRE_TIME = 24 * 60 * 60

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=1000))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth/register")
def register(user: UserCreationModel, db: Session = Depends(get_db)):
    if (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    ):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = pwd_context.hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}


@router.post("/auth/login", response_model=TokenModel)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        user = db.query(User).get(user_id)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
