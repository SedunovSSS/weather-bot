import requests
from telebot import TeleBot
from googletrans import Translator
TOKEN = 'YOUR BOT TOKEN'
bot = TeleBot(TOKEN)

translator = Translator()

key = 'YOUR KEY openweathermap.org'
lang = ''


@bot.message_handler(content_types=['text'])
def start(message):
    global lang
    if message.text == '/start':
        lang = message.from_user.language_code
        bot.send_message(message.from_user.id, translator.translate('Write City', dest=lang).text)
        bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types=['text'])
def get_city(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, translator.translate('Write City', dest=lang).text)
        bot.register_next_step_handler(message, get_city)
    else:
        try:
            city = message.text
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang={lang}&appid={key}&units=metric'
            data = requests.get(url).json()
            msg = f'''{translator.translate('Weather', dest=lang).text}: {data['weather'][0]['description']}
{translator.translate('Temperature', dest=lang).text}: {str(data['main']['temp'])}°C
{translator.translate('Feels like', dest=lang).text}: {str(data['main']['feels_like'])}°C
{translator.translate('Pressure', dest=lang).text}: {str(data['main']['pressure'])} Pa
{translator.translate('Wind speed', dest=lang).text}: {str(data['wind']['speed'])} М/с
{translator.translate('Direction of the wind', dest=lang).text}: {str(data['wind']['deg'])}°
{translator.translate('Cloudiness', dest=lang).text}: {str(data['clouds']['all'])}%
            '''
            bot.send_message(message.from_user.id, msg)
        except:
            bot.send_message(message.from_user.id, translator.translate('Error! City not found.', dest=lang).text)
        bot.register_next_step_handler(message, get_city)


bot.infinity_polling()
