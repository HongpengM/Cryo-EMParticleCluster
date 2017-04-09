import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('./HDF5Module')
sys.path.append('./KMeans')
import readh5
from sklearn.cluster import KMeans
import scipy.ndimage
import scipy.misc
rotate = scipy.ndimage.interpolation.rotate
resize = scipy.misc.imresize

data = readh5.mergeDataSet('../weiner', r'(.*?)weiner\.hdf')
data2 = np.zeros((data.shape[0] * 8,) + (data.shape[1] / 3,) + (data.shape[2] / 3,))
for i in range(data.shape[0]):
    for j in range(8):
        datai = data[i]
        data2[8 * i + j] = resize(rotate(datai ,45 * j, reshape=False), (data.shape[1] / 3,) + (data.shape[2] / 3,))
    if i % 500 == 0:
        print i, 'rotated'    
with h5py.File('rotated.hdf','w') as h:
    h.create_group('images')
    for i in range(data.shape[0]):
        for j in range(8):
            h['images'].create_dataset(
                str(i) + '_' + str(j*45),
                shape=data2[8 * i + j, :].shape,
                dtype='float32',
                data=data2[8 * i + j, :])
