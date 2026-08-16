from flask import Blueprint, request, jsonify
from database import connection

auth_bp = Blueprint("auth", __name__)


# ----------------------------
# Register API
# ----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    cursor = connection.cursor()

    sql = """
    INSERT INTO users
    (name, email, password, role)
    VALUES
    (%s, %s, %s, 'employee')
    """

    cursor.execute(sql, (name, email, password))
    connection.commit()

    return jsonify({
        "message": "Registration Successful"
    })


# ----------------------------
# Login API
# ----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    cursor = connection.cursor()

    sql = """
    SELECT *
    FROM users
    WHERE email=%s
    AND password=%s
    """

    cursor.execute(sql, (email, password))

    user = cursor.fetchone()

    if user:
        return jsonify({
            "message": "Login Successful",
            "role": user["role"],
            "user_id": user["id"]
        })

    return jsonify({
        "message": "Invalid Credentials"
    }), 401