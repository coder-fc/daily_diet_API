from database import db
from datetime import datetime


class Snack(db.Model):
    # id (int), name (text), description, date, diet
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diet = db.Column(db.Boolean, default=True)
