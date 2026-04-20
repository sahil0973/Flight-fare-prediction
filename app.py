from flask import Flask, request, render_template
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("flight_model.joblib")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.form.to_dict()

        df = pd.DataFrame([{
            "Airline": data["airline"],
            "Source": data["source"],
            "Destination": data["destination"],
            "Total_Stops": int(data["stops"]),
            "Journey_day": int(data["day"]),
            "Journey_month": int(data["month"]),
            "Dep_hour": int(data["dep"]),
            "Arrival_hour": int(data["arr"])
        }])

        prediction = model.predict(df)[0]

        return render_template("index.html",
                               prediction_text=f"Price: ₹ {round(prediction,2)}")

    except Exception as e:
        return render_template("index.html",
                               prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)