from database import Base
from sqlalchemy import Column , Integer , String , Boolean , ForeignKey


class Users(Base):
    __tablename__ = 'User'

    id = Column(Integer , primary_key= True , index= True)
    first_name = Column(String)
    last_name  = Column(String)
    username = Column(String , unique= True)
    email = Column(String , unique= True)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)



class Todo(Base):
    __tablename__ = 'Todo'

    id = Column(Integer , primary_key = True , index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean , default = False)
    owner = Column(Integer , ForeignKey("User.id"))