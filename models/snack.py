from database import db


class Snack(db.Model):
    # id (int), name (text), description, date, diet
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300))
    date = db.Column(db.String(10), nullable=False)
    diet = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
