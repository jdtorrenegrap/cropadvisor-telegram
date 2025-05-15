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

# Handler para mensajes de texto
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat.send_message(bot, message, auth.data_token)

# Handler para imágenes
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat.send_message(bot, message, auth.data_token)

# Podés agregar más si más adelante soportás audio, video, etc.

bot.polling(none_stop=True, interval=0)