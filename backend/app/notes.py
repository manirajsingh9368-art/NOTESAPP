from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db_connection

notes_bp = Blueprint("notes", __name__)

# CREATE NOTES
@notes_bp.route("/notes", methods=["POST"])
@jwt_required()
def create_notes():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON required"}), 400

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "title and content required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes_table(user_id, title, content, created_at)
        VALUES (?, ?, ?, datetime('now'))
        """,
        (user_id, title, content)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note created"}), 201


# GET ALL NOTES
@notes_bp.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():

    user_id = int(get_jwt_identity())

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, content, created_at, updated_at
        FROM notes_table
        WHERE user_id = ?
        AND is_deleted = 0
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    notes = [dict(row) for row in rows]

    return jsonify(notes), 200


# UPDATE NOTES
@notes_bp.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):

    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON required"}), 400

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notes_table
        SET title = ?, content = ?, updated_at = datetime('now')
        WHERE id = ? AND user_id = ? AND is_deleted = 0
        """,
        (title, content, note_id, user_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Note not found"}), 404

    conn.close()

    return jsonify({"message": "Note updated successfully"}), 200


# DELETE NOTES (SOFT DELETE)
@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):

    user_id = int(get_jwt_identity())

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notes_table
        SET is_deleted = 1,
        updated_at = datetime('now')
        WHERE id = ? AND user_id = ? AND is_deleted = 0
        """,
        (note_id, user_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Note not found"}), 404

    conn.close()

    return jsonify({"message": "Note deleted successfully"}), 200