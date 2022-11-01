from code.base_functions import *

#https://towardsdatascience.com/hierarchical-clustering-and-k-means-clustering-on-country-data-84b2bf54d282

# allData = pd.read_excel("macrobond_series_eu_industries.xlsx")
# data2 = collectData(allData)
# pd.concat(data2,  axis=1).to_csv("tmp2.csv")

df1=pd.read_csv("tmp2.csv")
#print(df1.head())

data1=df1.iloc[-10:,:].mean()

#data1.to_csv("tmp3.csv")
country_sector=data1.index.str.split("_")
country=[x[0] for x in country_sector]
sector=[x[1] for x in country_sector]

values=data1.values
n = 34

data1 = [values[i:i + n] for i in range(0, len(values), n)]
df1 = pd.DataFrame(data1)
df1.index = sector[::34]
df1.columns = country[0:34]

df1.drop(columns=["Euro Area"], inplace=True)

clus1 = df1.T

normalized_clus1=(clus1-clus1.mean())/clus1.std()

#normalized_clus1.to_csv("tmp4.csv")

print(normalized_clus1)

from scipy.cluster.hierarchy import dendrogram, linkage
linkage_data = linkage(normalized_clus1, method='ward', metric='euclidean')
dendrogram(linkage_data, labels=normalized_clus1.index)

plt.savefig("dendogram.png")
#plt.show()

########################################
from sklearn.decomposition import PCA
X = normalized_clus1.values
pca = PCA(n_components=2)
print(pca.fit(X))

print(pca.explained_variance_ratio_)

pca = PCA(n_components=2)
pca.fit(X)

print(pca.transform(X))
scores_pca=pca.transform(X)

wcss = []
from sklearn.cluster import KMeans

for i in range(1,21):
    kmeans_pca = KMeans(n_clusters=i, init='k-means++')
    kmeans_pca.fit(scores_pca)
    wcss.append(kmeans_pca.inertia_)


plt.figure(figsize=(10,8))
plt.plot(range(1,21), wcss, marker='o', linestyle='--')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.title('K-means with PCS clustering')
plt.show()


#df_segm_pca_kmeans = pd.concat([normalized_clus1.reset_index(drop=True), pd.DataFrame(scores_pca)], axis=1)
#df_segm_pca_kmeans.columns.values[-3:] =