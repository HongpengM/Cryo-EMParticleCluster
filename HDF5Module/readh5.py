"""
Read hdf5 file python interface
Input
path of hdf5 file folder
Output
A merged (number, dimension, dimension) matrix


Function:

Estimate size
    for file name in folder
        match name
        read number of box
    return sum number

Merge dataset
    First estimate the size of data
    for file name in folder
        match name
        read file
        write file
            /images
                /[number of line]
        output configure file
        filename [start, end)
    return stack matrix


"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import re
import os


def estimate(folderName, namePattern):
    cnt = 0
    for name in os.listdir(folderName):
        print name
        match = re.match(namePattern, name)
        if match:
            with h5py.File(os.path.join(folderName, name), 'r') as f:
                cnt += len(f['MDF']['images'])
    return cnt


def mergeDataSet(folderName, namePattern):
    """
        merge data in one folder
    """

    _TEMPFILE = os.path.join(folderName, 'lastRunResult.hdf')
    _TEMPCONFIG = os.path.join(folderName, '.lastConfigure')

    if os.path.isfile(_TEMPFILE):
        # estimateSize = estimate(folderName, namePattern)

        with h5py.File(_TEMPFILE, 'r') as temp:
            estimateSize = len(temp['images'])
            # print len(temp['images']), estimateSize
            # assert len(temp['images']) == estimateSize
            mergeMat = np.zeros((estimateSize, 180, 180))
            for i in range(estimateSize):
                mergeMat[i, :] = temp['images'][str(i)]
            print 'Successfully load data'
    else:
        estimateSize = estimate(folderName, namePattern)
        print estimateSize
        mergeMat = np.zeros((estimateSize, 180, 180))
        cnt = 0
        tempList = []
        for name in os.listdir(folderName):
            match = re.match(namePattern, name)
            if match:
                tempList.append((name, cnt))
                with h5py.File(os.path.join(folderName, name), 'r') as f:
                    for i in range(len(f['MDF']['images'])):
                        mergeMat[i, :] = f['MDF']['images'][str(i)]['image']
                    cnt += len(f['MDF']['images'])

                # [record: filename, [start number, end number]]
                tempList[-1] = tempList[-1] + (cnt, )
        if not os.path.isfile(_TEMPFILE):
            # write temp matrix
            h5py.File
            matrixResult = h5py.File(_TEMPFILE, 'w')
            matrixResult.create_group('images')
            for i in range(mergeMat.shape[0]):
                matrixResult['images'].create_dataset(str(i),
                                                      shape=(180, 180),
                                                      dtype='float32',
                                                      data=mergeMat[i, :])
            matrixResult.close()
            # write temp log filename
            with open(_TEMPCONFIG, 'w') as configure:
                for item in tempList:
                    configure.write(
                        str(item[0]) + ',' + str(item[1]) +
                        ',' + str(item[2]) + '\n')
    return mergeMat


def test():
    # print estimate('weinertest', r'(.*?)wiener\.hdf')
    # with h5py.File('weinertest/lastRunResult.hdf') as f:
    #     for i in f:
    #         print len(f[i])

    print os.path.curdir
    a = mergeDataSet('/home/k/GithubRepo/weiner', r'(.*?)wiener\.hdf')
    print a.shape
    print np.max(a[1, :]), np.min(a[1, :]), np.mean(a[1, :])


def main():
    test()

if __name__ == '__main__':
    main()
