import requests
from src.config import Settings

class Chat:
    def __init__(self):
        self.settings = Settings()
        self.chat_endpoint = self.settings.CHAT 

    def send_message(self, bot, message, data):

        chat_id = message.chat.id

        # Verificar autenticación
        if chat_id not in data:
            bot.send_message(chat_id, "Please authenticate first using /start.")
            return

        token = data[chat_id]
        headers = {"Authorization": f"Bearer {token}"}

        bot.send_chat_action(chat_id, "typing")

        response = requests.post(
            self.chat_endpoint, json={"message": message.text}, headers=headers
        )

        if response.status_code == 200:
            bot.send_message(chat_id, response.json().get("message", "No response from server."))
        else:
            bot.send_message(chat_id, "An error occurred while sending the message.")
