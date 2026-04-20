from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load model
model = pickle.load(open("flight_rf.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        # Airline encoding
        airline = request.form['airline']
        airlines = [
            'Jet Airways','IndiGo','Air India','Multiple carriers','SpiceJet',
            'Vistara','GoAir','Multiple carriers Premium economy',
            'Jet Airways Business','Vistara Premium economy','Trujet'
        ]
        airline_dict = {name: 0 for name in airlines}
        if airline in airline_dict:
            airline_dict[airline] = 1

        # Source encoding
        Source = request.form["Source"]
        sources = ['Delhi','Kolkata','Mumbai','Chennai']
        source_dict = {name: 0 for name in sources}
        if Source in source_dict:
            source_dict[Source] = 1

        # Destination encoding
        Destination = request.form["Destination"]
        destinations = ['Cochin','Delhi','New_Delhi','Hyderabad','Kolkata']
        dest_dict = {name: 0 for name in destinations}
        if Destination in dest_dict:
            dest_dict[Destination] = 1

        # Prediction
        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            airline_dict['Air India'],
            airline_dict['GoAir'],
            airline_dict['IndiGo'],
            airline_dict['Jet Airways'],
            airline_dict['Jet Airways Business'],
            airline_dict['Multiple carriers'],
            airline_dict['Multiple carriers Premium economy'],
            airline_dict['SpiceJet'],
            airline_dict['Trujet'],
            airline_dict['Vistara'],
            airline_dict['Vistara Premium economy'],
            source_dict['Chennai'],
            source_dict['Delhi'],
            source_dict['Kolkata'],
            source_dict['Mumbai'],
            dest_dict['Cochin'],
            dest_dict['Delhi'],
            dest_dict['Hyderabad'],
            dest_dict['Kolkata'],
            dest_dict['New_Delhi']
        ]])

        output = round(prediction[0], 2)

        return render_template(
            'index.html',
            prediction_text=f"Your Flight price is Rs. {output}"
        )

    return render_template("index.html")


# Render compatible run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)