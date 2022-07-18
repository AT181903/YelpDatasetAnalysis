from itertools import combinations

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.neighbors import NearestNeighbors


def score_plot_and_get_best(data_frame, algorithm, number_of_tests):
    if algorithm == "kmeans":
        parameter_to_detect = "n_clusters"
    else:
        parameter_to_detect = "eps"

    # fitted_kmeans = {}
    labels = {}
    df_scores = []
    inertias_for_kmeans = []

    for i in number_of_tests:
        if algorithm == "kmeans":
            model = KMeans(n_clusters=i)
        else:
            model = DBSCAN(eps=i, min_samples=10)

        i_labels = model.fit_predict(data_frame)

        if algorithm == "kmeans":
            inertias_for_kmeans.append(model.inertia_)

        # Insert fitted model and calculated cluster labels in dictionaries, for further reference.
        # fitted_kmeans[i] = kmeans
        labels[i] = i_labels

        # Calculate various scores, and save them for further reference.
        df_scores.append({
            parameter_to_detect: i,
            "silhouette_score": silhouette_score(data_frame, i_labels),
            "calinski_harabasz_score": calinski_harabasz_score(data_frame, i_labels),
            "davies_bouldin_score": davies_bouldin_score(data_frame, i_labels),
        })

    # Create a DataFrame of clustering scores, using `n_clusters` as index, for easier plotting.
    df_scores = pd.DataFrame(df_scores)
    df_scores.set_index(parameter_to_detect, inplace=True)

    print(df_scores)

    if algorithm == "kmeans":
        # Plot inertias
        plt.plot(number_of_tests, inertias_for_kmeans, 'bx-')
        plt.title('Inertias')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')

    best_scores_list = [
        df_scores["silhouette_score"].idxmax(),
        df_scores["calinski_harabasz_score"].idxmax(),
        df_scores["davies_bouldin_score"].idxmin()
    ]

    best_parameter = max(set(best_scores_list), key=best_scores_list.count)

    print("Best " + parameter_to_detect + ": ", best_parameter)

    return labels.get(best_parameter)


# def add_new_column(algorithm, df_new_column, initial_data_frame):
#     if algorithm == 'kmeans':
#         df_new_column = pd.DataFrame({'cluster': df_new_column})
#     else:
#         df_new_column = pd.DataFrame({'eps': df_new_column})
#
#     # return pd.concat([initial_data_frame, df_new_column], axis=1)
#
#     return pd.concat([initial_data_frame.reset_index(drop=True), df_new_column.reset_index(drop=True)], axis=1)

def add_new_column(algorithm, df_new_column, initial_data_frame):
    if algorithm == 'kmeans':
        df_new_column = pd.DataFrame({'cluster': df_new_column})
    else:
        df_new_column = pd.DataFrame({'eps': df_new_column})

    # df_new_column.reset_index()
    # initial_data_frame.reset_index()
    return pd.concat([initial_data_frame.reset_index(drop=True), df_new_column.reset_index(drop=True)], axis=1)


def plot_clusters(algorithm, data_frame, num_row, num_col, fig_width, fig_height):
    if algorithm == 'kmeans':
        c_column = 'cluster'
    else:
        c_column = 'eps'

    every_combinations = list(combinations(data_frame.drop(columns=c_column).columns, 2))

    figure, axis = plt.subplots(num_row, num_col, figsize=(fig_width, fig_height))

    next_row = 0
    next_column = 0

    for combination in every_combinations:
        first_feature = combination[0]
        second_feature = combination[1]

        axis[next_row, next_column].scatter(
            data_frame[first_feature],
            data_frame[second_feature],
            c=data_frame[c_column],
            cmap='rainbow'
        )

        axis[next_row, next_column].set_title(first_feature + " and " + second_feature)

        if next_column == (num_col - 1):
            next_row = next_row + 1
            next_column = 0
        else:
            next_column = next_column + 1


# Utils for DB Scan
def get_distances_and_plot(data_frame):
    nbrs = NearestNeighbors(n_neighbors=10, metric='cosine').fit(data_frame)
    distances, indices = nbrs.kneighbors(data_frame)
    distances = distances[:, 2]
    distances = np.sort(distances, axis=0)

    show_plot(distances)

    return distances


def filter_distances_and_plot(distances, filter, filter2):
    if (filter2 == None):
        distances = [x for x in distances if x > filter]
    else:
        distances = [x for x in distances if filter > x > filter2]

    show_plot(distances)

    return distances


def remove_duplicates(distances):
    no_duplicate_distances = list(dict.fromkeys(distances))
    show_plot(no_duplicate_distances)
    return no_duplicate_distances


def show_plot(distances):
    plt.plot(distances)
    plt.show()
