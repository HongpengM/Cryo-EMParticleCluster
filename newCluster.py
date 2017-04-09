import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('./HDF5Module')
sys.path.append('./KMeans')
import readh5
from sklearn.cluster import KMeans
data = readh5.mergeDataSet('../weiner', r'(.*?)weiner\.hdf')
