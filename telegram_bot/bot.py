import telebot
from django.conf import settings as conf_settings
from telebot import types
import sys

if conf_settings.TOKEN_TELEGRAM:
    BOT = telebot.TeleBot(conf_settings.TOKEN_TELEGRAM)
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
    keyboard_list.append('Отправить')
    keyboard.add(*keyboard_list, row_width=1)
    BOT.send_message(message.chat.id, 'Вы в главном меню',
                     reply_markup=keyboard)


@BOT.message_handler(content_types=['text'])
def mainmenu_choice(message):
    """Выбор пункта главного меню"""
    choice = message.text
    if choice == 'Отправить':
        BOT.send_message(message.chat.id, 'Выбран пункт меню')
    else:
        BOT.send_message(message.chat.id, 'Неизвестная команда')
        mainmenu(message)

if __name__ == '__main__':
    print('bot started!!!')
    try:
        BOT.infinity_polling()
    except Exception as ex:
        sys.exit()
