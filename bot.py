import telebot
from telebot import types
import pyowm
import config
import logging
import json
import collections
from pyowm.utils import timeformatutils
from datetime import datetime, date, timedelta
import math

bot = telebot.TeleBot(config.telegram_token)
owm = pyowm.OWM(config.owm_token, language = 'ru')

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands = ['start'])
def start(message):
    bot.reply_to(message, 'Здравствуйте!')
    keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    keyboard.one_time_keyboard = True 
    btn_now = types.KeyboardButton(text = 'Сейчас')
    btn_tom = types.KeyboardButton(text = 'Завтра')
    keyboard.add(btn_now, btn_tom)
    bot.send_message(message.chat.id, "Вы хотели бы узнать погоду на завтра, или на сегодня?", reply_markup = keyboard)


@bot.message_handler(regexp = "Сейчас")
def now(message):
    w = owm.weather_at_place('Saint Petersburg').get_weather()
    h = w.get_temperature(unit = 'celsius')['temp']
    logger.info('Получил - ', w.to_JSON())
    resp = collections.OrderedDict({
        'Время' : w.get_reference_time(timeformat = 'date'),
        'Статус': w.get_detailed_status(),
        'Температура:': '+' + str(round(h)) if round(h) > 0 else '-' + str(round(h)),
        'Дождь?': 'Да!' if w.get_rain() else 'Нет!',
        'Снег?': 'Да!' if w.get_snow() else 'Нет!',
        'Скорость ветра' : str(w.get_wind(unit = 'meters_sec')['speed']) + ' ' + 'м/с',
        'Рассвет': w.get_sunrise_time(timeformat = 'iso'),
        'Закат': w.get_sunset_time(timeformat = 'iso')
    })
    bot.send_message(chat_id = message.chat.id, text = 'Погода в Санкт-Петербурге на сегодня')
    for key, value in resp.items():
        bot.send_message(chat_id = message.chat.id, text = '{0} {1}'.format(key, value))



@bot.message_handler(regexp = "Завтра")
def tomorrow(message):
    bot.send_message(chat_id = message.chat.id, text='К сожалению для такой функции требуется платная подписка на OWM!')


if __name__ == '__main__':
    bot.polling(none_stop = True) 