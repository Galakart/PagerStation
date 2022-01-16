import os
import sys
import time
from pathlib import Path

import environ
import telebot
from telebot import types
import dbops as db

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

TOKEN_TELEGRAM = env('TOKEN_TELEGRAM')

if TOKEN_TELEGRAM:
    BOT = telebot.TeleBot(TOKEN_TELEGRAM)
else:
    BOT = None


@BOT.message_handler(commands=['start'])
def cmd_start(message):
    """Старт диалога с ботом"""
    mainmenu(message)


def mainmenu(message):
    """Главное меню"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_list = []
    keyboard_list.append('Ping private')
    keyboard.add(*keyboard_list, row_width=1)
    BOT.send_message(message.chat.id, 'Вы в главном меню',
                     reply_markup=keyboard)


@BOT.message_handler(content_types=['text'])
def mainmenu_choice(message):
    """Выбор пункта главного меню"""
    choice = message.text
    if choice == 'Ping private':
        if db.send_ping_private():
            BOT.send_message(message.chat.id, 'Отладочное личное сообщение отправлено')
    else:
        BOT.send_message(message.chat.id, 'Неизвестная команда')
        mainmenu(message)


if __name__ == '__main__':
    if TOKEN_TELEGRAM:
        try:
            BOT.infinity_polling()
        except Exception as ex:
            sys.exit()
    else:
        while True:
            time.sleep(1)
