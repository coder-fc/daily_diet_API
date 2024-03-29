from database import db


class Snack(db.Model):
    # id (int), snackname (text), description, date, diet
    id = db.Column(db.Integer, primary_key=True)
