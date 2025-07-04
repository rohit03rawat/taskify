import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/mydb')
