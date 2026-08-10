# import 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

SQL_ALCHEMY_DATABASE_URL = "sqlit:///./todo.db"

# engine 
engine = create_engine(SQL_ALCHEMY_DATABASE_URL , connect_args={'check_same_thread':False})


# session

SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)


# config

Base = declarative_base()