import os
from fastapi import APIRouter, HTTPException, Path, Depends, Header
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import UserSchema, RequestUser, Response
import crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt

load_dotenv(".env")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

JWT_SECRET = os.environ["X_TOKEN"]
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/create')
async def create(request : RequestUser, db:Session = Depends(get_db)):
    crud.create_user(db, request.parameter)
    return Response(code=200, status = "ok", message = "user created successfully").dict(exclude_none = True)

def authenticate_user(db, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not crud.verify_password(password, user.hashed_password):
        return False
    return user

@router.get('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        return create_jwt(form_data.email,JWT_SECRET,True)

def create_jwt(email, secret, authz):
    return jwt.encode({
        "email":email,
        "exp":datetime.now(tz=datetime._local_timezone.utc)
        + timedelta(days=1),
        "iat":datetime.utcnow(),
        "admin":authz,

    },
    secret,
    algorithm = "HS256")

@router.post("/validate")
async def validate(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return payload




