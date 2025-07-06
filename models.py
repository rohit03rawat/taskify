from flask_sqlalchemy import SQLAlchemy  # type: ignore # 1️⃣ We import SQLAlchemy

db = SQLAlchemy()  # 2️⃣ Create an object that manages all DB stuff

# 3️⃣ Define a User table as a Python class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto ID
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(128), nullable=False)  # Store password

