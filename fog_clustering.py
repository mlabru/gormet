# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.model_selection import ParameterGrid
from sklearn.cluster import KMeans

# < constants >--------------------------------------------------------------------------------

# diretório contendo as imagens
DS_DIR_IMG = "data/shots/cap/SBGR-28/"

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------------------------
def load_embeddings():
    """
    loading the fog dataset in pandas dataframe

    :returns: scaled data
    """
    # loading fog dataset
    fog_raw = pd.read_csv("./data/fog-clustering.csv")

    # checking data shape
    row, col = fog_raw.shape
    print(f'There are {row} rows and {col} columns') 
    print(fog_raw.head(10))

    # to work on copy of the data
    fog_raw_scaled = fog_raw.copy()

    # scaling the data to keep the different attributes in same range
    fog_raw_scaled[fog_raw_scaled.columns] = StandardScaler().fit_transform(fog_raw_scaled)
    print(fog_raw_scaled.describe())

    return fog_raw_scaled

# ---------------------------------------------------------------------------------------------
def pca_embeddings(df_scaled):
    """
    To reduce the dimensions of the fog dataset we use Principal Component Analysis (PCA).
    Here we reduce it from 5 dimensions to 2.

    :param df_scaled: scaled data
    :return: pca result, pca for plotting graph
    """

    pca_2 = PCA(n_components=2)
    pca_2_result = pca_2.fit_transform(df_scaled)
    print('Explained variation per principal component: {}'.format(pca_2.explained_variance_ratio_))
    print('Cumulative variance explained by 2 principal components: {:.2%}'.format(np.sum(pca_2.explained_variance_ratio_)))

    # Results from pca.components_
    dataset_pca = pd.DataFrame(abs(pca_2.components_), columns=df_scaled.columns, index=['PC_1', 'PC_2'])
    print('\n\n', dataset_pca)
    
    print("\n*************** Most important features *************************")
    print('As per PC 1:\n', (dataset_pca[dataset_pca > 0.3].iloc[0]).dropna())
    print('\n\nAs per PC 2:\n', (dataset_pca[dataset_pca > 0.3].iloc[1]).dropna())
    print("\n******************************************************************")

    return pca_2_result, pca_2

# ---------------------------------------------------------------------------------------------
def kmean_hyper_param_tuning(data):
    """
    Hyper parameter tuning to select the best from all the parameters on the basis of silhouette_score.

    :param data: dimensionality reduced data after applying PCA
    :return: best number of clusters for the model (used for KMeans n_clusters)
    """
    # candidate values for our number of cluster
    parameters = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]

    # instantiating ParameterGrid, pass number of clusters as input
    parameter_grid = ParameterGrid({'n_clusters': parameters})

    best_score = -1
    kmeans_model = KMeans(n_init="auto")     # instantiating KMeans model
    silhouette_scores = []

    # evaluation based on silhouette_score
    for p in parameter_grid:
        kmeans_model.set_params(**p)    # set current hyper parameter
        kmeans_model.fit(data)          # fit model on fog dataset, this will find clusters based on parameter p

        ss = metrics.silhouette_score(data, kmeans_model.labels_)   # calculate silhouette_score
        silhouette_scores += [ss]       # store all the scores

        print('Parameter:', p, 'Score', ss)

        # check p which has the best score
        if ss > best_score:
            best_score = ss
            best_grid = p

    # plotting silhouette score
    plt.bar(range(len(silhouette_scores)), list(silhouette_scores), align='center', color='#722f59', width=0.5)
    plt.xticks(range(len(silhouette_scores)), list(parameters))
    plt.title('Silhouette Score', fontweight='bold')
    plt.xlabel('Number of Clusters')
    plt.show()

    return 5  # best_grid['n_clusters']

# ---------------------------------------------------------------------------------------------
def visualizing_results(pca_result, label, centroids_pca):
    """ 
    Visualizing the clusters

    :param pca_result: PCA applied data
    :param label: K Means labels
    :param centroids_pca: PCA format K Means centroids
    """
    # ------------------ Using Matplotlib for plotting-----------------------
    x = pca_result[:, 0]
    y = pca_result[:, 1]

    plt.scatter(x, y, c=label, alpha=0.5, s=200)  # plot different colors per cluster
    plt.title('Fog clusters')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')

    plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1],
                marker='X', s=200, linewidths=1.5,
                color='red', edgecolors="black", lw=1.5)
    plt.show()

# ---------------------------------------------------------------------------------------------
def make_link(flst_labels: list):
    """
    write image
    """
    # index
    li_ndx = 0
    # percorre o diretório de imagens...
    for ls_filename in os.listdir(DS_DIR_IMG):
        # é um arquivo de imagem ?
        if ls_filename.endswith(".jpg") or ls_filename.endswith(".png"):
            # caminho completo para a imagem
            ls_image_path = os.path.join(DS_DIR_IMG, ls_filename)

            # caminho da imagem
            ls_src = os.path.join("..", ls_filename)
            
            # caminho completo para a saída
            ls_dst = os.path.join(DS_DIR_IMG, "kmeans", f'{flst_labels[li_ndx]:02d}_' + ls_filename)

            # increment index
            li_ndx += 1
            
            try:
                # create a symbolic link pointing to src named dst using os.symlink() method
                os.symlink(ls_src, ls_dst)

            # em caso de erro...
            except FileExistsError:
                # remove previous link
                os.remove(ls_dst)

                # create a symbolic link pointing to src named dst using os.symlink() method
                os.symlink(ls_src, ls_dst)

# ---------------------------------------------------------------------------------------------
def main():
    print("1. Loading Fog dataset\n")
    data_scaled = load_embeddings()

    print("\n\n2. Reducing via PCA\n")
    pca_result, pca_2 = pca_embeddings(data_scaled)

    print("\n\n3. HyperTuning the Parameter for KMeans\n")
    optimum_num_clusters = kmean_hyper_param_tuning(data_scaled)
    print("optimum num of clusters =", optimum_num_clusters)

    # fitting KMeans
    kmeans = KMeans(n_clusters=optimum_num_clusters, n_init="auto")
    labels = kmeans.fit_predict(data_scaled)

    centroids = kmeans.cluster_centers_
    centroids_pca = pca_2.transform(centroids)

    print("\n\n4. Visualizing the data")
    visualizing_results(pca_result, kmeans.labels_, centroids_pca)

    print("\n\n5. Making links")
    make_link(labels)

if __name__ == "__main__":
    main()
