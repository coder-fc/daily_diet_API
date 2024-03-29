from database import db
from datetime import datetime
import pytz

fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')


class Snack(db.Model):
    # id (int), name (text), description, date, diet
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300))
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.now(fuso_horario_brasilia))
    diet = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
