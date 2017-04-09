import h5py

result = h5py.File('clusterResult.hdf', 'r')

print type(result['MDF']['images']['0']['image'])
print result['MDF']['images']['0']['image'].shape

result.close()
