from fastapi import APIRouter, Depends , HTTPException , Path , status
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel , Field
import models
from typing import Annotated



router = APIRouter()


class Todo_Request(BaseModel):
    title:str = Field(min_length= 3  , max_length= 30)
    description:str = Field(min_length=6 , max_length= 60)
    priority:int = Field(gt=0 , lt=10)
    complete:bool



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]





@router.get("/" , status_code=status.HTTP_200_OK)
async def root(db: db_dependency):
    return db.query(models.Todo).all()


@router.get("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def get_todo(db : db_dependency , todo_id: int =  Path(gt = 0 , title = "The ID of the todo to get")):
    
    task =  db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if task is None:
        raise HTTPException(status_code=404 , detail = "Todo not found")
    else:
        return task

@router.post("/todo/" ,status_code=status.HTTP_201_CREATED)
async def create_todo(db : db_dependency , todo_request : Todo_Request):
    todo = models.Todo(**todo_request.model_dump())

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependency ,
                      todo_request: Todo_Request,
                      todo_id: int =  Path(gt = 0 , title = "The ID of the todo to get")):

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Not Found")
    else:
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.complete = todo_request.complete

        db.add(todo)
        db.commit()
        db.refresh(todo)

        return todo
    

@router.delete("/todo/{todo_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency , todo_id:int = Path(gt=0 ,title="The ID of TODO to delete" )):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Not Found")
    else:
        db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    db.commit()
