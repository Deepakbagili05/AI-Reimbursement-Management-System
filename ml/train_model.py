import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("reimbursement_dataset.csv")

encoder = LabelEncoder()

df["category"] = encoder.fit_transform(
    df["category"]
)

df["status"] = encoder.fit_transform(
    df["status"]
)

X = df[
    [
        "expense_amount",
        "category",
        "submission_day",
        "history_score",
        "bill_available"
    ]
]

y = df["status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier()

model.fit(X_train, y_train)

joblib.dump(
    model,
    "reimbursement_model.pkl"
)

print("Model Trained Successfully")