

# # from flask_jwt_extended import jwt_required,get_jwt_identity 
# # from flask_jwt_extended import JWTManager
# # from flask_jwt_extended import create_access_token,set_access_cookies
# # from werkzeug.security import check_password_hash
# # from werkzeug.security import generate_password_hash
# # from flask import Flask, jsonify, request
# # from datetime import timedelta
# # import sqlite3
# # import os


# # app=Flask(__name__)

# # app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"
# # app.config["JWT_ACCESS_TOKEN_EXPIRES"]= timedelta(minutes=30)

# # app.config["JWT_TOKEN_LOCATION"]=["cookies"]
# # app.config["JWT_COOKIE_SECURE"]= False

# # app.config["JWT_COOKIE_CSRF_PROTECT"] = False

# # jwt = JWTManager(app)



# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # DB_PATH = os.path.join(BASE_DIR, "Notes_v14.db")

# # def get_db_connection():
# #     conn = sqlite3.connect(DB_PATH)
# #     conn.row_factory = sqlite3.Row   #(by this rows will behave like dictionaries)
# #     return conn

# # def init_users_table():
# #     conn=get_db_connection()
# #     cursor=conn.cursor()

# #     cursor.execute("""
# #         CREATE TABLE IF NOT EXISTS users(
# #                    id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                    username TEXT UNIQUE NOT NULL,
# #                    password TEXT NOT NULL,
# #                    created_at TEXT NOT NULL)""")

# # @app.route("/auth/login", methods=["POST"])
# # def user_login():
# #     data = request.get_json()

# #     if not data:
# #         return jsonify({"error":"JSON body required"})
    
# #     username=data.get("username","").strip()
# #     password=data.get("password","").strip()

# #     if not username:
# #         return jsonify({"error":"Username is required"})
    
# #     if not password:
# #         return jsonify({"error":"Password is required"})
    
# #     conn= get_db_connection()
# #     cursor=conn.cursor()

# #     cursor.execute("""
# #         SELECT id, username, password 
# #         FROM users
# #         WHERE username = ?
# #         """,(username,))
    
# #     user =cursor.fetchone()

# #     if not user:
# #         return jsonify({"error":"Login failed"})







# # @app.route("/notes", methods = ["GET"])
# # @jwt_required()
# # def get_notes():
    
# #     user_id = get_jwt_identity()

# #     if not user_id:
# #         return jsonify({"error":"Unauthorized"})

    
# #     page = request.args.get("page", default=1, type=int)
# #     limit = request.args.get("limit", default =5, type=int)

# #     if page <1:
# #         page=1
# #     if limit <1:
# #         limit=5
# #     print("PAGE:",page)
# #     print("LIMIT:", limit)


# #     search = request.args.get("search")

# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     if search :
# #         cursor.execute("""
# #             SELECT id, title, content, created_at, updated_at
# #                        FROM notes_table
# #                        WHERE user_id = ? 
# #                        AND is_deleted = 0 
# #                        AND (title LIKE ? OR content LIKE ?)
# #                        ORDER BY COALESCE(updated_at, created_at)
# #                        DESC
# #                        """,(user_id, f"%{search}%", f"%{search}%"))
# #     else:
# #         offset = (page - 1) * limit 
# #         cursor.execute("""SELECT id, title, content, created_at, updated_at
# #                      FROM notes_table
# #                      WHERE user_id = ?
# #                      AND is_deleted = 0
# #                      ORDER BY COALESCE(updated_at, created_at) DESC
# #                      LIMIT ? OFFSET ?
# #                      """, (user_id, limit, offset))
# #     rows = cursor.fetchall()
# #     conn.close()

# #     notes=[]
# #     for row in rows:
# #             notes.append({
# #                 "id": row["id"],
# #                 "title": row["title"],
# #                 "content": row["content"],
# #                 "created_at": row["created_at"],
# #                 "updated_at": row["updated_at"]
# #             })
# #     return jsonify({
# #         "page": page,
# #         "limit": limit,
# #         "count": len(notes),
# #         "notes": notes
# #     })


# # @app.route("/notes/<int:note_id>", methods = ["GET"])
# # @jwt_required()
# # def get_note(note_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     cursor.execute("""
# #         SELECT id, title, content, created_at, updated_at
# #                    FROM notes_table
# #                    WHERE id = ? AND is_deleted = 0""",
# #                    (note_id,))


