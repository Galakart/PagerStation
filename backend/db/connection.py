"""Соединение с БД"""
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_session():
    """Экземпляр сессии sqlalchemy"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record): # pylint: disable=unused-argument
    """Включение foreign_keys у sqlite3"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
