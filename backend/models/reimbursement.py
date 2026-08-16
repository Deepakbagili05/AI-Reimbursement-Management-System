from database import connection


def submit_reimbursement(user_id, amount, category, description, filename):
    cursor = connection.cursor()

    cursor.execute("""
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
        (%s,%s,%s,%s,%s,'Pending')
    """, (
        user_id,
        amount,
        category,
        description,
        filename
    ))

    connection.commit()

    return {
        "message": "Reimbursement Submitted Successfully"
    }


def get_all_reimbursements():
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM reimbursements")

    return cursor.fetchall()


def get_history(user_id):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM reimbursements WHERE user_id=%s",
        (user_id,)
    )

    return cursor.fetchall()


def approve_reimbursement(reimbursement_id):
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE reimbursements SET status='Approved' WHERE id=%s",
        (reimbursement_id,)
    )

    connection.commit()

    return {
        "message": "Approved Successfully"
    }


def reject_reimbursement(reimbursement_id):
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE reimbursements SET status='Rejected' WHERE id=%s",
        (reimbursement_id,)
    )

    connection.commit()

    return {
        "message": "Rejected Successfully"
    }


def employee_dashboard(user_id):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS total FROM reimbursements WHERE user_id=%s",
        (user_id,)
    )
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS approved FROM reimbursements WHERE user_id=%s AND status='Approved'",
        (user_id,)
    )
    approved = cursor.fetchone()["approved"]

    cursor.execute(
        "SELECT COUNT(*) AS pending FROM reimbursements WHERE user_id=%s AND status='Pending'",
        (user_id,)
    )
    pending = cursor.fetchone()["pending"]

    cursor.execute(
        "SELECT COUNT(*) AS rejected FROM reimbursements WHERE user_id=%s AND status='Rejected'",
        (user_id,)
    )
    rejected = cursor.fetchone()["rejected"]

    return {
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    }


def admin_statistics():
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM reimbursements")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS approved FROM reimbursements WHERE status='Approved'")
    approved = cursor.fetchone()["approved"]

    cursor.execute("SELECT COUNT(*) AS pending FROM reimbursements WHERE status='Pending'")
    pending = cursor.fetchone()["pending"]

    cursor.execute("SELECT COUNT(*) AS rejected FROM reimbursements WHERE status='Rejected'")
    rejected = cursor.fetchone()["rejected"]

    return {
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    }