# #     row = cursor.fetchone()
# #     conn.close()

# #     if row is None:
# #         return jsonify({"error":"Notes not found"}), 404
    
# #     note = {
# #         "id":row["id"],
# #         "title":row["title"],
# #         "content":row["content"],
# #         "created_at":row["created_at"],
# #         "updated_at": row["updated_at"]
# #     }
    
# #     return jsonify(note)

# # @app.route("/notes", methods = ["POST"])
# # @jwt_required()
# # def create_notes():
# #     data = request.get_json()

# #     user_id = get_jwt_identity()

# #     if not user_id:
# #         return jsonify({"error":"Unauthorized"}), 401

# #     if not data:
# #         return jsonify({"error":"JSON body required"}), 400
    
# #     title = data.get("title","").strip()
# #     content = data.get("content","").strip()

# #     if not title:
# #         return jsonify({"error":"Title is required"}), 400
    
# #     if not content:
# #         return jsonify({"error":"Content is required"}), 400
    
# #     conn = get_db_connection()
# #     cursor = conn.cursor()

# #     cursor.execute("""INSERT INTO notes_table (user_id,title, content, created_at)
# #                    VALUES (?, ?, datetime('now'))""", 
# #                    (user_id,title, content)
# #                    )
   
# #     conn.commit()
# #     conn.close()

# #     return jsonify({"message":"Note created successfully"}), 201


# # @app.route("/notes/<int:note_id>", methods=["PUT"])
# # @jwt_required()
# # def update_note(note_id):
# #     user_id =get_jwt_identity()

# #     if not user_id:
# #         return jsonify({"error":"Unauthorized"})
# #     data = request.get_json()

# #     if not data:
# #         return jsonify({"error":"JSON body required"}), 400
    
# #     title=data.get("title","").strip()
# #     content = data.get("content","").strip()

# #     if not title or not content:
# #         return jsonify({"error":"Title and content is required"}), 400

# #     conn = get_db_connection()
# #     cursor=conn.cursor()

# #     cursor.execute("""
# #         UPDATE notes_table
# #         SET title = ?, content = ?, updated_at = datetime('now')
# #         WHERE  user_id = ? 
# #         AND id = ? 
# #         AND is_deleted = 0
# #         """,(user_id, title, content, note_id))

# #     conn.commit()
# #     affected = cursor.rowcount
# #     conn.close()

# #     if affected == 0 :
# #         return jsonify({"error":"No note found"}), 404

# #     return jsonify({"message":"Note updated successfully"}) 



# # @app.route("/notes/<int:note_id>", methods=["DELETE"])
# # @jwt_required()
# # def delete_note(note_id):
# #     user_id = get_jwt_identity()

# #     if not user_id():
# #         return jsonify({"error":"Unauthorized"})

# #     conn=get_db_connection()
# #     cursor=conn.cursor()

# #     cursor.execute("""
# #         UPDATE notes_table
# #         SET is_deleted=1
# #         Where AND user_id = ? 
# #         AND id = ? 
# #         AND is_deleted=0
# #         """, (user_id, note_id,))
    
# #     conn.commit()
# #     affected = cursor.rowcount
# #     conn.close()

# #     if affected == 0 :
# #         return jsonify({"error":"Note not found"}), 404
    
# #     return jsonify({"Note deleted successfully"})

# # @app.route("/auth/register", methods=["POST"])
# # @jwt_required()
# # def register_user():
# #     data = request.get_json()

# #     if not data:
# #         return jsonify({"error":"JSON body required"}), 400
    
# #     username= data.get("username","").strip()
# #     password= data.get("password","").strip()

# #     if not username:
# #         return jsonify({"error":"Username is required"}), 400
    
# #     if not password:
# #         return jsonify({"error":"Password is required"}), 400
    
# #     hashed_password = generate_password_hash(password)


# #     conn=get_db_connection()
# #     cursor=conn.cursor()

