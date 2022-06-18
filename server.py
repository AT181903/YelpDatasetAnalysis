from flask import Flask, request
from flask_cors import CORS

import predictions

app = Flask(__name__)
CORS(app)


@app.route('/')
def home_page():  # put application's code here
    return 'go to ./predict_review to predict a review'


@app.route('/predict_review', methods=(['GET']))
def predict_review():
    query_param = request.args.to_dict()

    review = query_param.get("review")

    if predictions.predict_review(review)[0] == 0:
        return "Bad review"
    else:
        return "Good review"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
