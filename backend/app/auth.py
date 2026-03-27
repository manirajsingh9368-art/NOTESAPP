from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
           data =request.get_json()

           if not data:
                   return jsonify({"error":"JSON required"}), 400
           
           username = data.get("username")
           password = data.get("password")

           if not username or not password:
                   return jsonify({"error":"Username and Password is required"}), 400
           
           hashed = generate_password_hash(password)

           conn = get_db_connection()
           cursor = conn.cursor()

           try:
                    cursor.execute(
                   """INSERT INTO users (username, password, created_at)
                      VALUES (?, ?, datetime('now')) """,
                      (username, hashed)
                    )

                    conn.commit()
           except Exception:
                   conn.close()
                   return jsonify({"error":"user exists"}), 409
            
           conn.close()
           return jsonify({"message":"registered"})



@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "access_token": access_token
    }), 200
          



@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
        
        response = jsonify({"message":"Logout Successfull"})

        unset_jwt_cookies(response)
        return response, 200

