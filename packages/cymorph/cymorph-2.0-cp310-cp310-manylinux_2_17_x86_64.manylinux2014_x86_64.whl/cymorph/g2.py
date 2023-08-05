from cymorph.cython_g2 import G2 as g2_cython
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


class G2:
    """
    G2(segmented_image, g2_modular_tolerance=0.01, g2_phase_tolerance=0.01)

    Extracts entropy metric from the supplied image.

    Parameters
    ----------
    segmented_image : 2-d `~numpy.ndarray`
        Segmented image data array.
    g2_modular_tolerance : float, optional
        Modular tolerance. How much differences in vector modules will be acepted. Ranges from 0.0 (vectors should be same to count the same) 
        to 1.0 (any vectors will be counted as same). Default is 0.01.
    g2_phase_tolerance : float, optional
        Phase tolerance. How much differences in vector phases will be acepted. Ranges from 0.0 (vectors should be same to count the same) 
        to 3.14 (any vectors will be counted as same, even completly opposite). Default is 0.01.
    """

    def __init__(self, segmented_image, g2_modular_tolerance=0.01, g2_phase_tolerance=0.01) -> None:
        if segmented_image.ndim != 2:
            raise ValueError("array must be 2-d")
        if segmented_image.dtype != 'float32':
            raise ValueError("array must be np.float32")
        if segmented_image.shape[0] != segmented_image.shape[1]:
            raise ValueError("array must be square")
        if segmented_image.size == 0:
            raise ValueError("the size array can not be 0")
        if segmented_image.shape[0] % 2 == 0:
            raise ValueError("the stamp shape should be odd")

        self.segmented_image = segmented_image
        self.g2_modular_tolerance = g2_modular_tolerance
        self.g2_phase_tolerance = g2_phase_tolerance

    def _get_contour_count(self, image):
        # function that counts the contour pixels pixels
        filter = np.array([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])

        aux = (image.copy())
        aux[image != 0] = 1
        aux = aux.astype(int)
        conv = signal.convolve2d(aux, filter, mode='same')
        contourMask = aux * np.logical_and(conv > 0, conv < 4)

        return contourMask.sum()

    def get_g2(self):
        """
        Get a g2 metric.

        Returns:
            result_g2 : `float`
        """

        g2 = g2_cython(
            # need to pass a copy, if not, it is overwritten inside (strange)
            self.segmented_image.copy(),
            self._get_contour_count(self.segmented_image),
            self.g2_modular_tolerance,
            self.g2_phase_tolerance)

        try:
            self.result_g2, self.gradient_x, self.gradient_y, self.gradient_asymmetric_x, self.gradient_asymmetric_y, self.modules_normalized, self.phases = g2.get_g2()
        except ValueError:
            raise ValueError('Not enough valid pixels in image for g2 extraction')

        return self.result_g2

    def get_gradient_plot(self):
        """(Debugging routine) Gradient plot showing the vector field
        before removing symmetrical vector pairs"""
        figSize = 7
        fig, ax = plt.subplots(figsize=(figSize, figSize))

        x, y = np.meshgrid(np.arange(0, self.gradient_x.shape[1], 1), np.arange(
            0, self.gradient_y.shape[0], 1))
        ax.quiver(x, y, self.gradient_y, self.gradient_x)
        ax.tick_params(labelsize=16)

        return ax

    def get_asymmetry_gradient_plot(self):
        """(Debugging routine) Asymmetrical gradient plot showing the vector field
        after removing symmetrical vector pairs."""
        figSize = 7
        fig, ax = plt.subplots(figsize=(figSize, figSize))

        x, y = np.meshgrid(np.arange(0, self.gradient_asymmetric_x.shape[1], 1), np.arange(
            0, self.gradient_asymmetric_y.shape[0], 1))
        ax.quiver(x, y, self.gradient_asymmetric_y, self.gradient_asymmetric_x)
        ax.tick_params(labelsize=16)

        return ax
