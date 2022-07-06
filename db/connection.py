"""Соединение с БД"""
import config as botconf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(botconf.DB_URL, pool_size=200)
Session = sessionmaker(bind=engine)
