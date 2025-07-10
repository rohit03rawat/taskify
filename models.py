from flask_sqlalchemy import SQLAlchemy  # type: ignore # 1️⃣ We import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import Boolean



db = SQLAlchemy()  # 2️⃣ Create an object that manages all DB stuff

# 3️⃣ Define a User table as a Python class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto ID
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(128), nullable=False)  # Store password

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    is_completed = db.Column(db.Boolean, default=False)
