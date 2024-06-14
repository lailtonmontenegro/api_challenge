from flask import Blueprint, request, jsonify, current_app
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import table
import sqlite3

auth_bp = Blueprint('auth', __name__)

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({"error 401": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({"error 401": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error 401": "Invalid token!"}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"error 401": "Could not verify"}), 401

    user = table.get_user(auth.username)
    if not user or not check_password_hash(user[1], auth.password):
        return jsonify({"error 401": "Could not verify"}), 401

    token = generate_token(auth.username)
    return jsonify({"token": token})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error 400": "Missing username or password"}), 400

    password_hash = generate_password_hash(password)
    try:
        table.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return jsonify({"error 400": "User already exists"}), 400

    return jsonify({"message": "User created successfully"}), 201

