from flask import Flask, request, jsonify, send_file
import joblib
import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

df = pd.read_csv("data/students.csv")

le_gender = joblib.load("artifacts/le_gender.pkl")
le_race = joblib.load("artifacts/le_race.pkl")

scaler_X = joblib.load("artifacts/std_scaler_X.pkl")
scaler_y = joblib.load("artifacts/std_scaler_y.pkl")

advanced_model = keras.models.load_model("artifacts/advanced_model.keras")


@app.route("/")
def home():
    return "Dobar dan!"

@app.route("/predict_writing_score", methods=["POST"])
def predict_writing_score():
    data = request.get_json()

    gender = data["gender"]
    race = data["race/ethnicity"]
    math_score = data["math score"]
    reading_score = data["reading score"]

    gender_encoded = le_gender.transform([gender])[0]
    race_encoded = le_race.transform([race])[0]

    X = np.array([[
        gender_encoded,
        race_encoded,
        math_score,
        reading_score
    ]])

    X_scaled = scaler_X.transform(X)

    y_pred_scaled = advanced_model.predict(X_scaled)

    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    return jsonify({
        "predicted_writing_score": round(float(y_pred[0][0]), 3)
    })

@app.route("/dataset_stats", methods=["GET"])
def dataset_stats():
    numeric_df = df.select_dtypes(include=[np.number])

    stats = {
        "shape": {
            "rows": df.shape[0],
            "columns": df.shape[1]
        },
        "columns": list(df.columns),
        "numeric_summary": numeric_df.describe().to_dict(),
        "mean": numeric_df.mean().to_dict(),
        "std": numeric_df.std().to_dict(),
        "min": numeric_df.min().to_dict(),
        "max": numeric_df.max().to_dict(),
        "quartiles": {
            "q1": numeric_df.quantile(0.25).to_dict(),
            "median": numeric_df.quantile(0.5).to_dict(),
            "q3": numeric_df.quantile(0.75).to_dict()
        }
    }

    return jsonify(stats)

@app.route("/dataset_plot", methods=["GET"])
def dataset_plot():
    cols = ["math score", "reading score", "writing score"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, col in enumerate(cols):
        axes[i].hist(df[col], bins=20)
        axes[i].set_title(col)
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Frequency")

    plt.tight_layout()

    # spremi u memoriju (buffer)
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)