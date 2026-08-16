import joblib
import os

# Load ML model
model_path = os.path.join(
    os.path.dirname(__file__),
    "../ml/reimbursement_model.pkl"
)

model = joblib.load(model_path)


def predict_reimbursement(
    expense_amount,
    category,
    submission_day,
    history_score,
    bill_available
):
    prediction = model.predict([[
        expense_amount,
        category,
        submission_day,
        history_score,
        bill_available
    ]])

    probability = model.predict_proba([[
        expense_amount,
        category,
        submission_day,
        history_score,
        bill_available
    ]])

    confidence = round(max(probability[0]) * 100, 2)

    return {
        "prediction": int(prediction[0]),
        "confidence": confidence
    }