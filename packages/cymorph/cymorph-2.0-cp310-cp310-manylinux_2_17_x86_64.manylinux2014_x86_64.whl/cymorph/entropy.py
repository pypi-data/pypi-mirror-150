from cymorph.cython_entropy import get_entropy
import matplotlib.pyplot as plt
import seaborn as sns


class Entropy:
    """
    Entropy(segmented_image, entropy_bins=130)

    Extracts entropy metric from the supplied image.

    Parameters
    ----------
    segmented_image : 2-d `~numpy.ndarray`
        Segmented image data array.
    entropy_bins : int, optional
        Number of bins to split image data. Default is 130
    """

    def __init__(self, segmented_image, entropy_bins=130):
        if segmented_image.ndim != 2:
            raise ValueError("array must be 2-d")
        if segmented_image.dtype != 'float32':
            raise ValueError("array must be np.float32")
        if segmented_image.shape[0] != segmented_image.shape[1]:
            raise ValueError("array must be square")
        if segmented_image.size == 0:
            raise ValueError("the size array can not be 0")

        self.segmented_image = segmented_image
        self.entropy_bins = entropy_bins

    def get_bins_plot(self):
        """(Debugging routine) Histogram plot showing the flux distribution"""
        line = self.segmented_image.flatten()
        line = line[line != 0]

        px = 1/plt.rcParams['figure.dpi']  # pixel in inches
        # coluna, linha
        fig_size = (500*px, 500*px)
        f, ax = plt.subplots(figsize=fig_size)
        ax = sns.histplot(line, kde=True, binwidth=50)
        ax.set_xlabel('Flux value', fontsize=20)
        ax.set_ylabel('Frequency', fontsize=20)
        ax.tick_params(labelsize=16)

        return ax

    def get_entropy(self):
        """
        Get entropy metric.

        Returns:
            entropy_metric : `float`
        """
        return get_entropy(self.segmented_image, self.entropy_bins)
