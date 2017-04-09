import numpy as np
from sklearn.cluster import KMeans


def skKmeans(data, cluster=8, random=0):
    return KMeans(n_clusters=cluster, random_state=random).fit(data)

distEucld = (lambda vecA, vecB:
             np.sqrt(np.sum(np.power(vecA.reshape(-1) - vecB.reshape(-1), 2))))

distAbs = (lambda vecA, vecB:
           np.sum(abs(vecA.reshape(-1) - vecB.reshape(-1))))


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
    k = None
    shape = None
    classAssign = None
    """
        init(k)
            set cluster number k,
        dist
            get distance function
        randCentroids
            randomly select k entries from the data as centroids
        fit(data)
            set data
            start k means converge
        predict(testdata)
            return a closest centroid

    """

    def __init__(self, k, dataSet=None):
        super(kmeansAlg, self).__init__()
        self.k = k
        if dataSet:
            self.data = dataSet
            self.shape = dataSet.shape[1:]

    def dist(self):
        pass
        # return dist

    def randCentroids(self):
        data = self.data
        k = self.k
        index = len(data)
        indexShuffle = np.arange(index)
        np.random.shuffle(indexShuffle)
        indexShuffle = indexShuffle[0:k]
        self.centroids = []
        for i in range(k):
            self.centroids.append(data[indexShuffle[i], :])
        print 'init centroids\n', self.centroids

    def fit(self, dataSet, distMethod=distEucld, centrSel=randCentroids):
        if dataSet == None:
            raise Exception('No correct input')
        self.data = dataSet
        self.shape = dataSet.shape[1:]
        self.randCentroids()
        self._fit(dist=distMethod)

    def _fit(self, dist=distEucld):
        """
            flag

            while flag:
                flag = false
                Update class
                for each datapoint
                    find closest centroids index i
                    compare new class to previous ones
                        if not equal
                            flag = true
                    assign/update this number to its class


                Update centroids
                for each centroids
                    cent = average(all class member)
        """
        k = self.k
        centroids = self.centroids
        data = self.data
        shape = self.shape
        n = data.shape[0]
        self.classAssign = np.zeros((n, 2))
        classAssign = self.classAssign
        flagCentrChange = True
        while flagCentrChange:
            # for z in range(3):
            flagCentrChange = False
            # Update data class
            for i in range(n):
                datapoint = data[i, :]
                # print '--debug--', datapoint, data, centroids
                distList = map((lambda x: dist(datapoint, x)), centroids)
                mindistIndex = np.argmin(distList)
                if mindistIndex != classAssign[i, 0]:
                    flagCentrChange = True
                classAssign[i] = [mindistIndex, distList[mindistIndex]]

            # Update centroids
            for i in range(k):
                # length n array of T/F
                classMem = map(
                    (lambda x: True if x[0] == i else False), classAssign)
                classMem = np.where(classMem)
                # part of data belongs to class i
                classMem = [data[j] for j in classMem]
                newCentroids = np.sum(classMem, 1) / float(len(classMem[0]))
                # print '-->' * 10
                # print 'classmember:\n', classMem
                # print 'len:\n', len(classMem[0])
                # print np.sum(classMem, 1)
                # print 'new centroid:\n', newCentroids[0]
                # print '--<' * 10
                self.centroids[i] = newCentroids[0]

    def predict(self, vec, dist=distEucld):
        dist = map((lambda x: dist(vec, x)), self.centroids)
        return np.argmin(dist)

    def printArgs(self):
        print 'Cluster number : ', self.k, ' Data shape: ', self.shape
        print 'Input data:\n', self.data
        print 'Centroids:\n', self.centroids
        print 'Cluster result:\n', '-----Class -- | ---Distance ----\n',\
            self.classAssign


def test():
    a = np.arange(30).reshape(5, 2, 3)
    kclf = kmeansAlg(k=2)
    kclf.fit(a)
    kclf.printArgs()
    print kclf.predict(np.array([[21, 22, 13], [13, 14, 15]]))


def main():
    test()

if __name__ == '__main__':
    main()
