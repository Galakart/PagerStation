"""Конфигурационный файл"""
IS_TEST = False

DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_HOST = 'localhost'
DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

OWM_TOKEN = ''
OWM_CITY = 'Novokuznetsk'
