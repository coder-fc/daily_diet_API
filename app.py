import bcrypt
from flask import Flask, request, jsonify
from models.snack import Snack
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/diet-crud'

login_manager = LoginManager()
db.init_app(app)

login_manager.init_app(app)

# view login
login_manager.login_view = 'login'
# Session <- conexão ativa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"})

    return jsonify({"message": "Credênciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return ({"message": "Logout realizado com sucesso!"})


@app.route('/create_user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400


@app.route('/snack', methods=["POST"])
def create_snack():
    if current_user.is_authenticated:
        data = request.json
        user_id = current_user.id
        name = data.get("name")
        description = data.get("description")
        date = data.get("date")
        diet = data.get("diet")

        if name:
            if date:
                date = datetime.strptime(date, "%d/%m/%Y %H:%M")

            snack = Snack(name=name,
                          description=description, diet=diet, date=date, user_id=user_id)
            db.session.add(snack)
            db.session.commit()
            return jsonify({"message": "Refeição cadastrada com sucesso!!!"})

        return jsonify({"message": "Erro ao cadastrar refeição"}), 400
    else:
        return jsonify({"message": "Usuário não autenticado"}), 401


@app.route('/snack/<int:id_snack>', methods=["PUT"])
@login_required
def update_snack(id_snack):
    data = request.json
    snack = Snack.query.get(id_snack)
    name = data.get("name")
    description = data.get("description")
    date = data.get("date")
    diet = data.get("diet")

    if name is None:
        name = snack.name

    if description is None:
        description = snack.description

    if diet is None:
        diet = snack.diet

    if date:
        date = datetime.strptime(date, "%d/%m/%Y %H:%M")
    else:
        date = snack.date

    if current_user.id != snack.user_id:
        return jsonify({"message": "Não é permitido alterar a refeição de outro usuário!"}), 403
    snack.name = name
    snack.description = description
    snack.date = date
    snack.diet = diet
    db.session.commit()
    return jsonify({"message": "Alteração realizada com sucesso"})


@app.route('/snacks', methods=["GET"])
@login_required
def get_snacks_user():
    user_snacks = Snack.query.filter_by(user_id=current_user.id).all()

    snacks_list = []

    for snack in user_snacks:
        snacks_list.append({
            "id": snack.id,
            "name": snack.name,
            "description": snack.description,
            "date": snack.date.strftime("%d/%m/%Y %H:%M"),
            "diet": snack.diet
        })

    if snacks_list == []:
        return jsonify({"message": "Usuário não possuí refeições cadastradas."})

    return jsonify(snacks_list)


@app.route('/snack/<int:id_snack>', methods=["DELETE"])
@login_required
def delete_snack(id_snack):
    snack = Snack.query.get(id_snack)
    if snack:
        if current_user.id != snack.user_id:
            return jsonify({"message": "Não é permitido deletar a refeição de outro usuário!"}), 403
        db.session.delete(snack)
        db.session.commit()
        return jsonify({"message": f"Refeição {id_snack} deletada com sucesso!"})

    return jsonify({"message": f"Refeição não encontrada!"})


@app.route('/snack/<int:id_snack>', methods=["GET"])
@login_required
def read_snack(id_snack):
    snack = Snack.query.get(id_snack)
    if snack:
        if current_user.id != snack.user_id:
            return jsonify({"message": "Não é permitido visualizar a refeição de outro usuário!"}), 403
        db.session.delete(snack)
        db.session.commit()
        return {
            "name": snack.name,
            "description": snack.description,
            "date": snack.date.strftime("%d/%m/%Y %H:%M"),
            "diet": snack.diet
        }

    return jsonify({"message": f"Refeição não encontrada!"})


if __name__ == '__main__':
    app.run(debug=True)
