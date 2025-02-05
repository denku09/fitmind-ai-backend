from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

routes = Blueprint("routes", __name__)

@routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Eksik bilgiler"}), 400

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Kullanıcı oluşturuldu!"}), 201

@routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Geçersiz kimlik bilgileri"}), 401

@routes.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Hoş geldin kullanıcı {user_id}"}), 200
