import tensorflow as tf
import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# データセットの作成
n_samples = 1500
n_features = 1536
n_clusters = 3

X, y_true = make_blobs(
    n_samples=n_samples, centers=n_clusters, n_features=n_features, random_state=42
)

# 初期のクラスタ中心をランダムに選択
k = n_clusters
initial_centers = tf.Variable(X[np.random.choice(len(X), k, replace=False)])


# K-meansクラスタリングの実装
def assign_to_nearest(X, centers):
    expanded_vectors = tf.expand_dims(X, 0)
    expanded_centers = tf.expand_dims(centers, 1)
    distances = tf.reduce_sum(tf.square(expanded_vectors - expanded_centers), 2)
    assignments = tf.argmin(distances, axis=0)
    return assignments


def update_centers(X, assignments, k):
    new_centers = []
    for i in range(k):
        assigned_points = X[assignments == i]
        new_center = tf.reduce_mean(assigned_points, axis=0)
        new_centers.append(new_center)
    return tf.stack(new_centers)


def kmeans(X, initial_centers, num_iters=100):
    centers = initial_centers
    for _ in range(num_iters):
        assignments = assign_to_nearest(X, centers)
        centers = update_centers(X, assignments, k)
    return assignments, centers


assignments, centers = kmeans(X, initial_centers)

# 結果の可視化
plt.scatter(X[:, 0], X[:, 1], c=assignments, cmap="viridis")
plt.scatter(centers[:, 0], centers[:, 1], c="red", marker="x")
plt.title("K-means Clustering with TensorFlow")
plt.savefig("kmeans_clustering_result.png")
