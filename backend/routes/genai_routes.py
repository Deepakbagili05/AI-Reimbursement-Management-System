from flask import Blueprint, request, jsonify
from gemini_summary import generate_ai_summary

genai_bp = Blueprint("genai", __name__)


# ----------------------------
# AI Summary API
# ----------------------------
@genai_bp.route("/summary", methods=["POST"])
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