"""Конфигурационный файл"""
IS_TEST = False

DB_USER = ''
DB_PASSWORD = ''
DB_NAME = 'pagerstation'
DB_HOST = 'localhost'
DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

OWM_TOKEN = ''
OWM_LATITUDE = 53.77
OWM_LONGITUDE = 87.17
