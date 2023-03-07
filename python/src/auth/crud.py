from sqlalchemy.orm import Session
from models import User
from schemas import UserSchema
from passlib.context import CryptContext

# create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db:Session, skip:int=0, limit:int=100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session, user: UserSchema):
    hashed_password = pwd_context.hash(user.password)
    _user = User(email = user.email, password = hashed_password)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user

def remove_user(db:Session, user_id : int):
    _user = get_user_by_id(db = db, user_id = user_id)
    db.delete(_user)
    db.commit()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
