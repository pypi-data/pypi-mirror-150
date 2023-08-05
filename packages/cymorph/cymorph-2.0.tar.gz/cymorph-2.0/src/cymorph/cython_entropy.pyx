import numpy as np

from libc.math cimport log10

cimport numpy as np
cimport cython

############################################
# Entropy (H) function:
# input:
#    image - matrix of 2d np.float32
#    number_bins - integer, number of number_bins to spliteration the histogram
# return:
#    coeficient - entropy value
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef float get_entropy(float[:,:] image, int number_bins):
    cdef:
        float[:] freq, line, bins
        long[:] counts
        float somatorio, entropy_coeficient
        int i
    
    line = ravel(image)

    freq = np.array([0.0 for i in range(number_bins)], dtype=np.float32)
    counts, bins = np.histogram(line, number_bins)
    
    somatorio = 0.0
    for i in range(number_bins):
        somatorio = somatorio + counts[i]
    
    for i in range(number_bins):
        freq[i] = float(counts[i]) / float(somatorio)
    
    somatorio = 0.0
    for i in range(number_bins):
        if freq[i]>0.0:
            somatorio = somatorio - freq[i] * log10(freq[i])
    
    entropy_coeficient = somatorio/log10(number_bins)
    
    return entropy_coeficient

############################################
# Array Ravel (fletten) function:
# input:
#    image - matrix of 2d np.float32
# return:
#    line - 1d version of input array
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef float[:] ravel(float[:,:] image):
    cdef:
          int w, h, valid_pixels, j, i, iteration
          float[:] line
    
    w, h = len(image[0]), len(image)
    
    valid_pixels = 0
    for i in range(w):
        for j in range(h):
            if(image[j, i] != 0.0):
               valid_pixels = valid_pixels + 1
    
    line = np.zeros(shape=valid_pixels, dtype=np.float32)

    iteration = 0
    for i in range(w):
        for j in range(h):
            if(image[j, i] != 0.0):
                line[iteration] = image[j, i]
                iteration = iteration + 1 
    
    return line