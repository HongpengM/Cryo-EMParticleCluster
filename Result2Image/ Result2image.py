import h5py
import re
import os
import numpy as np
import matplotlib.pyplot as plt


def mergeMat(folder, namePattern):
    for name in os.listdir(folder):
        match = re.match(namePattern, name)
        if match:
            with h5py.File(os.path.join(folder, name), 'r') as f:
                n = len(f['MDF']['images'])
                shape = f['MDF']['images']['0']['image'].shape
                mat = np.zeros((n,) + shape)
                for i in range(n):
                    mat[i, :] = f['MDF']['images'][str(i)]['image']
    return mat


def outputImage(outFolder, mat, name='classResult'):

    fig = plt.figure(figsize=(10, 10), frameon=False)
    for i in range(mat.shape[0]):

        ax = fig.add_subplot(10, 10, i + 1, frameon=False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(mat[i], vmin=mat.min(), vmax=mat.max(), cmap=plt.cm.gray)
        ax.set_title('Class ' + str(i))
    plt.savefig(os.path.join(outFolder, name + '.png'))
    plt.show()


def test():
    mat = mergeMat('.', 'clusterResult_rotated_1000.hdf')
    print mat.shape
    outputImage('.', mat, 'skkmeans_masked_rotated_1000')


def main():
    test()

if __name__ == '__main__':
    main()
