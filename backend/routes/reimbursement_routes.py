from database import connection


# Submit Reimbursement
def submit_reimbursement(user_id, amount, category, description, filename):

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

    return {
        "message": "Reimbursement Submitted Successfully"
    }


# Get All Reimbursements
def get_all_reimbursements():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM reimbursements
    """)

    return cursor.fetchall()


# Employee Reimbursement History
def get_history(user_id):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM reimbursements
        WHERE user_id=%s
    """, (user_id,))

    return cursor.fetchall()


# Approve Reimbursement
def approve_reimbursement(id):

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE reimbursements
        SET status='Approved'
        WHERE id=%s
    """, (id,))

    connection.commit()

    return {
        "message": "Approved Successfully"
    }


# Reject Reimbursement
def reject_reimbursement(id):

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE reimbursements
        SET status='Rejected'
        WHERE id=%s
    """, (id,))

    connection.commit()

    return {
        "message": "Rejected Successfully"
    }


# Employee Dashboard Statistics
def employee_dashboard(user_id):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM reimbursements
        WHERE user_id=%s
    """, (user_id,))
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS approved
        FROM reimbursements
        WHERE user_id=%s
        AND status='Approved'
    """, (user_id,))
    approved = cursor.fetchone()["approved"]

    cursor.execute("""
        SELECT COUNT(*) AS pending
        FROM reimbursements
        WHERE user_id=%s
        AND status='Pending'
    """, (user_id,))
    pending = cursor.fetchone()["pending"]

    cursor.execute("""
        SELECT COUNT(*) AS rejected
        FROM reimbursements
        WHERE user_id=%s
        AND status='Rejected'
    """, (user_id,))
    rejected = cursor.fetchone()["rejected"]

    return {
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    }


# Admin Dashboard Statistics
def admin_statistics():

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM reimbursements")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS approved
        FROM reimbursements
        WHERE status='Approved'
    """)
    approved = cursor.fetchone()["approved"]

    cursor.execute("""
        SELECT COUNT(*) AS pending
        FROM reimbursements
        WHERE status='Pending'
    """)
    pending = cursor.fetchone()["pending"]

    cursor.execute("""
        SELECT COUNT(*) AS rejected
        FROM reimbursements
        WHERE status='Rejected'
    """)
    rejected = cursor.fetchone()["rejected"]

    return {
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    }