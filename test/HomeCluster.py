import inline as inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, time
from test.DistanceCalculator import DistanceCalculator
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
# from shapely.geometry import MultiPoint
# %matplotlib inline


class HomeCluster():
    kms_per_radian = 6371.0088
    epsilon = 0.1 / kms_per_radian
    def __init__(self,path = "C:/Users/saina/Documents/sample/test/data/sensorDataSelf.xlsx"):
        self.df = pd.read_excel(path, header=0).filter(items=['locLat', 'locLon'])
       # self.df =  self.df[self.df['locLat'] != "None"]
        # df = pd.read_csv('C:/Users/saina/Documents/sample/test/data/sample_data.csv', encoding='utf-8')
        # df = pd.read_excel("C:/Users/saina/Documents/sample/test/data/sampleData.xlsx",header = 0).filter(items =['locLat','locLon'])
        # self.df.head()
        self.homeLocation = []
        self._dbscan_()

    def _dbscan_(self):

        coords1 = self.df.as_matrix(columns=['locLat', 'locLon'])
        coords = [x for x in coords1 if x[0] is not None]
        # start_time = time.time()
        db = DBSCAN(eps=self.epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
        cluster_labels = db.labels_
        num_clusters = len(set(cluster_labels))
        n_clusters_ = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)

        message = 'Clustered {:,} points down to {:,} clusters'
        print(message.format(len(self.df), num_clusters, 100*(1 - float(num_clusters) / len(self.df))))
        # print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(coords, cluster_labels)))

        clusters = pd.Series([coords[cluster_labels==n] for n in range(num_clusters)])
        max_len, indx = -1,-1
        for i in range(len(clusters)):
            if max_len < len(clusters[i]):
                indx = i
                max_len = len(clusters[i])

        print(indx)
        print(clusters[indx])

        self.homeLocation = clusters[indx].mean(axis=0)
        print("The home location is [Lat,Lon]: ")
        print(self.homeLocation)
        # DistanceCalculator

        # with open("C:/Users/saina/Documents/sample/test/data/seriesout.txt", "w") as out:
        #     print(clusters, file=out)

        # print(([coords[cluster_labels==n]]) for n in range(num_clusters) )

if __name__ == "__main__":
        hc = HomeCluster()
        print(hc.homeLocation)
        DistanceCalculator(hc.homeLocation)

