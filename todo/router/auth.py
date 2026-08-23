from fastapi import APIRouter , Depends
from pydantic import Field , BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'] , deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]

class User_Request(BaseModel):
    first_name:str = Field(min_length= 2  , max_length= 20)
    last_name:str = Field(min_length= 2  , max_length= 20)
    username:str = Field(min_length=5 , max_length= 20) 
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
