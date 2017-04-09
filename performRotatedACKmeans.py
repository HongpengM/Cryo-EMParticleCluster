import sys
sys.path.append('./KMeans')
from ACKmeans import ACKmeans
import numpy as np
import h5py
import matplotlib.pyplot as plt
import sys
sys.path.append('./HDF5Module')
import readh5


# a = np.arange(72).reshape(12, 2, 3)
# kclf = ACKmeans(k=3)
# kclf.fit(a)
# print kclf.predict(a)


with h5py.File('rotated.hdf', 'r') as h:
    data = np.zeros((len(h['images']),) + (60, 60))
    for i in range(len(h['images']) / 8):
        for j in range(8):
            data[i * 8 + j] = h['images'][str(i) + '_' + str(45 * j)]
print 'data shape', data.shape

print data[2]
data = data.reshape(data.shape[0], -1)
data = data[~np.isnan(data).any(axis=1)]
print np.isinf(data), np.sum(np.isinf(data))
print np.isnan(data), np.sum(np.isnan(data))


data = data[0:5000]
print data.shape
kclf = ACKmeans(k=100)
kclf.fit(data)
pred = kclf.predict(data)
print pred, len(pred)
stacked = np.zeros((100,) + (data.shape[1],))
for i in range(100):
    if i in pred:
        index = np.where(pred == i)
        dt = [data[j] for j in index]
        stacked[i] = np.sum(dt[0], 0) / float(dt[0].shape[0])
result = h5py.File('clusterResult_rotated_ackmeans_5000.hdf', 'w')
result.create_group('MDF')
result['MDF'].create_group('images')
for i in range(stacked.shape[0]):
    images = result['MDF']['images']
    images.create_group(str(i))
    images[str(i)].create_dataset(
        'image',
        shape=(60, 60),
        dtype='float32',
        data=kclf.centroids[i].reshape(60, 60))
result.close()
