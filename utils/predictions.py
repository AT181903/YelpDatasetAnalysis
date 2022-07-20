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

import pickle
import pandas as pd
from utils import text_processing
from utils.algorithm import score_plot_and_get_best


def predict_review(review):
    df_review = pd.DataFrame([review], columns=['text'])

    text_processing.process_text(df_review)

    vectorizer = pickle.load(open('../models/vectorizer.pkl', 'rb'))

    vectorized_review = pd.DataFrame(columns=vectorizer.get_feature_names_out(),
                                     data=vectorizer.transform(df_review["processed_text"]).toarray())

    svc_model = pickle.load(open('../models/svc_model.pkl', 'rb'))

    review_prediction = svc_model.predict(vectorized_review)

    return review_prediction