# #     try:
# #         cursor.execute("""
# #             INSERT INTO users (username, password, created_at)
# #             VALUES (?, ?, datetime('now'))
# #             """,(username, hashed_password))
# #         conn.commit()
# #     except sqlite3.IntegrityError:
# #         conn.close()
# #         return jsonify({"error":"Username already exists"}), 409
    
# #     conn.close()

# #     return jsonify({"message":"User register successfully"}), 201



    
        
    









# # if __name__ == "__main__":
# #     init_users_table()
# #     app.run(debug=True)










































































# # # app.route("/login", methods=["POST"])
# # # def login():
# # #     data = request.get_json()

# # #     if not data:
# # #         return jsonify({"error":"JSON body required"}), 400
    
# # #     username = data.get("username","").strip()
# # #     password = data.get("password","").strip()

# # #     if not username or not password:
# # #         return jsonify({"error":"Username and Password are required"}), 400
    
# # #     conn = get_db_connection()
# # #     cursor = conn.cursor()

# # #     cursor.execute("""
# # #         SELECT id, password FROM users WHERE username = ?""",(username))
    
# # #     user=cursor.fetchone()
# # #     conn.close()

# # #     if not user:
# # #         return jsonify({"error":"Invalid credentials"}), 401
    
# # #     if not check_password_hash(user["password"],password):
# # #         return jsonify({"error":"Invalid Credentials"}), 401
    
# # #     access_token = create_access_token(identity=user["id"])

# # #     response = jsonify({"message":"login successfull"})

# # #     set_access_cookies(response, access_token)
# # #     return response, 200























# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from .db import get_db_connection

# notes_bp = Blueprint("notes", __name__)

# # CREATE NOTES
# @notes_bp.route("/notes", methods=["POST"])
# @jwt_required()
# def create_notes():

#     user_id = int(get_jwt_identity())
#     data = request.get_json()

#     if not data:
#         return jsonify({"error": "JSON required"}), 400

#     title = data.get("title")
#     content = data.get("content")

#     if not title or not content:
#         return jsonify({"error": "title and content required"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO notes_table(user_id, title, content, created_at)
#         VALUES (?, ?, ?, datetime('now'))
#         """,
#         (user_id, title, content)
#     )

#     conn.commit()
#     conn.close()

#     return jsonify({"message": "Note created"}), 201


# # GET ALL NOTES
# @notes_bp.route("/notes", methods=["GET"])
# @jwt_required()
# def get_notes():

#     user_id = int(get_jwt_identity())

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT id, title, content, created_at, updated_at
#         FROM notes_table
#         WHERE user_id = ?
#         AND is_deleted = 0
#         ORDER BY created_at DESC
#         """,
#         (user_id,)
#     )

#     rows = cursor.fetchall()
#     conn.close()

#     notes = [dict(row) for row in rows]

#     return jsonify(notes), 200


# # UPDATE NOTES
# @notes_bp.route("/notes/<int:note_id>", methods=["PUT"])
# @jwt_required()
# def update_note(note_id):

#     user_id = int(get_jwt_identity())
#     data = request.get_json()

#     if not data:
#         return jsonify({"error": "JSON required"}), 400

#     title = data.get("title", "").strip()
#     content = data.get("content", "").strip()

#     if not title or not content:
#         return jsonify({"error": "Title and content required"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         UPDATE notes_table
#         SET title = ?, content = ?, updated_at = datetime('now')
#         WHERE id = ? AND user_id = ? AND is_deleted = 0
#         """,
#         (title, content, note_id, user_id)
#     )

#     conn.commit()

#     if cursor.rowcount == 0:
#         conn.close()
#         return jsonify({"error": "Note not found"}), 404

#     conn.close()

#     return jsonify({"message": "Note updated successfully"}), 200


# # DELETE NOTES (SOFT DELETE)
# @notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
# @jwt_required()
# def delete_note(note_id):

#     user_id = int(get_jwt_identity())

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         UPDATE notes_table
#         SET is_deleted = 1,
#         updated_at = datetime('now')
#         WHERE id = ? AND user_id = ? AND is_deleted = 0
#         """,
#         (note_id, user_id)
#     )

#     conn.commit()

#     if cursor.rowcount == 0:
#         conn.close()
#         return jsonify({"error": "Note not found"}), 404

#     conn.close()

#     return jsonify({"message": "Note deleted successfully"}), 200