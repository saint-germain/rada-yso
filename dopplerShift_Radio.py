from __future__ import print_function, division
import scipy.interpolate as sci
import numpy as np
#from PyAstronomy.pyaC import pyaErrors as PE
#import six.moves as smo


def dopplerShiftFreqRadio(Freq, flux, v, edgeHandling=None, fillValue=None, vlim=0.05):
    """
    Doppler shift a given spectrum.
    An algorithm to apply a Doppler shift
    to a spectrum. The idea here is to obtain a shifted spectrum
    without loosing the wavelength axis. Therefore,
    this function, first, calculates
    the shifted wavelength axis and, second, obtains
    the new, shifted flux array at the old, unshifted
    wavelength points by linearly interpolating. No
    relativistic effects are considered.
    Due to the shift, some bins at the edge of the
    spectrum cannot be interpolated, because they
    are outside the given input range. The default
    behavior of this function is to return numpy.NAN
    values at those points. One can, however, specify
    the `edgeHandling` parameter to choose a different
    handling of these points.
    If "firstlast" is specified for `edgeHandling`,
    the out-of-range points at the red or blue edge
    of the spectrum will be filled using the first
    (at the blue edge) and last (at the red edge) valid
    point in the shifted, i.e., the interpolated, spectrum.
    If "fillValue" is chosen for edge handling,
    the points under consideration will be filled with
    the value given through the `fillValue` keyword.
    .. warning:: Shifting a spectrum using linear
                interpolation has an effect on the
                noise of the spectrum. No treatment
                of such effects is implemented in this
                function.
    Parameters
    ----------
    Freq : array
        Input wavelengths in A.
    flux : array
        Input flux.
    v : float
        Doppler shift in km/s
    edgeHandling : string, {"fillValue", "firstlast"}, optional
        The method used to handle the edges of the
        output spectrum.
    fillValue : float, optional
        If the "fillValue" is specified as edge handling method,
        the value used to fill the edges of the output spectrum.
    vlim : float, optional
        Maximal fraction of the speed of light allowed for Doppler
        shift, v. Default is 0.05.
    Returns
    -------
    nflux : array
        The shifted flux array at the *old* input locations.
    Freq_prime : array
        The shifted wavelength axis.
    """
    # Order check
    if np.any(np.diff(Freq) < 0.0):
        print("Wavelength axis must be sorted in ascending order. ","Use sorted axis.")
        
    # Speed of light [km/s]
    cvel = 299792.458
    
    if np.abs(v) > vlim*cvel:
        print("Specified velocity of % g km/s exceeds %g %% of the speed of light. No relativistic effects are considered in this implementation. " % (v, vlim*100.),"dopplerShiftFreqRadio ", \
                             "Increase 'vlim' if you wish to suppress this error.")
    
    # Shifted wavelength axis
    Freq_prime = Freq / (1.0 - (v / cvel))

    # Overlap check
    if (Freq_prime[0] >= Freq[-1]) or (Freq_prime[-1] <= Freq[0]):
        print("The shifted wavelength axis shows no overlap with the input axis. The velocity shift of %g km/s is too large. " % v, \
                             "dopplerShiftFreqRadio ", "Use smaller shifts ", "Please consider another implementation. Also note that the treatment here is not relativistic.")

    fv = np.nan
    if edgeHandling == "fillValue":
        if fillValue is None:
            print("Fill value not specified ","pyasl.dopplerShiftFreqRadio ","If you request 'fillValue' as edge handling method, you need to specify the 'fillValue' keyword.")
        fv = fillValue

    f = sci.interp1d(Freq_prime, flux, bounds_error=False, fill_value=fv)
    nflux = f(Freq)

    if edgeHandling == "firstlast":
        # Not is-NaN
        nin = ~np.isnan(nflux)
        if not nin[0]:
            # First element in invalid (NaN)
            # Find index of first valid (not NaN) element
            fvindex = np.argmax(nin)
            # Replace leading elements
            nflux[0:fvindex] = nflux[fvindex]
        if not nin[-1]:
            # Last element is invalid
            # Index of last valid element
            lvindex = -np.argmax(nin[::-1])-1
            # Replace trailing elements
            nflux[lvindex+1:] = nflux[lvindex]

    return nflux, Freq_prime
