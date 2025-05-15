import requests
import base64
from src.config import Settings

class Chat:
    def __init__(self):
        self.settings = Settings()
        self.chat_endpoint = self.settings.CHAT

    def send_message(self, bot, message, data):
        chat_id = message.chat.id

        if chat_id not in data:
            bot.send_message(chat_id, "⚠️ Por favor, autentícate primero usando /start.")
            return

        token = data[chat_id]
        headers = {"Authorization": f"Bearer {token}"}

        bot.send_chat_action(chat_id, "typing")

        if message.content_type == "text":
            self._handle_text_message(bot, chat_id, message.text, headers)
        elif message.content_type == "photo":
            self._handle_photo_message(bot, chat_id, message, headers)
        else:
            bot.send_message(chat_id, "⚠️ Solo se aceptan imágenes (photo) o texto.")

    def _handle_text_message(self, bot, chat_id, text, headers):
        """Maneja mensajes de texto."""
        payload = {
            "type": "text",
            "message": text.strip()  # Sanitizar entrada
        }
        self._process_request(bot, chat_id, payload, headers)

    def _handle_photo_message(self, bot, chat_id, message, headers):
        """Maneja mensajes de imagen."""
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            file = bot.download_file(file_info.file_path)

            # Codificar en base64
            base64_str = base64.b64encode(file).decode('utf-8')
            payload = {
                "type": "image",
                "base64": base64_str,
                "message": message.caption.strip() if hasattr(message, "caption") and message.caption else ""
            }
            self._process_request(bot, chat_id, payload, headers)
        except Exception as e:
            bot.send_message(chat_id, "⚠️ Error al procesar la imagen.")
            print(f"Error al procesar la imagen: {str(e)}")

    def _process_request(self, bot, chat_id, payload, headers):
        """Procesa la solicitud al servidor y envía la respuesta en tiempo real."""
        try:
            with requests.post(self.chat_endpoint, json=payload, headers=headers, stream=True) as response:
                if response.status_code == 200:
                    # Enviar las líneas del stream en tiempo real
                    for line in response.iter_lines(decode_unicode=True):
                        if line.strip():  # Ignorar líneas vacías
                            bot.send_message(chat_id, line.strip())
                else:
                    bot.send_message(chat_id, f"❌ Error al consultar el servicio. Código: {response.status_code}")
                    print(f"Error en la API: {response.status_code}, Respuesta: {response.text}")
        except requests.exceptions.RequestException as e:
            bot.send_message(chat_id, f"⚠️ Error de conexión: {str(e)}")
            print(f"Error de conexión: {str(e)}")