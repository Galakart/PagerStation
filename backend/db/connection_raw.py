"""Подключения для сырых запросов в БД"""

import logging

import config
import pymysql

LOGGER = logging.getLogger('applog')


def open_connection():
    """Открытие соединения к базе"""
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        passwd=config.DB_PASSWORD,
        db=config.DB_NAME,
        use_unicode=1,
        charset='utf8mb4'
    )


def close_connection(connection):
    """Закрытие соединения"""
    connection.close()
