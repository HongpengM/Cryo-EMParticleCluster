import numpy as np
import os
import mrc
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import re


def fft2(mat, shape=None):
    if shape:
        return np.fft.fft2(mat, shape)
    else:
        return np.fft.fft2(mat)


def fourier2abs(mat):
    return np.abs(np.fft.fftshift(mat))


def ctf(param):


def ifft2(mat, shape=None):
    if shape:
        return np.fft.ifft2(mat, shape)
    else:
        return np.fft.ifft2(mat)


def test():
    pass


def main():
    test()

if __name__ == '__main__':
    main()
