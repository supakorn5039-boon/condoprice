from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import logging


app = Flask(__name__)

# Load the trained model
with open('condo_price_model.pkl', 'rb') as model_file:
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
        # Extract user input from the JSON data sent by the front-end
        data = request.get_json()

        # Extract values from the data
        sqm = float(data['sqm'])
        bedroom = int(data['bedroom'])
        bathroom = int(data['bathroom'])
        parking = int(data['parking'])
        
        # Log the user's selections
        logging.info(f"User selected: sqm={sqm}, bedroom={bedroom}, bathroom={bathroom}, parking={parking}")

        # Create a DataFrame with the correct order of features
        input_data = pd.DataFrame({'bedroom': [bedroom], 'bathroom': [bathroom], 'sqm': [sqm], 'parking': [parking]})
        

        # Make the prediction using the model
        prediction = model.predict(input_data)[0]

        # Return the prediction result as JSON
        return jsonify({'prediction': prediction})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)