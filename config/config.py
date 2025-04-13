from dotenv import load_dotenv
import os
load_dotenv()
class Config:
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    ALLOWED_USER_IDS = list(map(int, os.getenv('ALLOWED_USER_IDS', '').split(','))) 
    SSH_HOST = os.getenv('SSH_HOST')
    SSH_PORT = int(os.getenv('SSH_PORT', 22))
    SSH_USERNAME = os.getenv('SSH_USERNAME')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    LOCAL_BIND_ADDRESS = os.getenv('LOCAL_BIND_ADDRESS', 'localhost')
    LOCAL_BIND_PORT = int(os.getenv('LOCAL_BIND_PORT', 3307))