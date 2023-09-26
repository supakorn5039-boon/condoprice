from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('Data_midterm.csv')
pipe = pickle.load(open('BestModel_CNX.pkl','rb'))


@app.route('/')
def index():
    
    
    locations = sorted(data['location'].unique()) 
    return render_template('index.html' ,locations=locations)


@app.route('/predict' , methods=['POST'])
def predict():
    location = request.form.get('location')
    sqm
    bedrooms
    bathrooms
    parking
    
    
    return ""


if __name__ == "__main__":
    app.run(debug=True, port=5001)
