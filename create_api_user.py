"""Создание первого пользователя с доступом к API"""
import datetime
import uuid

from backend.db.auth import create_access_token, get_password_hash
from backend.db.connection import SessionLocal
from backend.models.model_user import User

print('Создание пользователя с доступом к API')
api_login = input('Введите логин пользователя: ')
api_password = input('Введите пароль пользователя: ')
fio = input('Введите ФИО пользователя: ')

with SessionLocal() as session:
    user = User(
        uid=uuid.uuid4(),
        fio=fio,
        api_login=api_login,
        api_password=get_password_hash(api_password)
    )
    session.add(user)
    session.commit()
    print(f'Пользователь {api_login} создан.')
    print()

    access_token = create_access_token(
        username=api_login,
        expires_delta=datetime.timedelta(days=365 * 10)
    )
    print('Создан Bearer-токен доступа сроком действия 10 лет:')
    print(access_token)
    print('Сохраните его для использования в долговременных сервисах (например в Алисе)')
    print()
