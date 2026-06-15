import joblib
import os
import sys

from werkzeug.utils import secure_filename

sys.path.append("../genai")

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from gemini_summary import generate_ai_summary
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import connection

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

print("Upload Folder:", app.config["UPLOAD_FOLDER"])

model = joblib.load(
    "../ml/reimbursement_model.pkl"
)
# ----------------------------
# Home API
# ----------------------------
@app.route("/")
def home():
    return "AI Reimbursement Management System"


# ----------------------------
# Register API
# ----------------------------
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    cursor = connection.cursor()

    sql = """
    INSERT INTO users
    (name,email,password,role)
    VALUES
    (%s,%s,%s,'employee')
    """

    cursor.execute(
        sql,
        (name, email, password)
    )

    connection.commit()

    return jsonify({
        "message": "Registration Successful"
    })


# ----------------------------
# Login API
# ----------------------------
@app.route("/login", methods=["POST"])
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

    cursor.execute(
        sql,
        (email, password)
    )

    user = cursor.fetchone()

    if user:

        return jsonify({
            "message": "Login Successful",
            "role": user["role"],
            "user_id": user["id"]
        })

    return jsonify({
        "message": "Invalid Credentials"
    })

# ----------------------------
# Submit Reimbursement API
# ----------------------------
@app.route("/submit", methods=["POST"])
def submit_reimbursement():

    user_id = request.form["user_id"]

    amount = request.form["expense_amount"]

    category = request.form["category"]

    description = request.form["description"]

    bill = request.files.get("bill")

    filename = ""

    if bill:

        filename = secure_filename(
            bill.filename
        )

        bill.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

    cursor = connection.cursor()

    sql = """
    INSERT INTO reimbursements
    (
        user_id,
        expense_amount,
        category,
        description,
        bill_file,
        status
    )
    VALUES
    (
        %s,%s,%s,%s,%s,'Pending'
    )
    """

    cursor.execute(
        sql,
        (
            user_id,
            amount,
            category,
            description,
            filename
        )
    )

    connection.commit()

    return jsonify({
        "message": "Reimbursement Submitted Successfully"
    })
# ----------------------------
# View Uploaded Bill
# ----------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )    

# ----------------------------
# View Reimbursements API
# ----------------------------
@app.route("/reimbursements", methods=["GET"])
def get_reimbursements():

    cursor = connection.cursor()

    sql = """
    SELECT *
    FROM reimbursements
    """

    cursor.execute(sql)

    data = cursor.fetchall()

    return jsonify(data)


# ----------------------------
# Employee History API
# ----------------------------
@app.route("/history/<int:user_id>", methods=["GET"])
def history(user_id):

    cursor = connection.cursor()

    sql = """
    SELECT *
    FROM reimbursements
    WHERE user_id=%s
    """

    cursor.execute(sql, (user_id,))

    data = cursor.fetchall()

    return jsonify(data)

# ----------------------------
# Approve Reimbursement
# ----------------------------
@app.route("/approve/<int:id>", methods=["POST"])
def approve(id):

    cursor = connection.cursor()

    sql = """
    UPDATE reimbursements
    SET status='Approved'
    WHERE id=%s
    """

    cursor.execute(sql, (id,))
    connection.commit()

    return jsonify({
        "message": "Approved Successfully"
    })
    # ----------------------------
# Reject Reimbursement
# ----------------------------
@app.route("/reject/<int:id>", methods=["POST"])
def reject(id):

    cursor = connection.cursor()

    sql = """
    UPDATE reimbursements
    SET status='Rejected'
    WHERE id=%s
    """

    cursor.execute(sql, (id,))
    connection.commit()

    return jsonify({
        "message": "Rejected Successfully"
    })
    
    
    # ----------------------------
# ML Prediction API
# ----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    amount = float(data["expense_amount"])
    category = int(data["category"])
    submission_day = int(data["submission_day"])
    history_score = int(data["history_score"])
    bill_available = int(data["bill_available"])

    prediction = model.predict([
        [
            amount,
            category,
            submission_day,
            history_score,
            bill_available
        ]
    ])

    probability = model.predict_proba([
        [
            amount,
            category,
            submission_day,
            history_score,
            bill_available
        ]
    ])

    confidence = round(
        max(probability[0]) * 100,
        2
    )

    return jsonify({
        "prediction": int(prediction[0]),
        "confidence": confidence
    })
    
# ----------------------------
# AI Summary API
# ----------------------------
@app.route("/summary", methods=["POST"])
def summary():

    data = request.json

    amount = data["amount"]
    category = data["category"]
    description = data["description"]

    result = generate_ai_summary(
        amount,
        category,
        description
    )

    return jsonify({
        "summary": result
    })
# ----------------------------
# Employee Dashboard API
# ----------------------------
@app.route(
    "/employee-dashboard/<int:user_id>",
    methods=["GET"]
)
def employee_dashboard(user_id):

    cursor = connection.cursor()

    # Total Claims
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM reimbursements
        WHERE user_id=%s
        """,
        (user_id,)
    )

    total = cursor.fetchone()["total"]

    # Approved
    cursor.execute(
        """
        SELECT COUNT(*) AS approved
        FROM reimbursements
        WHERE user_id=%s
        AND status='Approved'
        """,
        (user_id,)
    )

    approved = cursor.fetchone()["approved"]

    # Pending
    cursor.execute(
        """
        SELECT COUNT(*) AS pending
        FROM reimbursements
        WHERE user_id=%s
        AND status='Pending'
        """,
        (user_id,)
    )

    pending = cursor.fetchone()["pending"]

    # Rejected
    cursor.execute(
        """
        SELECT COUNT(*) AS rejected
        FROM reimbursements
        WHERE user_id=%s
        AND status='Rejected'
        """,
        (user_id,)
    )

    rejected = cursor.fetchone()["rejected"]

    return jsonify({
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    })
# ----------------------------
# Admin Dashboard Statistics
# ----------------------------
@app.route(
    "/admin-stats",
    methods=["GET"]
)
def admin_stats():

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM reimbursements
        """
    )

    total =cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS approved
        FROM reimbursements
        WHERE status='Approved'
        """
    )

    approved =cursor.fetchone()["approved"]

    cursor.execute(
        """
        SELECT COUNT(*) AS pending
        FROM reimbursements
        WHERE status='Pending'
        """
    )

    pending =cursor.fetchone()["pending"]

    cursor.execute(
        """
        SELECT COUNT(*) AS rejected
        FROM reimbursements
        WHERE status='Rejected'
        """
    )

    rejected =cursor.fetchone()["rejected"]

    return jsonify({
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    })   
    # ----------------------------
# PDF Report API
# ----------------------------
@app.route("/generate-report")
def generate_report():

    pdf_file = "reimbursement_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Reimbursement Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,20)
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM reimbursements
        """
    )

    data = cursor.fetchall()

    for item in data:

        text = f"""
        ID: {item['id']}<br/>
        Amount: ₹{item['expense_amount']}<br/>
        Category: {item['category']}<br/>
        Status: {item['status']}<br/>
        """

        content.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1,10)
        )

    doc.build(content)

    return send_from_directory(
        ".",
        pdf_file,
        as_attachment=True
    ) 
# ----------------------------
# Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)