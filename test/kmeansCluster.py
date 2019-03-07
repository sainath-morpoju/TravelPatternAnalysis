
import pandas as pd
import numpy as np


class kmeansCluster(object):
    def __init__(self,data = None, metric = None, no_of_clusters = 1, **kwargs ):
        self.data = data
        self.clusters = no_of_clusters
        self.distance_metric = metric
        self.result = {}
        self._setup()

    def _setup(self):
        for i in range(self.clusters):
            self.result[i] = {"mean"}