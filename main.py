import telebot
from src.config import Settings
from src.auth import Auth
from src.chat import Chat

bot = telebot.TeleBot(Settings().TOKEN)
auth = Auth()  
chat = Chat()  

@bot.message_handler(commands=['start'])
def start(message):
    auth.ask_username(bot, message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat.send_message(bot, message, auth.data_token)

bot.polling(none_stop=True, interval=0)
