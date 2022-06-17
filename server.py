import pickle
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home_page():  # put application's code here
    return 'go to ./predict_review to predict a review'


@app.route('/predict_review', methods=(['GET']))
def predict_review():
    return "To predict_review"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
