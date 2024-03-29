from flask import Flask, request, jsonify
from models.snack import Snack
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/diet-crud'

db.init_app(app)
