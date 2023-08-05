import numpy as np
from math import degrees

from libc.math cimport isnan, pow, abs, sqrt, atan2, M_PI, sin, cos, tan, ceil, floor
cdef extern from "numpy/npy_math.h":
    bint npy_isnan(double x)


cimport numpy as np
cimport cython

cdef class G2:
    # gradients
    cdef float[:,:] gradient_asymmetric_x, gradient_asymmetric_y
    cdef float[:,:] gradient_x, gradient_y
    cdef float[:,:] image, modules, phases

    cdef float[:,:] phases_noise, modules_noise, modules_normalized
    
    cdef int contour_pixels_count, valid_pixels_count, assimetric_pixel_count
    cdef int height, width, center_x, center_y

    cdef float phase_tolerance, module_tolerance
    cdef float f_nan
    
    def __cinit__(self, float[:,:] image, int contour_pixels_count, float module_tolerance, float phase_tolerance):
        self.image = image
        self.contour_pixels_count = contour_pixels_count
        self.phase_tolerance = phase_tolerance
        self.module_tolerance = module_tolerance
        self.height = len(image)
        self.width = len(image[0])
        self.center_x = <int>floor(self.height/2)
        self.center_y = <int>floor(self.width/2)
        self.f_nan = np.nan
        self.valid_pixels_count = 0
        self.assimetric_pixel_count = 0


    # debug method to add noise to phases
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    cdef float add_phase_noise(self):
        for i in range(self.width):
            for j in range(self.height):
                self.phases[i,j] = self.phases[i,j] + self.phases_noise[i,j]

    
    # debug method to add noise to modules
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    cdef float add_module_noise(self):
        for i in range(self.width):
            for j in range(self.height):
                self.modules_normalized[i,j] = self.modules_normalized[i,j] + self.modules_noise[i,j]
    

    # aux methods
    # add pi to phases, this is done to maintain phases 0-360 degrees
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    cdef float add_pi(self):
        for i in range(self.width):
            for j in range(self.height):
                self.phases[i,j] = self.phases[i,j] + M_PI

    # modules normalization by max module
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    cdef float normalize_modules(self):
        self.modules_normalized = np.zeros(shape=(self.width, self.height), dtype=np.float32)
        cdef float max_gradient = 0
        max_gradient = self.get_max_gradient()
        for i in range(self.width):
            for j in range(self.height):
                self.modules_normalized[i,j] = self.modules[i,j]/max_gradient
    
    # find maximum gradient
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cdef float get_max_gradient(self):
        cdef float max_gradient = -1.0
        cdef int i, j
        
        for i in range(self.width):
            for j in range(self.height):
                if not isnan(self.gradient_x[j,i]) and not isnan(self.gradient_y[j,i]):
                    if (max_gradient<0.0) or (sqrt(pow(self.gradient_y[j, i], 2.0)+pow(self.gradient_x[j, i], 2.0)) > max_gradient):
                        # modulo campo gradiente -> distancia euclidiana (maior modulo)
                        max_gradient = sqrt(pow(self.gradient_y[j, i],2.0)+pow(self.gradient_x[j, i],2.0))
        
        return max_gradient

    # simple function to get min between two numbers
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    cdef float min(self, float a, float b):
        if a < b:
            return a
        else:
            return b

    # function to find angle difference
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    cdef float angle_difference(self,float a1,float a2):
        # if it is in second quadrant - add pi
        if a1 >= M_PI/2 and a1 <= M_PI:
            return abs(round((a1 - (a2 - M_PI)),4)) 
        # if it is in first quadrant - substract pi pi
        else:
            return abs(round((a1 - (a2 + M_PI)),4)) 

    # function that converst 0 to non in matrix
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cdef void convert_to_nan(self):
        cdef int i, j
        for i in range(self.height):
            for j in range(self.width):
                if self.image[i,j] == 0:
                    self.image[i,j] = self.f_nan


    # function that constructs asymmetric field
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cdef void get_asymmetryc_field(self):
        cdef int[:] x, y
        cdef float[:,:] distance_from_center
        cdef float[:] uniq_distance_from_center
        cdef int i, j, pixel_pairs_count, distance
        

        self.gradient_asymmetric_x = self.gradient_x.copy()
        self.gradient_asymmetric_y = self.gradient_y.copy()

        # calculating phases
        self.phases = np.arctan2(self.gradient_x,self.gradient_y)
        # adding pi to maintaing everything in range 0 - 2pi (radians)
        self.add_pi()

        distance_from_center = np.array([[int(sqrt(pow(i-self.center_x, 2.0)+pow(j-self.center_y, 2.0))) for i in range(self.width)] for j in range(self.height)], dtype=np.float32)

        uniq_distance_from_center = np.unique(distance_from_center)

        # run for each distance from center
        for distance in range(len(uniq_distance_from_center)):
            # selects pixels with equal distances to see if they are symmetrical or not
            x, y = self.get_pixels_same_distance_from_center(distance_from_center, distance)
            pixel_pairs_count = len(x)
            
            
            # compare each point in the same distance
            # verifica se os pixeis sao simetricos ou nao
            for i in range(pixel_pairs_count):
                if isnan(self.image[x[i], y[i]]):
                    continue
                
                if (self.modules_normalized[x[i], y[i]] <= self.module_tolerance):
                    # if vector is too small, it is considered symmetric
                    self.gradient_asymmetric_x[x[i], y[i]] = self.f_nan
                    self.gradient_asymmetric_y[x[i], y[i]] = self.f_nan
                
                # getting opposite pixel
                opposite_pixel = self.get_opposite_pixel(x[i], y[i])
                
                if opposite_pixel[0] == -1:
                    continue
                if isnan(self.image[opposite_pixel[0], opposite_pixel[1]]):
                    continue

                if (self.modules_normalized[opposite_pixel[0], opposite_pixel[1]] <= self.module_tolerance):
                    # if vector is too small, it is considered symmetric
                    self.gradient_asymmetric_x[opposite_pixel[0], opposite_pixel[1]] = self.f_nan
                    self.gradient_asymmetric_y[opposite_pixel[0], opposite_pixel[1]] = self.f_nan

                if (abs(self.modules_normalized[x[i], y[i]] - self.modules_normalized[opposite_pixel[0], opposite_pixel[1] ]) <= self.module_tolerance):
                    if (self.angle_difference(self.phases[x[i], y[i]], self.phases[opposite_pixel[0], opposite_pixel[1]])  <= self.phase_tolerance):
                       
                        self.gradient_asymmetric_x[x[i], y[i]] = self.f_nan
                        self.gradient_asymmetric_y[x[i], y[i]] = self.f_nan
                        self.gradient_asymmetric_x[opposite_pixel[0], opposite_pixel[1]] = self.f_nan
                        self.gradient_asymmetric_y[opposite_pixel[0], opposite_pixel[1]] = self.f_nan
    
    # function that return (if such) opposite pixel
    cdef tuple get_opposite_pixel(self, int pixel_x, int pixel_y):
        #0 - x; 1 - y
        cdef int opposite_pixel_x=-1, opposite_pixel_y=-1
        cdef int distance_from_center_x, distance_from_center_y
        
        #check quadrand, ignore third and fourth as there will be located opposites
        if pixel_x > self.center_x and pixel_y < self.center_y:
            distance_from_center_x = self.center_x - pixel_x
            distance_from_center_y = self.center_y - pixel_y
            opposite_pixel_x = self.center_x + distance_from_center_x
            opposite_pixel_y = self.center_y + distance_from_center_y
            
            #print('first quadrant, opposite in third qudrant')
            #quadrand, opposite_quandrant = 1,4
        
        elif pixel_x < self.center_x and pixel_y < self.center_y:
            distance_from_center_x = self.center_x - pixel_x
            distance_from_center_y = self.center_y - pixel_y
            opposite_pixel_x = self.center_x + distance_from_center_x
            opposite_pixel_y = self.center_y + distance_from_center_y
        #     #print('second quadrant, opposite in fourth qudrant')
        #     #quadrand, opposite_quandrant = 2,3
        
        elif pixel_x < self.center_x and pixel_y > self.center_y:
            #print('third quadrant - ignore')
            pass
        
        elif pixel_x > self.center_x and pixel_y > self.center_y:
            #print('fourth quadrant - ignore')
            pass
        
        elif pixel_x == self.center_x and pixel_y > self.center_y:
            distance_from_center_x = self.center_x - pixel_x
            distance_from_center_y = self.center_y - pixel_y
            opposite_pixel_x = self.center_x + distance_from_center_x
            opposite_pixel_y = self.center_y + distance_from_center_y
            #print('on same x axis, but ontop of center')

        elif pixel_x == self.center_x and pixel_y < self.center_y:
            distance_from_center_x = self.center_x - pixel_x
            distance_from_center_y = self.center_y - pixel_y
            opposite_pixel_x = self.center_x + distance_from_center_x
            opposite_pixel_y = self.center_y + distance_from_center_y
            #print('on same x axis, but below of center')
            

        elif pixel_x > self.center_x and pixel_y == self.center_y:
            distance_from_center_x = self.center_x - pixel_x
            distance_from_center_y = self.center_y - pixel_y
            opposite_pixel_x = self.center_x + distance_from_center_x
            opposite_pixel_y = self.center_y + distance_from_center_y
            #print('on same y axis, but right of center')
            
        elif pixel_x < self.center_x and pixel_y == self.center_y:
            distance_from_center_x = self.center_x - pixel_x
            distance_from_center_y = self.center_y - pixel_y
            opposite_pixel_x = self.center_x + distance_from_center_x
            opposite_pixel_y = self.center_y + distance_from_center_y
            #print('on same y axis, but left of center')
    
        return opposite_pixel_x, opposite_pixel_y

    # getting list of pixels that have same distance from center
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cdef tuple get_pixels_same_distance_from_center(self, float[:,:] distance_from_center, int distance):
        cdef int px, py
        cdef int[:] x, y
        x2,y2 = [],[]

        for py in range(self.height):
            for px in range(self.width):
                # 0 means that take only pixels of specific distance from the center
                if (abs(distance_from_center[py, px] - distance) == 0):
                    x2.append(px)
                    y2.append(py)
            
        x, y = np.array(x2, dtype=np.int32), np.array(y2, dtype=np.int32)
        return (x,y)

    # calculating confluence
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cdef float get_confluence(self):
        cdef float sum_x_vectors = 0.0
        cdef float sum_y_vectors = 0.0
        cdef float sum_modules = 0.0
        cdef float aux_mod = 0.0
        cdef float confluence = 0.0

        for j in range(self.height):
            for i in range(self.width):
                if (not isnan(self.gradient_asymmetric_y[j,i])) and (not isnan(self.gradient_asymmetric_x[j,i])) and (not isnan(self.image[j,i])):
                    aux_mod = self.modules[j,i]
                    sum_x_vectors += self.gradient_asymmetric_x[j,i]
                    sum_y_vectors += self.gradient_asymmetric_y[j,i]
                    sum_modules += aux_mod

                    self.assimetric_pixel_count = self.assimetric_pixel_count + 1
                    self.valid_pixels_count = self.valid_pixels_count + 1
                elif not isnan(self.image[j,i]):
                    self.valid_pixels_count = self.valid_pixels_count + 1
        
        # if valid pixels does not cover the whole image, substract the contour pixels
        if self.valid_pixels_count != self.height*self.width:
            self.valid_pixels_count = self.valid_pixels_count - self.contour_pixels_count
        
        # if there is no assimetric modules, confluence is 0
        if self.assimetric_pixel_count == 0:
            return 0.0
        
        confluence = sqrt(pow(sum_x_vectors, 2.0) + pow(sum_y_vectors, 2.0)) / sum_modules
        
        return confluence
    
    # entry point
    def get_g2(self):
        cdef int  i, j
        cdef float confluence, g2

        self.convert_to_nan()

        self.gradient_x, self.gradient_y = np.gradient(self.image)
        
        self.modules = np.array([[sqrt(pow(self.gradient_y[j, i],2.0)+pow(self.gradient_x[j, i],2.0)) for i in range(self.width) ] for j in range(self.height)], dtype=np.float32)
        self.normalize_modules()
        
        self.get_asymmetryc_field()

        confluence = self.get_confluence()
        if float(self.valid_pixels_count) > 0:
            g2 = (float(self.assimetric_pixel_count) / float(self.valid_pixels_count)) * (2.0 - confluence)
        else:
            raise ValueError('Not enough valid pixels in image for g2 extraction')

        return g2, self.gradient_x, self.gradient_y, self.gradient_asymmetric_x, self.gradient_asymmetric_y, self.modules_normalized, self.phases