import numpy as np
import scipy.ndimage
import scipy.spatial

import skimage.feature
import skimage.filters
import skimage.morphology
import skimage.segmentation

import bokeh.layouts
import bokeh.models
import bokeh.plotting


def good_frames(ic, frac_diff=0.95, bad_frames=[], return_covs=False):
    """
    Determine which frames in an list of images are in focus.

    Parameters
    ----------
    ic : list of ndarrays
        List of images. This is *not* a skimage.ImageCollection.
    frac_diff : float, default = 0.95
        Frames whose coefficient of variation is less than frac_diff
        times the mean of the coefficient of variation of all frames
        are considered bad.
    bad_frame : list, default []
        List of indices of frames that are known to be bad.
    return_covs : bool
        If True, also return coefficients of varation of frames.

    Returns
    -------
    output : list of ints
        List of indices of good frames.
    covs : ndarray, only returns if return_covs is True
        Array of coefficient of variation of each frame.
    """
    covs = np.array([im.std() / im.mean() for im in ic])
    thresh = frac_diff * covs.mean()
    gf = [i for i in range(len(ic)) if covs[i] > thresh and i not in bad_frames]

    if return_covs:
        return gf, covs
    else:
        return gf


def cross_corr(im_1_fft, im_2_fft):
    """
    Find shift from im_1 to im_2 that maximizes cross-correlation

    Parameters
    ----------
    im_1 : ndarray
        2D FFT of first image
    im_2 : ndarray
        2D FFT of second image

    Returns
    -------
    output : ndarray, shape (2,)
        Shift in the row, column direction of one image to the next.
        This is given to integer pixel accuracy.
    """
    # Compute correlation using spectral theorem
    ccoeff = np.fft.fftshift((np.fft.ifft2(np.conj(im_1_fft) * im_2_fft)).real)

    # Normalize and find maximum
    if not (ccoeff == 0.0).all():
        ccoeff /= ccoeff.max()  # Normalize
    max_ind = np.nonzero(ccoeff == ccoeff.max())

    # Return shift
    return np.array(
        [max_ind[0][0] - im_1_fft.shape[0] // 2, max_ind[1][0] - im_1_fft.shape[1] // 2]
    )


def drift_correct(ic):
    """
    Perform drift correction by cross-correlation with the first frame.

    Parameters
    ----------
    ic : list of ndarrays
        List of images.

    Returns
    -------
    output : list of ndarrays
        Zero-padded drift-corrected images.
    max_shift : int
        Maximum shift in any direction.
    """

    # Compute FFTs of all images
    ic_fft = [np.fft.fft2(im) for im in ic]

    ic_out = [ic[0]]
    max_shift = 0
    for i, im in enumerate(ic[1:]):
        shift = cross_corr(ic_fft[0], ic_fft[i])
        pad = np.abs(shift).max()

        if pad > max_shift:
            max_shift = pad

        im_out = np.pad(im, pad, "constant")
        ic_out.append(
            im_out[
                pad + shift[0] : pad + shift[0] + im.shape[0],
                pad + shift[1] : pad + shift[1] + im.shape[1],
            ]
        )

    return ic_out, max_shift


def preprocess(im, sigma=1, selem_width=5, neg_im=False):
    """
    Perform bluring and background subtraction of image.

    Parameters
    ----------
    im : ndarray
        Image to preprocess.
    sigma : float
        The characteristic length scale of noise in the images
        in units of pixels.  This is used to set the sigma value
        in the Gaussian blur.
    selem_width : int
        Width of square structuring element for mean filter.  Should be an
        odd integer greater than the pixel radius, but smaller than
        interparticle distance.
    neg_im : bool
        If True, use the negative of the image.

    Returns
    -------
    output : ndarray, shape as im, dtype float
        Blurred, background subtracted image.
    """

    # Convert image to float
    im = skimage.img_as_float(im)

    # Make the negative
    if neg_im:
        im = im.max() - im

    # Set up structuring element
    selem = skimage.morphology.square(selem_width)

    # Perform a mean filter (this is much faster than skimage.filters.rank.mean)
    im_bg = scipy.ndimage.uniform_filter(im, selem_width)

    # Gaussian blur
    im_blur = skimage.filters.gaussian(im, sigma)

    # Background subtract
    bg_subtracted_image = im_blur - im_bg

    # Return with negative pixels set to zero
    return np.maximum(bg_subtracted_image, 0)


def get_peaks(im, particle_size=3, thresh_abs=None, thresh_perc=None, border=0):
    """
    Find local maxima in pixel intensity.  Designed for use
    with images containing particles of a given size.

    Parameters
    ----------
    im : array_like
        Image in which to find local maxima.
    particle_size : int, default 3
        Diameter of particles in units of pixels.
    thresh_abs : int or float
        Minimum intensity of peaks. Overrides thresh_perc. If both
        thresh_abs and thresh_perc are None, Otsu's method is used to
        determine threshold.
    thresh_perc : float in range of [0, 100], default None
        Only pixels with intensities above the thresh_perc
        percentile are considered.  Default = 70.  Ignored if
        thresh_abs is not None.
    border : int, default 0
        Peaks within distance border from the edge of the image are
        deleted.

    Returns
    -------
    output: ndarray of bools
        Boolean array shaped like image, with peaks represented by
        True values.
    """

    if thresh_abs is None:
        if thresh_perc is None:
            thresh_abs = skimage.filters.threshold_otsu(im)
        else:
            thresh_abs = np.percentile(im, thresh_perc)

    peak_indices = skimage.feature.peak_local_max(
        im,
        min_distance=particle_size,
        threshold_abs=thresh_abs,
        exclude_border=True,
    )

    # Peaks as a mask
    peaks = np.zeros(im.shape, dtype=bool)
    peaks[tuple(peak_indices.transpose())] = True

    return skimage.segmentation.clear_border(peaks, buffer_size=border)


def get_all_peaks(ic, particle_size=3, thresh_abs=None, thresh_perc=None, border=0):
    """
    Find local maxima in pixel intensity for each image in a list of
    images. Designed for use with images containing particles of a
    given size.

    Parameters
    ----------
    ic : list of images
        Images in which to find local maxima.
    particle_size : int, default 3
        Diameter of particles in units of pixels.
    thresh_abs : int or float
        Minimum intensity of peaks. Overrides thresh_perc. If both
        thresh_abs and thresh_perc are None, Otsu's method is used to
        determine threshold.
    thresh_perc : float in range of [0, 100], default None
        Only pixels with intensities above the thresh_perc
        percentile are considered.  Default = 70.  Ignored if
        thresh_abs is not None.
    border : int, default 0
        Peaks within distance border from the edge of the image are
        deleted.

    Returns
    -------
    output: list of ndarray of bools
        List of Boolean arrays shaped like image, with peaks
        represented by True values.
    """

    return [
        get_peaks(
            im,
            particle_size=3,
            thresh_abs=thresh_abs,
            thresh_perc=thresh_perc,
            border=border,
        )
        for im in ic
    ]


def peak_rois(peaks, r):
    """
    Draw square ROIs around peaks.

    Parameters
    ----------
    peaks : ndarray, type bool
        Boolean array shaped like image, with peaks represented by
        True values.
    r : int
        Radius of ROI.  The ROIs are squares centered at the
        respective peak with side length 2*r + 1.

    Returns
    -------
    output : list of slice objects
        A list of slice objects corresponding to ROIs.
    """

    # Get peaks as indices
    peaks_ind = np.transpose(peaks.nonzero())

    # Dimension of image
    im_shape = peaks.shape

    # Get ROIs around peaks
    rois = []
    for peak in peaks_ind:
        if (
            peak[0] >= r
            and peak[0] < im_shape[0] - r
            and peak[1] >= r
            and peak[1] < im_shape[1] - r
        ):
            rois.append(
                np.s_[peak[0] - r : peak[0] + r + 1, peak[1] - r : peak[1] + r + 1]
            )
    return rois


def filter_rois_intensity(im, rois, thresh_std=(1, 1)):
    """
    Determine which ROIs are worth keeping based on intensity.

    Parameters
    ----------
    ic : ndarray
        Image to use in filtering ROIS
    rois : list of slice objects
        List of ROIs to consider.
    thresh_std : 2-tuple
        If m is the mean intensity present in all ROIs in im
        and s is the standard deviation of intensities in the ROIs
        in im, them we only keep ROIs with total intensity between
        m - thresh_std[0] * s and m + thresh_std[1] * s.

    Returns
    -------
    filtered_rois : list of slice objects
        List of ROIs to consider in analysis
    """

    # Comute intensities in ROI
    roi_ints = np.array([im[roi].sum() for roi in rois])

    # Determine thresholds
    thresh_high = roi_ints.mean() + thresh_std[0] * roi_ints.std()
    thresh_low = roi_ints.mean() - thresh_std[1] * roi_ints.std()

    # Only keep ROIs with intensity within threshold
    return [
        roi
        for i, roi in enumerate(rois)
        if roi_ints[i] < thresh_high and roi_ints[i] > thresh_low
    ]


def filter_rois_peaks(peaks, rois):
    """
    Only keep ROIs with single beads.

    Parameters
    ----------
    peaks : ndarray
        A binary image, True if the pixel is at a peak, False otherwise
    rois : list of slice objects
        List of ROIs to consider.

    Returns
    -------
    filtered_rois : list of slice objects
        List of ROIs to consider in analysis
    """
    return [roi for roi in rois if peaks[roi].sum() == 1]


def _positional_variance_single_roi(peaks, roi):
    """Compute the positional variance of a bead within an ROI.

    Parameters
    ----------
    peaks : ndarray
        A binary image, True if the pixel is at a peak, False otherwise
    roi : Slice objects
        ROI to consider.

    Returns
    -------
    variance : float
        Variance of position of bead in units of square pixels.
    """
    r = []
    for i, peak_im in enumerate(peaks):
        inds = np.nonzero(peak_im[roi])
        x = inds[0]
        y = inds[1]
        if len(x) == 1:
            r.append(np.array([x[0], y[0]]))

    r = np.array(r)
    mean_r = np.mean(r, axis=0)
    r2 = np.sum(r * r, axis=1)

    return np.mean(r2) - np.dot(mean_r, mean_r)


def positional_variance(peaks, rois):
    """Compute the positional variances of a beads within ROIs.

    Parameters
    ----------
    peaks : ndarray
        A binary image, True if the pixel is at a peak, False otherwise
    rois : list of slice objects
        List of ROIs to consider.

    Returns
    -------
    variances : 1D Numpy array
        Variances of position of bead in units of square pixels. Entry `i` 
        corresponds to `rois[i]`.
    """
    return np.array([_positional_variance_single_roi(peaks, roi) for roi in rois])


def n_peaks_in_rois(peaks, rois):
    """
    Compute number of peaks in each ROI in each image.

    Parameters
    ----------
    peaks : list of ndarrays of type bool
        List of Boolean images that are True where a peak was detected
        and False elsewhere.
    rois : list of slice objects
        ROIs in which to check for peaks.

    Returns
    -------
    output : ndarray, shape (len(rois), len(peaks)), dtype int
        Entry i,j is the number of peaks in ROI i in frame j.
    """
    n_peaks = np.empty((len(rois), len(peaks)), dtype=int)

    for j, peak in enumerate(peaks):
        for i, roi in enumerate(rois):
            n_peaks[i, j] = peak[roi].sum()

    return n_peaks


def detect_bead_loss(t, n_peaks, n_frames=5, frac=0.75):
    """
    Detect when a bead is lost.  An ROI is said to lose a bead when
    frac of n_frames consecutive frames have zero beads.

    Parameters
    ----------
    t : ndarray
        Time points of frames
    n_peaks : ndarray, shape (len(t), )
        Entry i is the number of peaks in a given ROI.
    n_frames : int
        Number of consecutive frames to consider for bead loss.
    frac : float
        Fraction of frames within n_frames that must be beadless for
        the bead to be considered lost.

    Returns
    -------
    output : float
        The time when the bead was lost.  Returns -1 if the bead was
        not lost.
    """
    bead_intact = True
    i = 0
    while bead_intact and i < len(t) - n_frames:
        if (
            n_peaks[i] == 0
            and (n_peaks[i : i + n_frames] == 0).sum() / n_frames >= frac
        ):
            bead_intact = False
        i += 1

    if bead_intact:
        return -1
    else:
        return t[i]


def all_bead_loss(t, n_peaks_all, n_frames=5, frac=0.75):
    """
    Detect bead loss in all frames.

    Parameters
    ----------
    t : ndarray
        Time points of frames
    n_peaks_all : ndarray, shape (len(rois), len(peaks)), dtype int
        Entry i,j is the number of peaks in ROI i in frame j.
    n_frames : int
        Number of consecutive frames to consider for bead loss.
    frac : float
        Fraction of frames within n_frames that must be beadless for
        the bead to be considered lost.

    Returns
    -------
    beads_lost : ndarray, dtype int
        The indices of the beads that were lost.
    t_lost : ndarray, dtype float
        The times when the bead were lost.
    """
    loss_times = [
        detect_bead_loss(t, n_peaks, n_frames=n_frames, frac=frac)
        for n_peaks in n_peaks_all
    ]
    loss_times = np.array(loss_times)
    return loss_times[loss_times != -1], np.nonzero(loss_times != -1)[0]


def centroid_mag(im):
    """
    Return magnitude of the centroid of an image

    Parameters
    ----------
    im : ndarray
        Image for which to compute centroid

    Returns
    -------
    output : float
        Magnitude of the centroid.
    """
    m = skimage.measure.moments(im, order=1)
    return np.sqrt(m[0, 1] ** 2 + m[1, 0] ** 2) / m[0, 0]


def fiducial_beads(ic, rois, peaks, n_frames=5, n_fiducial=11):
    """
    Detect fiducial beads. This is used in drift correction based on fiducial
    beads as opposed to cross correlation of images.

    Parameters
    ----------
    ic : list of images
        Images to use in analysis.
    rois : list of slice objects
        List of ROIs to consider.
    peaks : ndarray, shape (n_peaks, 2)
        List of indicies of peaks in first frame of stack of images.
    n_frames : int, default 5
        Number of frames to use to determing fiducial ROIs
    n_fiducial : int, default 11 (must be odd)
        Number of fiducial ROIs to keep

    Returns
    -------
    output : ndarray, shape (n_fiducial, 2)
        Array of indices of fiducial beads
    """

    if n_fiducial % 2 == 0:
        raise RuntimeError("n_fiducial must be odd.")

    # Convert peaks to indices
    peaks_ind = np.transpose(peaks.nonzero())

    # Compute centroids of ROIS
    covs = np.empty(len(rois))
    for i, roi in enumerate(rois):
        centroids = np.array([centroid_mag(im[roi]) for im in ic[:n_frames]])
        covs[i] = centroids.std() / centroids.mean()

    # Sort coefficients of variation to get indicies of still ROIs
    roi_inds = np.argsort(covs)

    # Find positions of beads in fiducial ROIs
    i = 0
    j = 0
    fid_peaks = np.empty((n_fiducial, 2), dtype=np.int)
    while i < len(roi_inds) and j < n_fiducial:
        roi = rois[roi_inds[i]]

        # Find peaks in ROI (only use ROI with a single bead)
        ind = np.where(
            (roi[0].start <= peaks_ind[:, 0])
            & (peaks_ind[:, 0] < roi[0].stop)
            & (roi[1].start <= peaks_ind[:, 1])
            & (peaks_ind[:, 1] < roi[1].stop)
        )[0]
        if len(ind) == 1:
            fid_peaks[j, :] = peaks_ind[ind[0], :]
            j += 1
        i += 1

    if j < n_fiducial:
        raise RuntimeError("Failed to find %d fiducial peaks." % n_fiducial)

    return fid_peaks


def drift_correct_fiducial(ic, peaks, fid_peaks):
    """
    Perform drift correction using fiducial beads.
    """
    # Convert to indices
    peaks_ind = [np.transpose(peak.nonzero()) for peak in peaks]

    # Initialize shifts and peak positions
    fid_0 = fid_peaks.copy()
    shift = np.array([0, 0])

    ic_out = [ic[0]]
    for i, im in enumerate(ic[1:]):
        # Make KD tree for current peak locations
        kd = scipy.spatial.KDTree(peaks_ind[i])

        # Find the index closest to fiducial peaks
        fid = np.array([peaks_ind[i][kd.query(fp)[1]] for fp in fid_0])

        # Compute drift
        drift_i = int(np.median(fid[:, 0] - fid_0[:, 0]))
        drift_j = int(np.median(fid[:, 1] - fid_0[:, 1]))

        # Update shift
        shift += np.array([drift_i, drift_j])

        print(shift)

        # Make shifted output image
        pad = np.abs(shift).max()
        im_out = np.pad(im, np.abs(shift).max(), "constant")
        ic_out.append(
            im[
                pad + shift[0] : pad + shift[0] + im.shape[0],
                pad + shift[1] : pad + shift[1] + im.shape[1],
            ]
        )

        # Update fiducial points
        fid_0 = fid

    return ic_out


def bead_checker(ic, rois, r, peaks):
    """Visualization to allow checking for fidelity in lost bead image processing.

    Parameters
    ----------
    ic : list of ndarrays
        List of images. This is *not* a skimage.ImageCollection.
    rois : list of slice objects
        List of ROIs to consider.    
    r : int
        Radius of ROI.  The ROIs are squares centered at the
        respective peak with side length 2*r + 1.
    peaks : list of ndarrays of type bool
        List of Boolean images that are True where a peak was detected
        and False elsewhere.

    Returns
    -------
    app : Bokeh app
        To view the app, use `bokeh.io.show(app)`.
    """
    # Scale all the images for display
    im_max = 0
    for im in ic:
        if im.max() > im_max:
            im_max = im.max()
    ic_scaled = [((im / im_max) * 255).astype(np.uint8) for im in ic]

    # Instantiate plot
    dim = 2 * r + 1
    p = bokeh.plotting.figure(
        frame_height=256, frame_width=256, x_range=[0, dim], y_range=[0, dim]
    )

    # Populate glyphs
    im = p.image(image=[ic_scaled[0][rois[0]]], x=[0], y=[0], dw=[dim], dh=[dim])
    x, y = np.where(peaks[0][rois[0]])
    circles = p.circle(x + 0.5, y + 0.5, size=10, color="tomato")

    # Write update function for response to widgets
    def callback(attr, old, new):
        try:
            roi_ind = int(roi_input.value)
        except:
            roi_ind = 0
        if roi_ind > len(rois):
            roi_ind = -1
        frame = int(frame_slider.value)
        i, j = np.where(peaks[frame][rois[roi_ind]])
        circles.data_source.data = {"x": j + 0.5, "y": i + 0.5}
        im.data_source.data["image"] = [ic_scaled[frame][rois[roi_ind]]]


    # Sliders for frame number and ROI
    frame_slider = bokeh.models.Slider(
        start=0, end=len(ic) - 1, value=0, step=1, title="frame"
    )
    roi_input = bokeh.models.TextInput(value="0", title="ROI")

    # Connect callback
    frame_slider.on_change("value", callback)
    roi_input.on_change("value", callback)

    # Build layout
    layout = bokeh.layouts.column(p, frame_slider, roi_input)


    def app(doc):
        doc.add_root(layout)

    return app
