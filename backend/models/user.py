from database import connection


def register_user(name, email, password):
    cursor = connection.cursor()

    sql = """
    INSERT INTO users
    (name, email, password, role)
    VALUES
    (%s, %s, %s, 'employee')
    """

    cursor.execute(sql, (name, email, password))
    connection.commit()

    return {
        "message": "Registration Successful"
    }


def login_user(email, password):
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
        return {
            "message": "Login Successful",
            "user_id": user["id"],
            "role": user["role"]
        }

    return {
        "message": "Invalid Credentials"
    }


def get_user(user_id):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (user_id,)
    )

    return cursor.fetchone()


def get_all_users():
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    return cursor.fetchall()