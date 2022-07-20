#  Copyright (C) <2022>  <MontyPython Group>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json

import pandas as pd
from flask import Flask, request
from flask_cors import CORS

from utils import predictions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

CORS(app, cors_allowed_origins='*')

port = 5500


@app.route('/')
def home_page():  # put application's code here
    return 'go to ./predict_review to predict a review'


@app.route('/predict_review', methods=(['GET']))
def predict_review():
    query_param = request.args.to_dict()

    review = query_param.get("review")

    prediction_string = "Bad" if predictions.predict_review(review)[0] == 0 else "Good"

    return json.dumps({"prediction": prediction_string + " review"})


@app.route('/get_clustered_df_kmeans', methods=(['GET']))
def get_clustered_df_kmeans():
    return get_clustered_df('kmeans')


@app.route('/get_clustered_df_dbscan', methods=(['GET']))
def get_clustered_df_dbscan():
    return get_clustered_df('dbscan')


def get_clustered_df(algorithm):
    df_review = pd.read_csv('./dataset/df_business_filtered_by_city_' + algorithm + '.csv')

    cluster_column = 'cluster' if algorithm == 'kmeans' else 'eps'

    return df_review[['name', 'address', 'latitude', 'longitude', cluster_column]].to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
