from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

sessionLocal = sessionmaker(bind=engine)
    
Base = declarative_base()



def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


