import numpy as np

cimport numpy as np
cimport cython

############################################
# Asymmetry (A) function:
# input:
#    image - image - 2d matrix of np.float32 type
# return:
#    original_image_pixels - pixels that was collected from original image and have pair with rotated immage
#    rotated_image_pixels - pixels that was collected from rotated image and have pair with original immage
#    rotated_image - roteted version of original image
#    final_image - image that contains only pixels that were collected (i.e pairs)
#    collected_pixels_length - number of collected pixels in total
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef get_asymmetry(float[:,:] image):
    cdef:
         float[:,:]  rotated_image, final_image
         int w, h, collected_pixels_length, valid_pixels
    w, h = len(image[0]), len(image)

    rotated_image = np.rot90(image,2)
    final_image = np.zeros(shape=(w, h), dtype=np.float32)
    
    valid_pixels = 0
    for i in range(w):
        for j in range(h):
            if(image[j, i] != 0.0):
                valid_pixels += 1
    
    # According to David(1938), a sample size equal or superior to 25 suffices.
    if(valid_pixels < 25):
        raise ValueError("Not enough valid pixels in image for correlation")

    collected_pixels_length = 0
    original_image_pixels = []
    rotated_image_pixels = []

    for i in range(w):
        for j in range(h):
            if (image[j,i] != 0) and (rotated_image[j,i] != 0):
                final_image[j,i] = image[j,i]
                original_image_pixels.append(image[j,i])
                rotated_image_pixels.append(rotated_image[j,i])
    
    collected_pixels_length = len(original_image_pixels)
    
    return original_image_pixels, rotated_image_pixels, rotated_image, final_image, collected_pixels_length
