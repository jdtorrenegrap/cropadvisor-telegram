from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    LOGIN = os.getenv("LOGIN")
    CHAT = os.getenv("CHAT")
    TOKEN = os.getenv("TOKEN")