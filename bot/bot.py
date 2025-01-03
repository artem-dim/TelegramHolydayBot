import requests
import datetime
import re
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from settings import telegram_token, api_token

TOKEN = telegram_token


bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Проверить текущую дату'))
keyboard.add(KeyboardButton('О проекте'))


def get_holiday(api_token,country='RU',year='2023',month='01',day='01'):
    params = {
        "api_key": api_token,
        "country": country,
        "year": year,
        "month": month,
        "day": day,
        "type": "national",
    }

    response = requests.get("https://calendarific.com/api/v2/holidays", params=params)

    if response.status_code == 200:
        data = response.json()
        if data['response']['holidays'] == []:
            return('На этот день государственных праздников не запланировано')
        else:
            holiday_name = data["response"]["holidays"][0]["name"]
            return(f"В этот день проводится праздник праздник '{holiday_name}'")
    else:
        print("Ошибка при выполнении запроса")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'Привет, отправь мне дату и страну и я скажу, является ли этот день национальным праздником'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = 'Бот позволяет узнать какой государственный праздник проводится в заданую дату в выбраной стране\n'
    text += 'Для получения сегодняшнего праздника нажми на кнопку, или отправь дату в формате дд.мм.гггг и код страны (Например 01.01.2023 RU).\n'
    text += 'Код страны можно найти здесь: https://calendarific.com/supported-countries.\n'
    text += 'Данные берутся с сайта https://calendarific.com.\n'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='Проверить текущую дату')
def send_today(message):
    today = datetime.date.today()
    result = get_holiday(api_token,year=today.year,month=today.month,day=today.day)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_day(message):
    match = re.fullmatch(r'\d{2}\.\d{2}\.\d{4} [A-Z]{2}', message.text)
    if match:
        date, country = message.text.split(' ')
        date = date.split('.')
        result = get_holiday(api_token,country=country,year=date[2],month=date[1],day=date[0])
    else:
        result = 'Запрос не подходит под поддерживаемый формат дд.мм.гггг и код страны (Например 01.01.2023 RU)'
    bot.send_message(message.chat.id, result, reply_markup=keyboard)


bot.infinity_polling()