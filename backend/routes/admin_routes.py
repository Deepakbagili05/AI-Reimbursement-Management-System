from flask import Blueprint, jsonify, send_from_directory
from database import connection
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

admin_bp = Blueprint("admin", __name__)


# View All Reimbursements
@admin_bp.route("/reimbursements", methods=["GET"])
def get_reimbursements():

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM reimbursements")

    data = cursor.fetchall()

    return jsonify(data)


# Approve Reimbursement
@admin_bp.route("/approve/<int:id>", methods=["POST"])
def approve(id):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE reimbursements
        SET status='Approved'
        WHERE id=%s
        """,
        (id,)
    )

    connection.commit()

    return jsonify({
        "message": "Approved Successfully"
    })


# Reject Reimbursement
@admin_bp.route("/reject/<int:id>", methods=["POST"])
def reject(id):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE reimbursements
        SET status='Rejected'
        WHERE id=%s
        """,
        (id,)
    )

    connection.commit()

    return jsonify({
        "message": "Rejected Successfully"
    })


# Admin Dashboard Statistics
@admin_bp.route("/admin-stats", methods=["GET"])
def admin_stats():

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS total FROM reimbursements"
    )
    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS approved
        FROM reimbursements
        WHERE status='Approved'
        """
    )
    approved = cursor.fetchone()["approved"]

    cursor.execute(
        """
        SELECT COUNT(*) AS pending
        FROM reimbursements
        WHERE status='Pending'
        """
    )
    pending = cursor.fetchone()["pending"]

    cursor.execute(
        """
        SELECT COUNT(*) AS rejected
        FROM reimbursements
        WHERE status='Rejected'
        """
    )
    rejected = cursor.fetchone()["rejected"]

    return jsonify({
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    })


# Generate PDF Report
@admin_bp.route("/generate-report", methods=["GET"])
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

    content.append(Spacer(1, 20))

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM reimbursements")

    data = cursor.fetchall()

    for item in data:

        text = f"""
        ID: {item['id']}<br/>
        Amount: ₹{item['expense_amount']}<br/>
        Category: {item['category']}<br/>
        Status: {item['status']}<br/>
        """

        content.append(
            Paragraph(text, styles["BodyText"])
        )

        content.append(Spacer(1, 10))

    doc.build(content)

    return send_from_directory(
        ".",
        pdf_file,
        as_attachment=True
    )