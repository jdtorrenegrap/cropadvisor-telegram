import requests
from telebot import types
from src.config import Settings

class Auth:
    def __init__(self):
        self.settings = Settings()
        self.data_token = {}

    def ask_username(self, bot, message):
        
        chat_id = message.chat.id
        bot.send_message(chat_id, "Please enter your username:")
        bot.register_next_step_handler(message, lambda msg: self.ask_password(bot, msg))

    def ask_password(self, bot, message):
       
        chat_id = message.chat.id
        username = message.text

        bot.send_message(chat_id, "Please enter your password:")
        bot.register_next_step_handler(message, lambda msg: self.authenticate(bot, msg, username))

    def authenticate(self, bot, message, username):
        
        chat_id = message.chat.id
        password = message.text

        response = requests.post(
            self.settings.LOGIN,
            data={"grant_type": "password", "username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            token = response.json().get("access_token")  
            self.data_token[chat_id] = token 
            bot.send_message(chat_id, "Authentication successful! You can now chat.")
        else:
            bot.send_message(chat_id, "Authentication failed. Please try again.")
            self.ask_username(bot, message) 
