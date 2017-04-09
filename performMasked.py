import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('./HDF5Module')
sys.path.append('./KMeans')
import readh5
from sklearn.cluster import KMeans

with h5py.File('maskedImages.hdf', 'r') as h:
    data = np.zeros((len(h['images']),) + (180, 180))
    for i in range(len(h['images'])):
        data[i] = h['images'][str(i)]
print 'data shape', data.shape
print data[2]
data = data.reshape(data.shape[0], -1)
data = data[~np.isnan(data).any(axis=1)]
print np.isinf(data), np.sum(np.isinf(data))
print np.isnan(data), np.sum(np.isnan(data))
print data.shape
kclf = KMeans(n_clusters=100, random_state=0).fit(data)
pred = kclf.predict(data)
print pred, len(pred)
stacked = np.zeros((100,) + (data.shape[1],))
for i in range(100):
    if i in pred:
        index = np.where(pred == i)
        dt = [data[j] for j in index]
        stacked[i] = np.sum(dt[0], 0) / float(dt[0].shape[0])
result = h5py.File('clusterResult_masked.hdf', 'w')
result.create_group('MDF')
result['MDF'].create_group('images')
for i in range(stacked.shape[0]):
    images = result['MDF']['images']
    images.create_group(str(i))
    images[str(i)].create_dataset(
        'image',
        shape=(180, 180),
        dtype='float32',
        data=kclf.cluster_centers_[i, :].reshape(180, 180))
result.close()

# result = h5py.File('clusterResult.hdf', 'w')
# result.create_group('MDF')
# result['MDF'].create_group('images')
# for i in range(kclf.cluster_centers_.shape[0]):
#     images = result['MDF']['images']
#     images.create_group(str(i))
#     images[str(i)].create_dataset(
#         'image',
#         shape=(180, 180),
#         dtype='float32',
#         data=kclf.cluster_centers_[i, :].reshape(180, 180))
# result.close()
# print kclf.cluster_centers_.shape
