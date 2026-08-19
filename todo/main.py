from fastapi import FastAPI , Depends , HTTPException , Path , status
import models
from database import engine , SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel , Field




app = FastAPI()
class Todo_Request(BaseModel):
    title:str = Field(min_length= 3  , max_length= 30)
    description:str = Field(min_length=6 , max_length= 60)
    priority:int = Field(gt=0 , lt=10)
    complete:bool



models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]





@app.get("/" , status_code=status.HTTP_200_OK)
async def root(db: db_dependency):
    return db.query(models.Todo).all()


@app.get("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def get_todo(db : db_dependency , todo_id: int =  Path(gt = 0 , title = "The ID of the todo to get")):
    
    task =  db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if task is None:
        raise HTTPException(status_code=404 , detail = "Todo not found")
    else:
        return task

@app.post("/todo/" ,status_code=status.HTTP_201_CREATED)
async def create_todo(db : db_dependency , todo_request : Todo_Request):
    todo = models.Todo(**todo_request.model_dump())

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
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
    

