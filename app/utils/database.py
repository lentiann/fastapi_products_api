import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLACHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost/shop"
SQLACHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

print("SQLACHEMY_DATABASE_URL", SQLACHEMY_DATABASE_URL)

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)