from cymorph.cython_asymmetry import get_asymmetry
from scipy.stats.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

class Asymmetry:
    """
    Asymmetry(image)

    Extracts assimetry metrics (pearson rank and spearman rank) from the supplied image.

    Parameters
    ----------
    segmented_image : 2-d `~numpy.ndarray`
        Data array.
    """

    def __init__(self, segmented_image):
        if segmented_image.ndim != 2:
            raise ValueError("array must be 2-d")
        if segmented_image.dtype != 'float32':
            raise ValueError("array must be np.float32")
        if segmented_image.shape[0] != segmented_image.shape[1]:
            raise ValueError("array must be square")
        if segmented_image.size == 0:
            raise ValueError("the size array can not be 0")

        self.segmented_image = segmented_image
        self._asymmetry()

    def _asymmetry(self):
        try:
            self.asymmetry_v1, self.asymmetry_v2, self.rotated_image, self.final_image, self.collected_points = get_asymmetry(
                self.segmented_image)
        except ValueError:
            raise ValueError("Not enough valid pixels in image for correlation")

    def get_collected_points_plot(self):
        """(Debugging routine) Correlation plot between original and rotated image"""
        px = 1/plt.rcParams['figure.dpi']  # pixel in inches

        # coluna, linha
        fig_size = (500*px, 500*px)
        f, ax = plt.subplots(figsize=fig_size)
        ax.set_xlabel('Original image', fontsize=20)
        ax.set_ylabel('Rotated image', fontsize=20)
        ax.tick_params(labelsize=16)
        ax.scatter(self.asymmetry_v1, self.asymmetry_v2, s=10, alpha=0.5)

        return ax

    def get_pearsonr(self):
        """
        Pearson rank asymmetry coeficient

        Returns:
            Pearson rank asymmetry coeficient : `float`
        """
        symmetry_pearsonr_correlation_coeficient = pearsonr(
            self.asymmetry_v1, self.asymmetry_v2)[0]

        return (1 - symmetry_pearsonr_correlation_coeficient)

    def get_spearmanr(self):
        """
        Spearman rank asymmetry coeficient
        
        Returns:
            Spearman rank asymmetry coeficient : `float`
        """

        symmetry_spearmanr_correlation_coeficient = spearmanr(
            self.asymmetry_v1, self.asymmetry_v2)[0]

        return (1 - symmetry_spearmanr_correlation_coeficient)