import telebot
from extensions import APIException, Convertor
import traceback
from config import *
 
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username}\nЧтобы начать работу, введи команду в следующем \
формате:\n <имя валюты>  <в какую валюту перевести>  <какую сумму перевести>\n\
Чтобы узнать доступные валюты, введикоманду /values')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)
    

bot.polling(none_stop=True)