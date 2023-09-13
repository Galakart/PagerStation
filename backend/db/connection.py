
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
