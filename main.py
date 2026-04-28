from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import keras
import pandas as pd

app = Flask(__name__)
CORS(app)

data = pd.read_csv("data/students.csv")
clean_data = data.dropna().copy()

le_gender = joblib.load("artifacts/le_gender.pkl")
le_race = joblib.load("artifacts/le_race.pkl")
scaler_X = joblib.load("artifacts/std_scaler_X.pkl")
scaler_y = joblib.load("artifacts/std_scaler_y.pkl")
advanced_model = keras.models.load_model("artifacts/advanced_model.keras")


def build_descriptive_statistics():
    describe_df = clean_data[["math score", "reading score", "writing score"]].describe().round(2)
    rows = []

    for index, row in describe_df.iterrows():
        rows.append({
            "metric": index,
            "math score": float(row["math score"]),
            "reading score": float(row["reading score"]),
            "writing score": float(row["writing score"]),
        })

    return rows


def build_insights():
    gender_writing = clean_data.groupby("gender")["writing score"].mean().round(2)
    prep_writing = clean_data.groupby("test preparation course")["writing score"].mean().round(2)
    lunch_math = clean_data.groupby("lunch")["math score"].mean().round(2)
    correlations = clean_data[["math score", "reading score", "writing score"]].corr().round(3)

    return [
        {
            "title": "Writing score po spolu",
            "value": f"female: {gender_writing['female']}, male: {gender_writing['male']}",
        },
        {
            "title": "Test preparation course",
            "value": f"completed: {prep_writing['completed']}, none: {prep_writing['none']}",
        },
        {
            "title": "Lunch i math score",
            "value": f"standard: {lunch_math['standard']}, free/reduced: {lunch_math['free/reduced']}",
        },
        {
            "title": "Najjača korelacija",
            "value": f"reading score i writing score: {correlations.loc['reading score', 'writing score']}",
        },
    ]


def build_chart_payload():
    score_means = clean_data[["math score", "reading score", "writing score"]].mean().round(2)
    gender_counts = clean_data["gender"].value_counts()
    race_counts = clean_data["race/ethnicity"].value_counts().sort_index()
    lunch_scores = clean_data.groupby("lunch")[["math score", "reading score", "writing score"]].mean().round(2)

    scatter_points = []
    for _, row in clean_data[["math score", "writing score"]].head(200).iterrows():
        scatter_points.append({
            "x": float(row["math score"]),
            "y": float(row["writing score"]),
        })

    return {
        "score_means": {
            "labels": ["Math", "Reading", "Writing"],
            "values": [
                float(score_means["math score"]),
                float(score_means["reading score"]),
                float(score_means["writing score"]),
            ],
        },
        "gender_counts": {
            "labels": gender_counts.index.tolist(),
            "values": [int(value) for value in gender_counts.tolist()],
        },
        "race_counts": {
            "labels": race_counts.index.tolist(),
            "values": [int(value) for value in race_counts.tolist()],
        },
        "lunch_score_means": {
            "labels": ["Math", "Reading", "Writing"],
            "datasets": [
                {
                    "label": "standard",
                    "values": [
                        float(lunch_scores.loc["standard", "math score"]),
                        float(lunch_scores.loc["standard", "reading score"]),
                        float(lunch_scores.loc["standard", "writing score"]),
                    ],
                },
                {
                    "label": "free/reduced",
                    "values": [
                        float(lunch_scores.loc["free/reduced", "math score"]),
                        float(lunch_scores.loc["free/reduced", "reading score"]),
                        float(lunch_scores.loc["free/reduced", "writing score"]),
                    ],
                },
            ],
        },
        "math_vs_writing": scatter_points,
    }


def make_prediction(payload):
    input_df = pd.DataFrame([{
        "gender": payload["gender"],
        "race/ethnicity": payload["race/ethnicity"],
        "math score": float(payload["math score"]),
        "reading score": float(payload["reading score"]),
    }])

    input_df["gender"] = le_gender.transform(input_df["gender"])
    input_df["race/ethnicity"] = le_race.transform(input_df["race/ethnicity"])

    scaled_input = scaler_X.transform(input_df)
    prediction_scaled = advanced_model.predict(scaled_input, verbose=0)
    prediction = scaler_y.inverse_transform(prediction_scaled)[0][0]

    return round(float(prediction), 2)


@app.route("/")
def home():
    return "Dobar dan!"


@app.route("/api/overview")
def overview():
    return jsonify({
        "dataset": {
            "rows_original": int(data.shape[0]),
            "cols_original": int(data.shape[1]),
            "rows_clean": int(clean_data.shape[0]),
            "cols_clean": int(clean_data.shape[1]),
            "column_names": data.columns.tolist(),
        },
        "missing_values": data.isnull().sum().astype(int).to_dict(),
        "descriptive_statistics": build_descriptive_statistics(),
        "insights": build_insights(),
    })


@app.route("/api/charts")
def charts():
    return jsonify(build_chart_payload())


@app.route("/api/predict", methods=["POST"])
@app.route("/predict_writing_score", methods=["POST"])
def predict():
    payload = request.get_json()

    if payload is None:
        return jsonify({"error": "Body mora biti JSON."}), 400

    required_fields = ["gender", "race/ethnicity", "math score", "reading score"]
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        return jsonify({
            "error": "Nedostaju obavezna polja.",
            "missing_fields": missing_fields,
        }), 400

    try:
        prediction = make_prediction(payload)
        return jsonify({"predicted_writing_score": prediction})
    except ValueError as exc:
        return jsonify({
            "error": "Neispravne ulazne vrijednosti.",
            "details": str(exc),
        }), 400
    except Exception as exc:
        return jsonify({
            "error": "Greška pri predikciji.",
            "details": str(exc),
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
