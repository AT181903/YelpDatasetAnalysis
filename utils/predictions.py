import pickle
import pandas as pd
from utils import text_processing
from utils.algorithm import score_plot_and_get_best


def predict_review(review):
    df_review = pd.DataFrame([review], columns=['text'])

    text_processing.process_text(df_review)

    vectorizer = pickle.load(open('/Users/at181903/PycharmProjects/IAproject/models/vectorizer.pkl', 'rb'))

    vectorized_review = pd.DataFrame(columns=vectorizer.get_feature_names_out(),
                                     data=vectorizer.transform(df_review["processed_text"]).toarray())

    svc_model = pickle.load(open('/Users/at181903/PycharmProjects/IAproject/models/svc_model.pkl', 'rb'))

    review_prediction = svc_model.predict(vectorized_review)

    return review_prediction
