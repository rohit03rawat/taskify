import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://todo_user:password123@localhost:5432/todo_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
