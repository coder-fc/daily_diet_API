from flask import Flask, request, jsonify
from models.snack import Snack
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/diet-crud'

db.init_app(app)


@app.route('/create_snack', methods=["POST"])
def create_snack():
    data = request.json
    username = data.get("username")
    name = data.get("name")
    description = data.get("description")
    date = data.get("date")

    if username and name:
        snack = Snack(username=username, name=name,
                      description=description, date=date, diet=True)
        db.session.add(snack)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso!!!"})

    return jsonify({"message": "Erro ao cadastrar refeição"}), 400


if __name__ == '__main__':
    app.run(debug=True)
