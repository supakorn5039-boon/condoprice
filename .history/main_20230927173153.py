from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)
data = pd.read_csv('Book5.csv')
pipe = pickle.load(open('model1.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Extract user input from the form
        sqm = int(request.form.get('sqm'))
        bedroom = int(request.form.get('bedroom'))
        bathroom = int(request.form.get('bathroom'))
        parking = int(request.form.get('parking'))

        # Create a DataFrame with the correct order of features
        input_data = pd.DataFrame([[sqm, bedroom, bathroom, parking ]], columns=['sqm', 'bedroom', 'bathroom', 'parking'])

        # Preprocess user input data as needed (e.g., one-hot encoding)

        # Make the prediction using the model
        prediction = pipe.predict(input_data)[0] * 1e5

        # Return the prediction result as JSON
        return jsonify({'prediction': np.round(prediction, 2)})

    # Handle GET request (initial page load)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)