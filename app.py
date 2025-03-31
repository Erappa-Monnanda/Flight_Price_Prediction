from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# ✅ Define homepage route
@app.route('/')
def home():
    return render_template("index.html")

# ✅ Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("Received form data:", request.form)  # ✅ Debugging

        # ✅ Get input values from form
        journey_day = request.form.get('Journey_Day')
        journey_month = request.form.get('Journey_Month')
        dep_hour = request.form.get('Dep_Hour')
        source = request.form.get('Source')
        destination = request.form.get('Destination')
        airline = request.form.get('Airline')
        duration = request.form.get('Duration')  # ✅ Added Duration (in minutes)
        total_stops = request.form.get('Total_Stops')

        # ✅ Ensure no empty values
        if None in [journey_day, journey_month, dep_hour, source, destination, airline, duration, total_stops]:
            return jsonify({"error": "Missing input values!"}), 400

        # ✅ Convert values to correct types
        journey_day = int(journey_day)
        journey_month = int(journey_month)
        dep_hour = int(dep_hour)
        duration = float(duration)  # ✅ Convert duration to float
        total_stops = int(total_stops)

        # ✅ Create DataFrame for prediction
        input_data = pd.DataFrame([[journey_day, journey_month, dep_hour, source, destination, airline, duration, total_stops]],
                                  columns=['Journey_Day', 'Journey_Month', 'Dep_Hour', 'Source', 'Destination',
                                           'Airline', 'Duration', 'Total_Stops'])

        # ✅ Make prediction
        prediction = model.predict(input_data)[0]

        return render_template("index.html", prediction_text=f"Predicted Flight Price: ₹{prediction:,.2f}")

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)