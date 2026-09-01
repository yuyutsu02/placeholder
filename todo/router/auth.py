from fastapi import APIRouter , Depends
from pydantic import Field , BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta , datetime , timezone

SECRET_KEY = "fv83mvH10OVfe65o788io865D3we56rt3y3id774b62J3K3B5796J2Bi4dv438KHjgv0rbBJgfrfVfUeYOb3h"
ALGO = "HS256"

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'] , deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]

def authenticate_user(username:str , password:str , db):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    elif(bcrypt_context.verify(password , user.hashed_password)):
        return user
    return False


def create_jwt(username:str , user_id:int , expires_delta:timedelta):
    encode = {'sub': username , 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode , SECRET_KEY , algorithm= ALGO)


class User_Request(BaseModel):
    first_name:str = Field(min_length= 1  , max_length= 20)
    last_name:str = Field(min_length= 1  , max_length= 20)
    username:str = Field(min_length=1 , max_length= 20) 
    email:str
    password:str
    is_active:bool
    role:str



@router.post("/auth")
async def auth_user(db:db_dependency , user_request:User_Request):
    create_user_model = Users(
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        username = user_request.username,
        email = user_request.email,
        hashed_password = bcrypt_context.hash(user_request.password),
        role = user_request.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token")
async def get_auth_token(form_data:Annotated[OAuth2PasswordRequestForm , Depends() ],db:db_dependency):

    user = authenticate_user(form_data.username , form_data.password , db)

    if user:
        token = create_jwt(user.username , user.id , timedelta(minutes=20))
        return {"access_token":token , "token_type":"bearer"}
    else:
        return "Failed Authentication"
        