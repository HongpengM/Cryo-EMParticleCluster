import numpy as np
import copy
from sklearn.cluster import KMeans


def skKmeans(data, cluster=8, random=0):
    return KMeans(n_clusters=cluster, random_state=random).fit(data)

distEucld = (lambda vecA, vecB:
             np.sqrt(np.sum(np.power(vecA.reshape(-1) -
                                     vecB.reshape(-1), 2))))

distAbs = (lambda vecA, vecB:
           np.sum(abs(vecA.reshape(-1) - vecB.reshape(-1))))


class ACKmeans(object):
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
        super(ACKmeans, self).__init__()
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

            sigma_zero: minimum fraction of data change criteria
            beta: the weight on the adaptive constraint term
            k: number of class

            # Initial assignment
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


            # Update cycle
            while sigma > sigma_0

                calculate the change of pixel intensity d_c
                by randome select images
                t_m = max dist(image_m, centroid) -
                                     min dist(image_m, centroid)
                d_c = average(t_m)
                lambda = d_c * beta / (2 * [n/k])
                class_Assignment_old = class_Assignment

                for each datapoint
                    s_prime = # other datapoint whose class is the same as
                                this one
                    update classAssignment

                update centroid
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

        #=====================Initialize=======================
        # Update data class
        for i in range(n):
            datapoint = data[i, :]
            # print '--debug--', datapoint, data, centroids
            distList = map((lambda x: dist(datapoint, x)), centroids)
            mindistIndex = np.argmin(distList)
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
            self.centroids[i] = newCentroids[0]
        #===================End Initialize=====================

        sigma_zero = 0.01
        sigma = 2 * sigma_zero
        pixelIntensityConstant = 10
        beta = 0.5
        #======================Update ==========================\
        # Calculate adaptive parameters
        # while sigma > sigma_zero:
        for _ in range(2):
            indexShuffle = np.arange(len(data))
            np.random.shuffle(indexShuffle)
            indexShuffle = indexShuffle[0:pixelIntensityConstant]
            t_mList = []
            for _i in indexShuffle:
                _tempDist = map((lambda x: dist(data[_i, :], x)),
                                centroids)
                t_mList.append(max(_tempDist) - min(_tempDist))
            d_c = np.average(t_mList)
            lambda_ = beta * d_c * 0.5 / np.floor(n / float(k))
            classAssignOld = copy.copy(classAssign)

        getAssignIndex = (lambda classAssign:
                          map((lambda x: x[0]),
                              classAssign))
        numberOfOthersInSameClass = (lambda thisClass, dpClass, classAssign:
                                     sum(
                                         map(
                                             (lambda x: 1 if x ==
                                              thisClass and x != dpClass else 0),
                                             getAssignIndex(classAssign)
                                         )
                                     )
                                     )
        # Update classAssignment
        for i in range(n):
            datapoint = data[i, :]
            # print '--debug--', datapoint, data, centroids
            distConstList = map(
                (lambda x: dist(datapoint, x)),
                centroids
            )

            adaptiveItem = map(
                (lambda x:
                 2 * lambda_ * numberOfOthersInSameClass(x, i, classAssign)),
                np.arange(k)
            )
            distList = map(
                (lambda x: x[0] + x[1]),
                zip(distConstList, adaptiveItem)
            )

            mindistIndex = np.argmin(distList)
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
            self.centroids[i] = newCentroids[0]

        print '-->' * 10

        print '--<' * 10
        sigma = 1 - np.average(
            map(
                (lambda x: 1 if x[0] == [1] else 0),
                zip(getAssignIndex(classAssign), getAssignIndex(classAssignOld))
            ))
        #====================End Update ==========================


    def predict(self, vec, dist=distEucld):
        dist = map((lambda x: dist(vec, x)), self.centroids)
        return np.argmin(dist)
        
    def printArgs(self):
        print 'Cluster number : ', self.k, ' Data shape: ', self.shape
        print 'Input data:\n', self.data
        print 'Centroids:\n', self.centroids
        print 'Cluster result:\n',
        '-----Class -- | ---Distance ----\n', self.classAssign


def test():
    a = np.arange(72).reshape(12, 2, 3)
    kclf = ACKmeans(k=3)
    kclf.fit(a)
    kclf.printArgs()
    print kclf.classAssign


def main():
    test()

if __name__ == '__main__':
    main()
