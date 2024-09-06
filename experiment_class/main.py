import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

load_dotenv()

df = pd.read_csv("todos.csv")

client = OpenAI(api_key=os.getenv("API_KEY"))

model = "text-embedding-3-small"
titles = df["title"]
embs = {}
for i, title in enumerate(titles):
    emb = client.embeddings.create(input=title, model=model).data[0].embedding
    embs[df["id"][i]] = emb

X = np.array(list(embs.values()))
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-meansクラスタリングの適用
n_clusters = 6
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(X_scaled)

results = {}

for i in range(n_clusters):
    results[str(i)] = []

for i, label in enumerate(kmeans.labels_):
    print(f"Title: '{df['title'][i]}' -> Cluster: {label}")
    results[str(label)] = results[str(label)] + [df["title"][i]]

import pprint

pprint.pprint(results)

""" # クラスタリング結果の可視化
# 2次元に縮約するためにPCAを使用
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis')
plt.title("K-means Clustering on OpenAI Embeddings")
plt.savefig('result.png')
 """
