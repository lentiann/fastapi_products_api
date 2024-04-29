from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLACHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost/shop"

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)