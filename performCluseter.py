import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('./HDF5Module')
sys.path.append('./KMeans')
import readh5
from sklearn.cluster import KMeans

data = readh5.mergeDataSet('../../weiner', r'(.*?)weiner\.hdf')
data = data.reshape(data.shape[0], -1)
data = data[~np.isnan(data).any(axis=1)]
print np.isinf(data), np.sum(np.isinf(data))
print np.isnan(data), np.sum(np.isnan(data))
kclf = KMeans(n_clusters=30, random_state=0).fit(data)
result = h5py.File('clusterResult.hdf', 'w')
result.create_group('MDF')
result['MDF'].create_group('images')
for i in range(kclf.cluster_centers_.shape[0]):
    images = result['MDF']['images']
    images.create_group(str(i))
    images[str(i)].create_dataset(
        'image',
        shape=(180, 180),
        dtype='float32',
        data=kclf.cluster_centers_[i, :].reshape(180, 180))
result.close()
print kclf.cluster_centers_.shape
