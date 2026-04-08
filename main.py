from flask import Flask
import joblib
import keras

app = Flask(__name__)

le_gender = joblib.load("artifacts/le_gender.pkl")
le_race = joblib.load("artifacts/le_race.pkl")

scaler_X = joblib.load("artifacts/std_scaler_X.pkl")
scaler_y = joblib.load("artifacts/std_scaler_y.pkl")

advanced_model = keras.models.load_model("artifacts/advanced_model.keras")

@app.route("/")
def home():
    return "Dobar dan!"

@app.route("/load_model")
def load_model():
    return "aa"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)