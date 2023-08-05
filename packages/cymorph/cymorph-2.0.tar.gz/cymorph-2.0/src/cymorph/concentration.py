from scipy import interpolate
import sep
import numpy as np


class Concentration:

    """
    Concentration(clean_image, radius1=0.8, radius2=0.2, rp=None, growth_curve=None, growth_radii=None)

    Extracts concentration metric from the supplied image. Additionally, can calculate petrosian
    radius, growth curve and growth radii if not supplied.

    Parameters
    ----------
    clean_image : 2-d `~numpy.ndarray`
        Clean image data array.
    radius1 : int, optional
        Value of outer radius that will enclose a give amount of galaxy flux. Default is 0.8 (80% of all flux).
    radius2 : int, optional
        Value of inner radius that will enclose a give amount of galaxy flux. Default is 0.2 (20% of all flux).
    rp : float, optional
        Value of petrosian radius in pixels. If not supplied, will be calculated at ETA=0.2.
    growth_curve : 1-d `~numpy.ndarray`
        Array of flux (in counts) growth curve of a galaxy. If not supplied, will be calculated.
    growth_radii : 1-d `~numpy.ndarray`
        Array of flux growth radii (in pixels) of a galaxy. This array should be the same length as `growth_curve`, where each value will correspond to flux value and respective radius that encloses it. If not supplied, will be calculated.
    """

    def __init__(self, clean_image, radius1=0.8, radius2=0.2, rp=None, growth_curve=None, growth_radii=None):
        if rp is not None and (growth_curve is None or growth_radii is None):
            raise ValueError(
                "rp should be supplied alongside with growth_curve and growth_radii")
        if rp is not None:
            if len(growth_curve) != len(growth_radii):
                raise ValueError(
                    "growth_curve and growth_radii should be of same length")

        self.clean_image = clean_image
        self.radius1 = radius1
        self.radius2 = radius2
        self.rp = rp
        self.growth_curve = growth_curve
        self.growth_radii = growth_radii

        if rp is None:
            # Subtract Background
            self.background = sep.Background(
                self.clean_image,
                bw=32,
                bh=32,
                fw=3,
                fh=3,
                fthresh=0.0,
                mask=None,
                maskthresh=0)

            self.image_no_background = self.clean_image - self.background

            # Get Object Shape Properties
            objs = sep.extract(
                self.image_no_background,
                thresh=1.5,
                err=self.background.globalrms,
                segmentation_map=False,
                gain=1.)

            dX = (objs['x'] - (len(self.image_no_background)/2))**2
            dY = (objs['y'] - (len(self.image_no_background)/2))**2

            distance = np.sqrt(dX + dY)

            self.obj = objs[distance == min(distance)]

            self.smax = int((len(self.image_no_background)) / self.obj['a'])
            self.smin = 1 / self.obj['a']
            self.step = 0.01

            # Estimate an Eta Profile to Define Petrosian Radius
            self._eta_func_ellipse()

    # calculates ETA profile

    def _eta_func_ellipse(self):
        self.growth_curve, self.etas = [], []
        numerators, denominators = [], []
        self.scales = np.arange(self.smin, self.smax, self.step)

        for s in self.scales:
            # numerators
            flux1, fluxerr1, flag1 = sep.sum_ellipse(self.image_no_background, self.obj['x'], self.obj['y'], (
                0.8 * s * self.obj['a']), (0.8 * s * self.obj['b']), self.obj['theta'])
            flux2, fluxerr2, flag2 = sep.sum_ellipse(self.image_no_background, self.obj['x'], self.obj['y'], (
                1.25 * s * self.obj['a']), (1.25 * s * self.obj['b']), self.obj['theta'])
            I = flux2 - flux1
            A1 = np.pi * (0.8 * s * self.obj['a']) * (0.8 * s * self.obj['b'])
            A2 = np.pi * (1.25 * s * self.obj['a']) * \
                (1.25 * s * self.obj['b'])
            numerator = I / (A2 - A1)
            numerators.append(float(numerator))

            # denominators
            flux3, fluxerr3, flag3 = sep.sum_ellipse(
                self.image_no_background, self.obj['x'], self.obj['y'], s * self.obj['a'], s * self.obj['b'], self.obj['theta'])
            self.growth_curve.append(float(flux3))

            A3 = np.pi * (s * self.obj['a']) * (s * self.obj['b'])
            denomenator = flux3/A3
            denominators.append(float(denomenator))
            self.etas.append(float(numerator/denomenator))

    def _interpolate_eta_ellipse(self):
        etas = np.array(self.etas)

        numbers_around = 5
        raio = self.scales * self.obj['a']
        e = etas[0]
        i = 0

        while e - 0.2 > 0:
            i = i+1
            e = etas[i]


        x = raio[i-numbers_around:i+numbers_around]
        y = etas[i-numbers_around:i+numbers_around]
        f1 = interpolate.splrep(x, y, k=3)
        xnew = np.linspace(min(x), max(x), num=10001, endpoint=True)
        ynew = interpolate.splev(xnew, f1, der=0)

        self.petrosian_radius = xnew[np.absolute(
            ynew - 0.2) == min(np.absolute(ynew - 0.2))]

    def _get_radii_values(self):
        growth_curve = np.asarray(self.growth_curve)
        numbers_around = 5
        curve = growth_curve[self.growth_radii <= 2 * self.petrosian_radius]
        radii = self.growth_radii[self.growth_radii <=
                                  2 * self.petrosian_radius]

        l_max = max(curve)

        indice = np.where(np.absolute((curve/l_max) - self.radius2)
                          == min(np.absolute((curve/l_max) - self.radius2)))[0][0]
        x = radii[indice - numbers_around: indice + numbers_around]
        y = curve[indice - numbers_around: indice + numbers_around]/l_max

        if len(x) < 10 or len(y) < 10:
            return np.nan, np.nan

        f1 = interpolate.splrep(x, y, k=3)
        xnew = np.linspace(min(x), max(x), num=10001, endpoint=True)
        ynew = interpolate.splev(xnew, f1, der=0)
        radius2_value = xnew[np.absolute(
            ynew - self.radius2) == min(np.absolute(ynew - self.radius2))]

        indice = np.where(np.absolute((curve/l_max) - self.radius1)
                          == min(np.absolute((curve/l_max) - self.radius1)))[0][0]
        x = radii[indice - numbers_around: indice + numbers_around]
        y = curve[indice - numbers_around: indice + numbers_around]/l_max
        f1 = interpolate.splrep(x, y, k=3)
        xnew = np.linspace(min(x), max(x), num=10001, endpoint=True)
        ynew = interpolate.splev(xnew, f1, der=0)
        radius1_value = xnew[np.absolute(
            ynew - self.radius1) == min(np.absolute(ynew - self.radius1))]

        return radius1_value, radius2_value

    def get_concentration(self):
        """
        Returns a concentration value

        Returns:
            concentration : `float`
        """
        if self.rp is None:
            # Interpolate Eta Profile to Get Exactly Eta = 0.2
            try:
                self._interpolate_eta_ellipse()
            except IndexError:
                raise ValueError('Unable to interpolate eta ellipse')

            # Define Growth Curve (acc.) and limit it to valid range
            self.growth_radii = self.scales * self.obj['a']

            radius1_value, radius2_value = self._get_radii_values()

            if radius1_value == np.nan:
                raise ValueError('Unable to calculate fraction of the flux in inner radius')
            elif radius2_value == np.nan:
                raise ValueError('Unable to calculate fraction of the flux in outer radius')
            else:
                return np.log10(radius1_value / radius2_value)[0]
        else:
            numbers_around = 5
            curve = self.growth_curve[self.growth_radii <= 2*self.rp]
            radii = self.growth_radii[self.growth_radii <= 2*self.rp]

            l_max = max(curve)

            indice = np.where(np.absolute((curve/l_max) - self.radius2)
                              == min(np.absolute((curve/l_max) - self.radius2)))[0][0]
            x = radii[indice - numbers_around: indice + numbers_around]
            y = curve[indice - numbers_around: indice + numbers_around]/l_max
            
            if len(x) < 10 or len(y) < 10:
                raise ValueError('Unable to calculate fraction of the flux in radius')

            f1 = interpolate.splrep(x, y, k=3)
            xnew = np.linspace(min(x), max(x), num=10001, endpoint=True)
            ynew = interpolate.splev(xnew, f1, der=0)
            r20 = xnew[np.absolute(ynew - self.radius2)
                       == min(np.absolute(ynew - self.radius2))]

            indice = np.where(np.absolute((curve/l_max) - self.radius1)
                              == min(np.absolute((curve/l_max) - self.radius1)))[0][0]
            x = radii[indice - numbers_around: indice + numbers_around]
            y = curve[indice - numbers_around: indice + numbers_around]/l_max
            f1 = interpolate.splrep(x, y, k=3)
            xnew = np.linspace(min(x), max(x), num=10001, endpoint=True)
            ynew = interpolate.splev(xnew, f1, der=0)
            r80 = xnew[np.absolute(ynew - self.radius1)
                       == min(np.absolute(ynew - self.radius1))]

            c = np.log10(r80/r20)

            return c[0]

    def get_petrosian_radius(self):
        """
        Return petrosian radius

        Returns:
            petrosian_radius : `float`
        """
        return self.petrosian_radius[0]