from database import db
from datetime import datetime


class Snack(db.Model):
    # id (int), name (text), description, date, diet
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    diet = db.Column(db.Boolean, default=True)
