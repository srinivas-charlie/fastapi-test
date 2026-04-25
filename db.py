from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
with engine.connect() as connection:
    print("db connection succesful")
    
Base = declarative_base()
sessionlocal = sessionmaker()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


