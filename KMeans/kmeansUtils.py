import numpy
from sklearn.cluster import KMeans


def skKmeans(data, cluster=8, random=0):
    return KMeans(n_clusters=cluster, random_state=random).fit(data)

distEucld = (lambda vecA, vecB:
             np.sqrt(np.sum(np.power(vecA - vecB, 2))))

distAbs = (lambda vecA, vecB:
           np.sum(abs(vecA - vecB)))


class kmeansAlg(object):
    """
    kmeans classifier
    implemented with flex extension of different choice in 
    distance function. 

    inputs:
        data: matrix like (n, d1, d2 ...) n is the number of samples
        k: number of centroids to assign
        distFun: choose the type of dissimilarity measure function
    """
    data = None
    centroids = None
    distFun = None

    def __init__(self, arg):
        super(kmeansAlg, self).__init__()
        self.arg = arg

    def dist(self, ):
        return dist

    def randCentroids(self, k):
        index = len(data)
        indexShuffle = np.random.shuffle(index)[0:k]
        self.centroids = np.zeros((k,) + data.shape[1:])
        for i in range(k):
            self.centroids[i, :] = data[indexShuffle[i], :]

    def fit(self,)
