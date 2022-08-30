import os
import sys
import time as tim
import ctypes
import platform
import datetime

import requests
import telebot
import calendar
import wikipedia
import webbrowser
import subprocess

import pyautogui as pag

from config import *
from telebot import types
from datetime import time, date
from weekday import *
from weather import *
from config import settings

bot = telebot.TeleBot(token=settings.TOKEN, parse_mode='HTML')
wikipedia.set_lang(prefix='ru')


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    key_volume_down = types.KeyboardButton('🔉')
    key_volume_up = types.KeyboardButton('🔊')

    key_play_right = types.KeyboardButton('⏩')
    key_play_left = types.KeyboardButton('⏪')

    key_openurl = types.KeyboardButton('🔗 Открыть ссылку')
    key_message_to_screen = types.KeyboardButton('📨 Сообщение на экран')
    key_input = types.KeyboardButton("👥 Собщение с ответом")
    key_wallpaper = types.KeyboardButton('🏞 Сменить обои')
    key_wiki = types.KeyboardButton('ℹ️ Поиск на WIKIPEDIA')
    key_screenshot = types.KeyboardButton('📷 Скриншот')
    key_offpc = types.KeyboardButton('🚫 Выключить ПК')
    key_infopc = types.KeyboardButton('🖥 Информация')

    key_menu_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(key_volume_up, key_volume_down,
                                                                                      key_play_left, key_play_right,
                                                                                      key_openurl,
                                                                                      key_message_to_screen, key_input,
                                                                                      key_wallpaper, key_wiki,
                                                                                      key_screenshot,
                                                                                      key_offpc, key_infopc)
    bot.send_message(message.from_user.id,
                     f"<b>🖥 Добро пожаловать в PCCONTROL!\n\n🌞Сегодня {weekday}, {CurrentDay} {CurrentMonth}\n\n🌧Температура в {place}e {t1}, {dt}</b>",
                     reply_markup=key_menu_reply)


@bot.message_handler(content_types=['text'])
def key_volume_down(message: types.Message):
    if message.text == '🔉':
        pag.press('volumedown', 10)
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '🔊':
        pag.press('volumeup', 10)
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '⏩':
        pag.press('right')
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '⏪':
        pag.press('left')
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '🔗 Открыть ссылку':
        msg = bot.send_message(message.from_user.id, "<b>Введите текст ссылки:</b>")
        bot.register_next_step_handler(msg, opennexturl)
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '📨 Сообщение на экран':
        mesg = bot.send_message(message.from_user.id, "<b>Введите текст сообщения:</b>")
        bot.register_next_step_handler(mesg, send_message_to_user)
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '👥 Собщение с ответом':
        meesg = bot.send_message(message.from_user.id, "<b>Введите сообщение на которые хотите получить ответ</b>")
        bot.register_next_step_handler(meesg, message_with_answer)

    if message.text == '🏞 Сменить обои':
        msg = bot.send_message(message.chat.id, "<b>Отправьте картинку:</b>")
        bot.register_next_step_handler(msg, set_wallpaper)

    if message.text == 'ℹ️ Поиск на WIKIPEDIA':
        meesg = bot.send_message(message.from_user.id, '<b>Что хотите найти?</b>')
        bot.register_next_step_handler(meesg, wiki_search)
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '📷 Скриншот':
        filename = f"1.jpg"
        pag.screenshot(filename)

        with open(filename, "rb") as img:
            bot.send_photo(message.from_user.id, img)
        os.remove(filename)

    if message.text == '🚫 Выключить ПК':
        meeesg = bot.send_message(message.from_user.id, '<b>Через какое время хотите выключить ПК? (В секундах)</b>')
        bot.register_next_step_handler(meeesg, off_pc_of_timer)
        bot.delete_message(message.chat.id, message.message_id)

    if message.text == '🖥 Информация':
        response = requests.get('http://jsonip.com/').json()
        bot.send_message(message.from_user.id,
                         f"<b>🤖Ваш IP: {response['ip']} \n\nСистема: {platform.system()}{platform.release()}\nИмя ПК: {platform.node()}\nПроцессор: {platform.processor()}</b>")
        bot.delete_message(message.chat.id, message.message_id)


def opennexturl(message: types.Message):
    webbrowser.open(message.text, new=2, autoraise=True)
    bot.send_message(message.from_user.id, f"<b>Ссылка: {message.text} успешно открыта!</b>")
    bot.delete_message(message.chat.id, message.message_id)


def send_message_to_user(message: types.Message):
    pag.alert(message.text, "Сообщение")
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.from_user.id, f'<b>Сообщение: "{message.text}" успешно отправленно!</b>')


def message_with_answer(message: types.Message):
    try:
        answer = pag.prompt(message.text, "~")
        bot.send_message(message.chat.id, f"<b>Пользователь ответил: {answer}</b>")
    except Exception:
        bot.send_message(message.chat.id, "Что-то пошло не так...")


def set_wallpaper(message: types.Message):
    file = message.photo[-1].file_id
    file = bot.get_file(file)

    download_file = bot.download_file(file.file_path)
    with open(f"screen.jpg", "wb") as img:
        img.write(download_file)

    path = os.path.abspath("image.jpg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def wiki_search(message: types.Message):
    try:
        bot.send_message(message.from_user.id, wikipedia.summary(message.text))
    except Exception:
        bot.send_message(message.from_user.id, "<b>🚫 Данная статья на википедии не была найденна</b>")


def off_pc_of_timer(message: types.Message):
    pag.alert(f'Ваш ПК будет выключен через "{message.text}"!')
    tim.sleep(int(message.text))
    os.system('shutdown -s')


if __name__ == '__main__':
    bot.polling()
