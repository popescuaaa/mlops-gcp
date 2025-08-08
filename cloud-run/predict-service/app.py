from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
try:
    with open('model_pipeline.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded from file")

except FileNotFoundError:
    print("Run locally the predictor file and rebuild the docker image")

# Routes
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "state": "running"
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json

        # Convert to DataFrame
        input_data = pd.DataFrame(data['instances']) # no-qa

        # Make prediction
        predictions = model.predict(input_data)
        probabilities = model.predict_proba(input_data).max(axis=1)

        # Return predictions
        return jsonify({
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400
