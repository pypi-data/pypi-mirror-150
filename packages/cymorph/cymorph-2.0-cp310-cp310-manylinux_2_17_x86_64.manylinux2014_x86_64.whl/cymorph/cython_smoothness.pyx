import numpy as np
from libc.math cimport sqrt

from scipy import fftpack
from scipy.ndimage.filters import gaussian_filter

cimport numpy as np
cimport cython

# butterworth smoothing functions
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef float butterworth(float d,float d0,float n):
    return 1.0/(1.0+pow(d/d0,2.0*n))

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def filter_butterworth_2d(float[:,:] image, float smoothness_degradation, float butterworth_order, float smoothing_area):
    cdef:
        int heigth, width, i, j
        float[:,:] smooothed_image
        np.complex64_t[:,:]  freq

    heigth, width = len(image),len(image[0])

    smooothed_image = np.array([[0.0 for i in range(width)] for j in range(heigth)], dtype=np.float32)
    for i in range(heigth):
        for j in range(width):
            smooothed_image[i][j] = image[i][j]
            

    freq = fftpack.fft2(image)
    freq = fftpack.fftshift(freq)

    for i in range(heigth):
        for j in range(width):
            freq[i][j] = freq[i][j] * butterworth(sqrt(((float(i) - float(heigth) / 2.0)*(float(i) - float(heigth) / 2.0)) + ((float(j) - float(width) / 2.0)*(float(j) - float(width) / 2.0))) ,smoothness_degradation * smoothing_area, butterworth_order)
    
    smooothed_image = np.real(fftpack.ifft2(fftpack.ifftshift(freq))).astype(np.float32)
    
    return smooothed_image

############################################
# Smoothness (A) function:
# input:
#    image - 2d matrix of np.float32 type
#    smoothed_function - 2d matrix containing smoothed image
# return:
#    original_image_pixels - pixels that was collected from original image and have pair with rotated immage
#    rotated_image_pixels - pixels that was collected from rotated image and have pair with original immage
#    final_image - image that contains only pixels that were collected (i.e pairs)
#    collected_pixels_length - number of collected pixels in total
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def get_smoothness(float[:,:] image, float[:,:] smooothed_image):
    cdef:
        int w, h, valid_pixels, iteration, i, j, collected_pixels_length
        float[:,:] final_image
        float[:] original_image_pixels, smoothed_image_pixels
    w, h = len(image[0]), len(image)

    final_image = np.zeros(shape=(w, h), dtype=np.float32)
    valid_pixels = 0
    for i in range(w):
        for j in range(h):
            if(image[j, i] != 0.0):
                valid_pixels += 1
    
    # According to David(1938), a sample size equal or superior to 25 suffices.
    if(valid_pixels < 25):
        raise ValueError("Not enough valid pixels in image for correlation")
    
    original_image_pixels = np.zeros(shape=valid_pixels, dtype=np.float32)
    smoothed_image_pixels = np.zeros(shape=valid_pixels, dtype=np.float32)

    iteration = 0 
    for i in range(w):
        for j in range(h):
            if (image[j,i] != 0.0) and (smooothed_image[j,i] != 0.0):
                final_image[j,i] = image[j,i]
                original_image_pixels[iteration] = image[j,i]
                smoothed_image_pixels[iteration] = smooothed_image[j,i]
                iteration = iteration + 1

    collected_pixels_length = iteration

    return original_image_pixels, smoothed_image_pixels, final_image, collected_pixels_length