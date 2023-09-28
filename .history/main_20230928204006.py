from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


app = Flask(__name__)

# Load the trained model
with open('data.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the index route
@app.route('/')
def index():
    return render_template('index.html')

# Define the predict route to handle form submissions
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extract user input from the JSON data sent by the front-end
        data = request.get_json()

        # Extract values from the data
        sqm = float(data['sqm'])
        bedroom = int(data['bedroom'])
        bathroom = int(data['bathroom'])
        parking = int(data['parking'])

        # Create a DataFrame with the correct order of features
        input_data = pd.DataFrame([[sqm, bedroom, bathroom, parking]], columns=['sqm', 'bedroom', 'bathroom', 'parking'])

        # Generate polynomial features for prediction data
        poly_transform = PolynomialFeatures(degree=2)
        input_data_poly = poly_transform.fit_transform(input_data)

        # Ensure feature order and names match those used during training
        feature_names = poly_transform.get_feature_names_out(input_data.columns)
        input_data_poly = pd.DataFrame(input_data_poly, columns=feature_names)

        # Make the prediction using the loaded model
        prediction = model.predict(input_data_poly)[0] * 1e5

        # Return the prediction result as JSON
        return jsonify({'prediction': np.round(prediction, 2)})
    
    
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)
