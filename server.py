import json

import pandas as pd
from flask import Flask, request
from flask_cors import CORS

from utils import predictions

app = Flask(__name__)
CORS(app)


@app.route('/')
def home_page():  # put application's code here
    return 'go to ./predict_review to predict a review'


@app.route('/predict_review', methods=(['GET']))
def pred_review():
    query_param = request.args.to_dict()

    review = query_param.get("review")

    if predictions.predict_review(review)[0] == 0:
        return json.dumps({"prediction" : "Bad review"})
    else:
        return json.dumps({"prediction" : "Good review"})


@app.route('/test', methods=(['GET']))
def predict_review():
    df_review = pd.read_csv('./dataset/df_business_filtered_by_city.csv')

    # print(df_review.shape)

    # df_review = df_review.iloc[44000:, :]

    # print(df_review.shape)

    return df_review[['latitude', 'longitude', 'cluster']].to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
