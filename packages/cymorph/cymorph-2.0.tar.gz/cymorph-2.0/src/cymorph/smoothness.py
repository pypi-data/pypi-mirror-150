from cymorph.cython_smoothness import get_smoothness, filter_butterworth_2d
from scipy.stats.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt


class Smoothness:
    """
    Smoothness(clean_image, segmented_mask, smoothing_degradation, butterworth_order)

    Extracts smoothness metric (pearson rank and spearman rank) from the supplied image.

    Parameters
    ----------
    clean_image : 2-d `~numpy.ndarray`
        Clean image data array.
    segmented_mask : 2-d `~numpy.ndarray`
        Mask array.
    smoothing_degradation : float
        Degradation level of the image.
    butterworth_order : int
        Butterworth order.
    """

    def __init__(self, clean_image, segmented_mask, smoothing_degradation, butterworth_order):
        if clean_image.ndim != 2:
            raise ValueError("array must be 2-d")
        if clean_image.dtype != 'float32':
            raise ValueError("array must be np.float32")
        if clean_image.shape[0] != clean_image.shape[1]:
            raise ValueError("array must be square")
        if clean_image.size == 0:
            raise ValueError("the size array can not be 0")

        self.segmented_image = clean_image * segmented_mask
        self.clean_image = clean_image
        self.segmented_mask = segmented_mask
        self.smoothing_degradation = smoothing_degradation
        self.butterworth_order = butterworth_order
        self.height, self.width = self.clean_image.shape

        self._smoothness()

    def _smoothness(self):
        self.smoothed_image = self._get_smoothed_image()
        try:
            self.smoothness_v1, self.smoothness_v2, self.final_image, self.collected_points = get_smoothness(
                self.segmented_image, self.smoothed_image)
        except ValueError:
            raise ValueError(
                "Not enough valid pixels in image for correlation")

    def get_collected_points_plot(self):
        """Correlation plot between original and rotated image"""
        px = 1/plt.rcParams['figure.dpi']  # pixel in inches
        # coluna, linha
        fig_size = (500*px, 500*px)
        f, ax = plt.subplots(figsize=fig_size)
        ax.set_xlabel('Original image', fontsize=20)
        ax.set_ylabel('Smoothed image', fontsize=20)
        ax.tick_params(labelsize=16)
        ax.scatter(self.smoothness_v1, self.smoothness_v2, s=10, alpha=0.5)

        return ax

    def _get_smoothed_image(self):
        smoothed_image_aux = filter_butterworth_2d(
            self.clean_image, self.smoothing_degradation, self.butterworth_order, self.height/2)

        return smoothed_image_aux * self.segmented_mask

    def get_pearsonr(self):
        """
        Pearson rank smoothness coeficient

        Returns:
            Pearson rank smoothness coeficient : `float`
        """
        
        symmetry_pearsonr_correlation_coeficient = pearsonr(
                self.smoothness_v1, self.smoothness_v2)[0]

        return (1 - symmetry_pearsonr_correlation_coeficient)

    def get_spearmanr(self):
        """
        Spearman rank smoothness coeficient

        Returns:
            Spearman rank smoothness coeficient : `float`
        """

        symmetry_spearmanr_correlation_coeficient = spearmanr(
                self.smoothness_v1, self.smoothness_v2)[0]


        return (1 - symmetry_spearmanr_correlation_coeficient)
