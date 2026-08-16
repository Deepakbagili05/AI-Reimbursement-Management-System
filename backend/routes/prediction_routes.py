from flask import Blueprint, request, jsonify
import joblib
import os

prediction_bp = Blueprint("prediction", __name__)

# Load ML Model
model_path = os.path.join(
    os.path.dirname(__file__),
    "../ml/reimbursement_model.pkl"
)

model = joblib.load(model_path)


# ----------------------------
# Prediction API
# ----------------------------
@prediction_bp.route("/predict", methods=["POST"])
def predict():

    data = request.json

    amount = float(data["expense_amount"])
    category = int(data["category"])
    submission_day = int(data["submission_day"])
    history_score = int(data["history_score"])
    bill_available = int(data["bill_available"])

    prediction = model.predict([[
        amount,
        category,
        submission_day,
        history_score,
        bill_available
    ]])

    probability = model.predict_proba([[
        amount,
        category,
        submission_day,
        history_score,
        bill_available
    ]])

    confidence = round(
        max(probability[0]) * 100,
        2
    )

    return jsonify({
        "prediction": int(prediction[0]),
        "confidence": confidence
    })