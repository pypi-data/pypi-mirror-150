#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of the CASCADe package which has been
# developed within the ExoplANETS-A H2020 program.
#
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2018, 2019, 2020, 2021  Jeroen Bouwman
"""Module defining the spectral extraction functionality used in cascade."""

import math
from functools import partial
import collections
import warnings
import copy
from itertools import zip_longest
import multiprocessing as mp
from asyncio import Event
from typing import Tuple
from psutil import virtual_memory, cpu_count
from tqdm import tqdm
import ray
from ray.actor import ActorHandle
import statsmodels.api as sm
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from scipy import ndimage
from astropy.convolution import convolve
from astropy.convolution import Gaussian2DKernel
from skimage.registration import phase_cross_correlation
from skimage.transform import warp
from skimage._shared.utils import safe_as_int
from skimage.transform import rotate
from skimage.transform import SimilarityTransform

from ..data_model import SpectralDataTimeSeries
from ..data_model import MeasurementDesc
from ..exoplanet_tools import SpectralModel
from ..utilities import _define_band_limits
from ..utilities import _define_rebin_weights
from ..utilities import _rebin_spectra

__all__ = [
           'determine_relative_source_position',
           'warp_polar', 'highpass', '_log_polar_mapping',
           '_determine_relative_source_shift', 'register_telescope_movement',
           '_determine_relative_rotation_and_scale', '_derotate_image',
           '_pad_to_size', '_pad_region_of_interest_to_square',
           'correct_wavelength_for_source_movent',
           'rebin_to_common_wavelength_grid',
           'determine_center_of_light_posision',
           'determine_absolute_cross_dispersion_position',
           'correct_initial_wavelength_shift',
           'renormalize_spatial_scans']


def chunks(lst, n):
    """
    Yield successive n-sized chunks from lst.

    Parameters
    ----------
    lst : 'list'
        Input list
    n : 'integer'
        Chunck size
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]




def determine_relative_source_position(spectralImageCube, ROICube,
                                       refIntegration,
                                       upsampleFactor=111,
                                       AngleOversampling=2):
    """
    Determine the shift of the spectra relative to the first integration.

    Parameters
    ----------
    spectralImageCube : 'ndarray'
        Input spectral image data cube. Fist dimintion is dispersion direction,
        second dimintion is cross dispersion direction and the last dimension
        is time.
    ROICube : 'ndarray' of 'bool'
        Cube containing the Region of interest for each integration.
        If not given, it is assumed that the mask of the spectralImageCube
        contains the region of interest.
    refIntegration : 'int'
        Index number of of integration to be taken as reference.
    upsampleFactor : 'int', optional
        integer factor by which to upsample image for FFT analysis to get
        sub-pixel accuracy. Default value is 111
    AngleOversampling : 'int', optional
        Oversampling factor for angle determination, Default value 2

    Returns
    -------
    relativeSourcePosition : 'collections.OrderedDict'
        relative rotation angle, scaling and x and y position as a
        function of time.

    Raises
    ------
    ValueError
        In case refIntegration exceeds number of integrations

    Notes
    -----
    Note that for sub-pixel registration to work correctly it should
    be performed on cleaned data i.e. bad pixels have been identified and
    corrected using the tools in this module.
    """
    nintegrations = spectralImageCube.shape[-1]
    refIntegration = int(refIntegration)
    if (refIntegration > nintegrations-1) | (refIntegration < 0):
        raise ValueError("Index number of reference integration exceeds \
                         limits. Aborting position determination")
    upsampleFactor = np.max([1, int(upsampleFactor)])
    AngleOversampling = np.max([1, int(AngleOversampling)])

    ImageCube = spectralImageCube.copy()
    refImage = ImageCube[..., refIntegration]

    if ROICube is None:
        ROICube = np.zeros((ImageCube.shape), dtype=bool)
    ROIref = ROICube[..., refIntegration]

    # First determine the rotation and scaling
    relativeAngle = np.zeros((nintegrations))
    relativeScale = np.ones((nintegrations))

    for it in range(1, nintegrations):
        relativeAngle[it], relativeScale[it] = \
         _determine_relative_rotation_and_scale(
             refImage, ROIref,
             ImageCube[..., it],
             ROICube[..., it],
             upsampleFactor=upsampleFactor,
             AngleOversampling=AngleOversampling)

    # Second, determine the shift
    yshift = np.zeros((nintegrations))
    xshift = np.zeros((nintegrations))

    for it, image in enumerate(ImageCube.T):
        if not np.allclose(relativeAngle[it], 0.0):
            derotateRefImage = _derotate_image(refImage, 0.0, ROI=ROIref,
                                               order=3)
            derotatedImage = _derotate_image(image.T, relativeAngle[it],
                                             ROI=ROICube[..., it], order=3)
            derotatedROIref = np.zeros_like(derotateRefImage).astype(bool)
            derotatedROI = np.zeros_like(derotatedImage).astype(bool)
        else:
            derotateRefImage = refImage
            derotatedImage = image.T
            derotatedROIref = ROIref
            derotatedROI = ROICube[..., it]

        shift = _determine_relative_source_shift(derotateRefImage,
                                                 derotatedImage,
                                                 referenceROI=derotatedROIref,
                                                 ROI=derotatedROI,
                                                 upsampleFactor=upsampleFactor)
        yshift[it] = shift[0]
        xshift[it] = shift[1]
    relativeSourcePosition = \
        collections.OrderedDict(relativeAngle=relativeAngle,
                                relativeScale=relativeScale,
                                cross_disp_shift=xshift,
                                disp_shift=yshift)
    return relativeSourcePosition


@ray.remote
def ray_determine_relative_source_position(spectralImageCube, ROICube,
                                           refIntegration, pba,
                                           upsampleFactor=111,
                                           AngleOversampling=2):
    """
    Ray wrapper for determine_relative_source_position.

    Parameters
    ----------
    spectralImageCube : 'ndarray'
        Input spectral image data cube. Fist dimintion is dispersion direction,
        second dimintion is cross dispersion direction and the last dimension
        is time.
    ROICube : 'ndarray' of 'bool'
        Cube containing the Region of interest for each integration.
        If not given, it is assumed that the mask of the spectralImageCube
        contains the region of interest.
    refIntegration : 'int'
        Index number of of integration to be taken as reference.
    upsampleFactor : 'int', optional
        integer factor by which to upsample image for FFT analysis to get
        sub-pixel accuracy. Default value is 111
    AngleOversampling : 'int', optional
        Oversampling factor for angle determination, Default value 2

    Returns
    -------
    movement : 'collections.OrderedDict'
        relative rotation angle, scaling and x and y position as a
        function of time.

    """
    movement = determine_relative_source_position(
        spectralImageCube, ROICube, refIntegration,
        upsampleFactor=upsampleFactor,
        AngleOversampling=AngleOversampling)
    pba.update.remote(1)
    return movement


def _determine_relative_source_shift(reference_image, image,
                                     referenceROI=None, ROI=None,
                                     upsampleFactor=111, space='real'):
    """
    Determine the relative shift of the spectral images.

    This routine determine the relative shift between a reference spectral
    image and another spectral image.

    Parameters
    ----------
    reference_image : 'ndarray or np.ma.MaskedArray' of 'float'
        Reference spectral image
    image : 'ndarray or np.ma.MaskedArray' of 'float'
        Spectral image
    referenceROI : ndarray' of 'bool', optional
    ROI : 'ndarray' of 'bool', optional
    upsampleFactor : 'int', optional
        Default value is 111
    space : 'str', optional
        Default value is 'real'
    Returns
    -------
    relativeImageShiftY
        relative shift compared to the reference image in the dispersion
        direction of the light (from top to bottom, shortest wavelength should
        be at row 0. Note that this shift is defined such that shifting a
        spectral image by this amound will place the trace at the exact same
        position as that of the reference image
    relativeImageShiftX
        relative shift compared to the reference image in the cross-dispersion
        direction of the light (from top to bottom, shortest wavelength should
        be at row 0. Note that this shift is defined such that shifting a
        spectral image by this amound will place the trace at the exact same
        position as that of the reference image.
    """
    ref_im = _pad_region_of_interest_to_square(reference_image, referenceROI)
    im = _pad_region_of_interest_to_square(image, ROI)

    # convolve with gaussian with sigma of 1 pixel to esnure that undersampled
    # spectra are properly registered.
    kernel = Gaussian2DKernel(1.0)
    ref_im = convolve(ref_im, kernel, boundary='extend')
    im = convolve(im, kernel, boundary='extend')

    # subpixel precision by oversampling image by upsampleFactor
    # returns shift, error and phase difference
    shift, _, _ = \
        phase_cross_correlation(ref_im, im, upsample_factor=upsampleFactor,
                                space=space)
    relativeImageShiftY = -shift[0]
    relativeImageShiftX = -shift[1]
    return relativeImageShiftY, relativeImageShiftX


def _determine_relative_rotation_and_scale(reference_image, referenceROI,
                                           image, ROI,
                                           upsampleFactor=111,
                                           AngleOversampling=2):
    """
    Determine rotation and scalng changes.

    This routine determines the relative rotation and scale change between
    an reference spectral image and another spectral image.

    Parameters
    ----------
    reference_image : 'ndarray or np.ma.MaskedArray' of 'float'
        Reference image
    referenceROI : 'ndarray' of 'float'
    image : 'ndarray or np.ma.MaskedArray' of 'float'
        Image for which the rotation and translation relative to the reference
        image will be determined
    ROI : 'ndarray' of 'float'
        Region of interest.
    upsampleFactor : 'int', optional
        Upsampling factor of FFT image used to determine sub-pixel shift.
        By default set to 111.
    AngleOversampling : 'int', optional
        Upsampling factor of the FFT image in polar coordinates for the
        determination of sub-degree rotation. Set by default to 2.

    Returns
    -------
    relative_rotation
        Relative rotation angle in degrees. The angle is defined such that the
        image needs to be rotated by this angle to have the same orientation
        as the reference spectral image
    relative_scaling
        Relative image scaling
    """
    AngleOversampling = int(AngleOversampling)
    nAngles = 360
    NeededImageSize = 2*AngleOversampling*nAngles
    ref_im = _pad_region_of_interest_to_square(reference_image, referenceROI)
    ref_im = _pad_to_size(ref_im, NeededImageSize, NeededImageSize)
    im = _pad_region_of_interest_to_square(image, ROI)
    im = _pad_to_size(im, NeededImageSize, NeededImageSize)

    # convolve with gaussian with sigma of 1 pixel to esnure that undersampled
    # spectra are properly registered.
    kernel = Gaussian2DKernel(1.0)
    ref_im = convolve(ref_im, kernel, boundary='extend')
    im = convolve(im, kernel, boundary='extend')

    h = np.hanning(im.shape[0])
    han2d = np.outer(h, h)  # 2D Hanning window

    fft_ref_im = np.abs(np.fft.fftshift(np.fft.fftn(ref_im*han2d)))**2
    fft_im = np.abs(np.fft.fftshift(np.fft.fftn(im*han2d)))**2

    h, w = fft_ref_im.shape
    radius = 0.8*np.min([w/2, h/2])

    hpf = highpass((h, w))

    fft_ref_im_filtered = fft_ref_im * hpf
    warped_fft_ref_im = warp_polar(fft_ref_im_filtered, scaling='log',
                                   radius=radius, output_shape=None,
                                   multichannel=None,
                                   AngleOversampling=AngleOversampling)
    fft_im_filtered = fft_im * hpf
    warped_fft_im = warp_polar(fft_im_filtered, scaling='log', radius=radius,
                               output_shape=None, multichannel=None,
                               AngleOversampling=AngleOversampling)

    tparams = phase_cross_correlation(warped_fft_ref_im, warped_fft_im,
                                      upsample_factor=upsampleFactor,
                                      space='real')

    shifts = tparams[0]
    # calculate rotation
    # note, only look for angles between +- 90 degrees,
    # remove any flip of 180 degrees due to search
    shiftr, shiftc = shifts[:2]
    shiftr = shiftr/AngleOversampling
    if shiftr > 90.0:
        shiftr = shiftr-180.0
    if shiftr < -90.0:
        shiftr = shiftr+180.0
    relative_rotation = -shiftr

    # Calculate scale factor from translation
    klog = radius / np.log(radius)
    relative_scaling = 1 / (np.exp(shiftc / klog))

    return relative_rotation, relative_scaling


def _derotate_image(image, angle, ROI=None, order=3):
    """
    Derotate image.

    Parameters
    ----------
    image : '2-D ndarray' of 'float'
        Input image to be de-rotated by 'angle' degrees.
    ROI : '2-D ndarray' of 'bool'
        Region of interest (default None)
    angle : 'float'
        Rotaton angle in degrees
    order : 'int'
        Order of the used interpolation in the rotation function of the
        skimage package.

    Returns
    -------
    derotatedImage : '2-D ndarray' of 'float'
        The zero padded and derotated image.
    """
    h, w = image.shape
    NeededImageSize = np.int(np.sqrt(h**2 + w**2))

    im = _pad_region_of_interest_to_square(image, ROI)
    im = _pad_to_size(im, NeededImageSize, NeededImageSize)
    derotatedImage = rotate(im, angle, order=order)

    return derotatedImage


def _pad_region_of_interest_to_square(image, ROI=None):
    """
    Pad ROI to square.

    Zero pad the extracted Region Of Interest of a larger image such that the
    resulting image is squared.

    Parameters
    ----------
    image : '2-D ndarray' of 'float'
        Input image to be de-rotated by 'angle' degrees.
    ROI : '2-D ndarray' of 'bool'
        Region of interest (default None)

    Returns
    -------
    padded_image : '2-D ndarray' of 'float'
    """
    if ROI is not None:
        label_im, _ = ndimage.label(ROI)
    elif isinstance(image, np.ma.core.MaskedArray):
        label_im, _ = ndimage.label(image.mask)
    else:
        raise AttributeError("For image 0 padding either use MaskedArray as \
                              input or provide ROI. Aborting 0 padding")
    slice_y, slice_x = ndimage.find_objects(label_im != 1)[0]
    padded_image = image[slice_y, slice_x]

    if isinstance(image, np.ma.core.MaskedArray):
        padded_image.set_fill_value(0.0)
        padded_image = padded_image.filled()

    h, w = padded_image.shape
    if h == w:
        return padded_image

    im_size = np.max([h, w])
    delta_h = im_size - h
    delta_w = im_size - w
    padding = ((delta_h//2, delta_h-(delta_h//2)),
               (delta_w//2, delta_w-(delta_w//2)))
    padded_image = np.pad(padded_image,
                          padding, 'constant', constant_values=(0))

    return padded_image


def _pad_to_size(image, h, w):
    """
    Zero pad the input image to an image of hight h and width w.

    Parameters
    ----------
    image : '2-D ndarray' of 'float'
        Input image to be zero-padded to size (h, w).
    h : 'int'
        Hight (number of rows) of output image.
    w : 'int'
        Width (number of columns) of output image.

    Returns
    -------
    padded_image : '2-D ndarray' of 'float'
    """
    padded_image = image.copy()
    if isinstance(padded_image, np.ma.core.MaskedArray):
        padded_image.set_fill_value(0.0)
        padded_image = padded_image.filled()
    h_image, w_image = padded_image.shape
    npad_h = np.max([1, (h-h_image)//2])
    npad_w = np.max([1, (w-w_image)//2])
    padding = ((npad_h, npad_h), (npad_w, npad_w))
    padded_image = np.pad(padded_image,
                          padding, 'constant', constant_values=(0))
    return padded_image


def _log_polar_mapping(output_coords, k_angle, k_radius, center):
    """
    Inverse mapping function to convert from cartesion to polar coordinates.

    Parameters
    ----------
    output_coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the output image
    k_angle : float
        Scaling factor that relates the intended number of rows in the output
        image to angle: ``k_angle = nrows / (2 * np.pi)``
    k_radius : float
        Scaling factor that relates the radius of the circle bounding the
        area to be transformed to the intended number of columns in the output
        image: ``k_radius = width / np.log(radius)``
    center : tuple (row, col)
        Coordinates that represent the center of the circle that bounds the
        area to be transformed in an input image.

    Returns
    -------
    coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the input image that
        correspond to the `output_coords` given as input.
    """
    angle = output_coords[:, 1] / k_angle
    rr = ((np.exp(output_coords[:, 0] / k_radius)) * np.sin(angle)) + center[0]
    cc = ((np.exp(output_coords[:, 0] / k_radius)) * np.cos(angle)) + center[1]
    coords = np.column_stack((cc, rr))
    return coords


def _linear_polar_mapping(output_coords, k_angle, k_radius, center):
    """
    Inverse mapping function to convert from cartesion to polar coordinates.

    Parameters
    ----------
    output_coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the output image
    k_angle : float
        Scaling factor that relates the intended number of rows in the output
        image to angle: ``k_angle = nrows / (2 * np.pi)``
    k_radius : float
        Scaling factor that relates the radius of the circle bounding the
        area to be transformed to the intended number of columns in the output
        image: ``k_radius = ncols / radius``
    center : tuple (row, col)
        Coordinates that represent the center of the circle that bounds the
        area to be transformed in an input image.

    Returns
    -------
    coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the input image that
        correspond to the `output_coords` given as input.
    """
    angle = output_coords[:, 1] / k_angle
    rr = ((output_coords[:, 0] / k_radius) * np.sin(angle)) + center[0]
    cc = ((output_coords[:, 0] / k_radius) * np.cos(angle)) + center[1]
    coords = np.column_stack((cc, rr))
    return coords


def warp_polar(image, center=None, *, radius=None, AngleOversampling=1,
               output_shape=None, scaling='linear', multichannel=False,
               **kwargs):
    """
    Remap image to polor or log-polar coordinates space.

    Parameters
    ----------
    image : ndarray
        Input image. Only 2-D arrays are accepted by default. If
        `multichannel=True`, 3-D arrays are accepted and the last axis is
        interpreted as multiple channels.
    center : tuple (row, col), optional
        Point in image that represents the center of the transformation (i.e.,
        the origin in cartesian space). Values can be of type `float`.
        If no value is given, the center is assumed to be the center point
        of the image.
    radius : float, optional
        Radius of the circle that bounds the area to be transformed.
    AngleOversampling : int
        Oversample factor for number of angles
    output_shape : tuple (row, col), optional
    scaling : {'linear', 'log'}, optional
        Specify whether the image warp is polar or log-polar. Defaults to
        'linear'.
    multichannel : bool, optional
        Whether the image is a 3-D array in which the third axis is to be
        interpreted as multiple channels. If set to `False` (default), only 2-D
        arrays are accepted.
    **kwargs : keyword arguments
        Passed to `transform.warp`.

    Returns
    -------
    warped : ndarray
        The polar or log-polar warped image.

    Examples
    --------
    Perform a basic polar warp on a grayscale image:
    >>> from skimage import data
    >>> from skimage.transform import warp_polar
    >>> image = data.checkerboard()
    >>> warped = warp_polar(image)
    Perform a log-polar warp on a grayscale image:
    >>> warped = warp_polar(image, scaling='log')
    Perform a log-polar warp on a grayscale image while specifying center,
    radius, and output shape:
    >>> warped = warp_polar(image, (100,100), radius=100,
    ...                     output_shape=image.shape, scaling='log')
    Perform a log-polar warp on a color image:
    >>> image = data.astronaut()
    >>> warped = warp_polar(image, scaling='log', multichannel=True)
    """
    if image.ndim != 2 and not multichannel:
        raise ValueError("Input array must be 2 dimensions "
                         "when `multichannel=False`,"
                         " got {}".format(image.ndim))

    if image.ndim != 3 and multichannel:
        raise ValueError("Input array must be 3 dimensions "
                         "when `multichannel=True`,"
                         " got {}".format(image.ndim))

    if center is None:
        center = (np.array(image.shape)[:2] / 2) - 0.5

    if radius is None:
        w, h = np.array(image.shape)[:2] / 2
        radius = np.sqrt(w ** 2 + h ** 2)

    if output_shape is None:
        height = 360*AngleOversampling
        width = int(np.ceil(radius))
        output_shape = (height, width)
    else:
        output_shape = safe_as_int(output_shape)
        height = output_shape[0]
        width = output_shape[1]

    if scaling == 'linear':
        k_radius = width / radius
        map_func = _linear_polar_mapping
    elif scaling == 'log':
        k_radius = width / np.log(radius)
        map_func = _log_polar_mapping
    else:
        raise ValueError("Scaling value must be in {'linear', 'log'}")

    k_angle = height / (2 * np.pi)
    warp_args = {'k_angle': k_angle, 'k_radius': k_radius, 'center': center}

    warped = warp(image, map_func, map_args=warp_args,
                  output_shape=output_shape, **kwargs)

    return warped


def highpass(shape):
    """
    Return highpass filter to be multiplied with fourier transform.

    Parameters
    ----------
    shape : 'ndarray' of 'int'
        Input shape of 2d filter

    Returns
    -------
    filter
        high pass filter
    """
    x = np.outer(
        np.cos(np.linspace(-math.pi/2., math.pi/2., shape[0])),
        np.cos(np.linspace(-math.pi/2., math.pi/2., shape[1])))
    return (1.0 - x) * (2.0 - x)


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks.

    Parameters
    ----------
    iterable : TYPE
        DESCRIPTION.
    n : TYPE
        DESCRIPTION.
    fillvalue : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


@ray.remote
class ProgressBarActor:
    counter: int
    delta: int
    event: Event

    def __init__(self) -> None:
        self.counter = 0
        self.delta = 0
        self.event = Event()

    def update(self, num_items_completed: int) -> None:
        """
        Updates the ProgressBar with the incremental
        number of items that were just completed.
        """
        self.counter += num_items_completed
        self.delta += num_items_completed
        self.event.set()

    async def wait_for_update(self) -> Tuple[int, int]:
        """
        Blocking call.

        Waits until somebody calls `update`, then returns a tuple of
        the number of updates since the last call to
        `wait_for_update`, and the total number of completed items.
        """
        await self.event.wait()
        self.event.clear()
        saved_delta = self.delta
        self.delta = 0
        return saved_delta, self.counter

    def get_counter(self) -> int:
        """
        Returns the total number of complete items.
        """
        return self.counter


class ProgressBar:
    progress_actor: ActorHandle
    total: int
    description: str
    pbar: tqdm

    def __init__(self, total: int, description: str = ""):
        # Ray actors don't seem to play nice with mypy, generating
        # a spurious warning for the following line,
        # which we need to suppress. The code is fine.
        self.progress_actor = ProgressBarActor.remote()  # type: ignore
        self.total = total
        self.description = description

    @property
    def actor(self) -> ActorHandle:
        """
        Returns a reference to the remote `ProgressBarActor`.

        When you complete tasks, call `update` on the actor.
        """
        return self.progress_actor

    def print_until_done(self) -> None:
        """Blocking call.

        Do this after starting a series of remote Ray tasks, to which you've
        passed the actor handle. Each of them calls `update` on the actor.
        When the progress meter reaches 100%, this method returns.
        """
        pbar = tqdm(desc=self.description, total=self.total)
        while True:
            delta, counter = ray.get(self.actor.wait_for_update.remote())
            pbar.update(delta)
            if counter >= self.total:
                pbar.close()
                return


def ray_loop(dataCube, ROICube=None, upsampleFactor=111,
             AngleOversampling=2, nreference=6, maxNumberOfCPUs=2,
             useMultiProcesses=True):
    """
    Ray wrapper around determine_relative_source_position function.

    Performs parallel loop for different reference integrations to determine
    the relative source movement on the detector.

    Parameters
    ----------
    dataCube : 'ndarray'
        Input spectral image data cube. Fist dimention is dispersion direction,
        second dimintion is cross dispersion direction and the last dimension
        is time. The shortest wavelengths are at the first row
    ROICube : 'ndarray' of 'bool', optional
        Region of Interest
    nreferences : 'int', optional
        Number of reference times used to determine the relative movement
    upsampleFactor : 'int, optional
        Upsample factor for translational movement
    AngleOversampling : 'int, optional
        Upsample factor for determination of rotational movement.
    max_number_of_cpus : 'int', optional
        Maximum number of CPU used when using parallel calculations.
    useMultiProcesses : 'bool', optional
        If True, calculations will be done in parallel.

    Returns
    -------
    relativeSourcePosition : 'collections.OrderedDict'
        Ordered dict containing the relative rotation angle,
        scaling and x and y position as a function of time.
    """
    ntime = dataCube.shape[-1]
    if not useMultiProcesses:
        # create new function with all fixed inout variables fixed.
        func = partial(determine_relative_source_position, dataCube,
                       ROICube, upsampleFactor=upsampleFactor,
                       AngleOversampling=AngleOversampling)
        ITR = list(np.linspace(0, ntime-1, nreference, dtype=int))
        movement_iterator = map(func, ITR)

        for j in tqdm(movement_iterator, total=len(ITR),
                      dynamic_ncols=True):
            yield j
    else:
        ncpu = int(np.min([maxNumberOfCPUs, np.max([1, mp.cpu_count()-3])]))
        ray.init(num_cpus=ncpu)

        dataCube_id = ray.put(dataCube)
        ROICube_id = ray.put(ROICube)
        upsampleFactor_id = ray.put(upsampleFactor)
        AngleOversampling_id = ray.put(AngleOversampling)
        ITR = iter(np.linspace(0, ntime-1, nreference, dtype=int))

        pb = ProgressBar(nreference,
                         'Determine Telescope movement for '
                         '{} reference times'.format(nreference))
        actor = pb.actor
        result_ids = \
            [ray_determine_relative_source_position.remote(
                dataCube_id,
                ROICube_id,
                x,
                actor,
                upsampleFactor=upsampleFactor_id,
                AngleOversampling=AngleOversampling_id) for x in ITR]
        pb.print_until_done()
        MPITR = ray.get(result_ids)
        for relativeSourcePosition in MPITR:
            yield relativeSourcePosition

        ray.shutdown()


def register_telescope_movement(cleanedDataset, ROICube=None,  nreferences=6,
                                mainReference=4, upsampleFactor=111,
                                AngleOversampling=2, verbose=False,
                                verboseSaveFile=None, maxNumberOfCPUs=2,
                                useMultiProcesses=True):
    """
    Register the telescope movement.

    Parameters
    ----------
    cleanedDataset : 'SpectralDataTimeSeries'
        Input dataset. Note that for image registration to work properly,
        bad pixels need ti be removed (cleaned) first. This routine checks if
        a cleaned dataset is used by checking for the isCleanedData flag.
    ROICube : 'ndarray' of 'bool', optional
        Cube containing the Region of interest for each integration.
        If not given, it is assumed that the mask of the cleanedDataset
        contains the region of interest.
    nreferences : 'int', optional
        Default is 6.
    mainReference : 'int', optional
        Default is 4.
    upsampleFactor : 'int, optional
        Upsample factor of FFT images to determine relative movement at
        sub-pixel level. Default is 111
    AngleOversampling : 'int, optional
        Upsampling factor of the angle in the to polar coordinates transformed
        FFT images to determine the relative rotation adn scale change.
        Default is 2.
    verbose : 'bool', optional
        If true diagnostic plots will be generated. Default is False
    verboseSaveFile : 'str', optional
        If not None, verbose output will be saved to the specified file.
    max_number_of_cpus : 'int', optional
        Maxiumum bumber of cpu's to be used.

    Returns
    -------
    spectralMovement : 'OrderedDict'
        Ordered dict containing the relative rotation, scaling,
        and movement in the dispersion and cross dispersion direction.

    Raises
    ------
    ValueError, TypeError
        Errors are raised if certain data is not present of from the wrong
        type.
    """
    try:
        if cleanedDataset.isCleanedData is False:
            raise ValueError
    except (ValueError, AttributeError):
        raise TypeError("Input dataset is not recognized as cleaned dataset")

    maskeddata = cleanedDataset.return_masked_array('data').copy()
    dataUse = maskeddata.data
    if ROICube is None:
        ROICube = maskeddata.mask
    else:
        ROICube = np.logical_or(maskeddata.mask, ROICube)

    ntime = dataUse.shape[-1]
    if (nreferences < 1) | (nreferences > ntime):
        raise ValueError("Wrong nreferences value")
    if (mainReference < 0) | (mainReference > nreferences):
        raise ValueError("Wrong mainReference value")

    determinePositionIterator = \
        ray_loop(dataUse, ROICube=ROICube,
                 upsampleFactor=upsampleFactor,
                 AngleOversampling=AngleOversampling,
                 nreference=nreferences,
                 maxNumberOfCPUs=maxNumberOfCPUs,
                 useMultiProcesses=useMultiProcesses)
    iteratorResults = list(determinePositionIterator)

    referenceIndex = np.linspace(0, ntime-1, nreferences, dtype=int)
    testAngle = np.zeros((nreferences, ntime))
    testScale = np.zeros((nreferences, ntime))
    testCrossDispShift = np.zeros((nreferences, ntime))
    testDispShift = np.zeros((nreferences, ntime))
    for i in range(nreferences):
        testAngle[i, :] = iteratorResults[i]['relativeAngle'] - \
            iteratorResults[i]['relativeAngle'][referenceIndex[mainReference]]
        testScale[i, :] = iteratorResults[i]['relativeScale'] / \
            iteratorResults[i]['relativeScale'][referenceIndex[mainReference]]
        testCrossDispShift[i, :] = iteratorResults[i]['cross_disp_shift'] - \
            iteratorResults[i]['cross_disp_shift'][referenceIndex[
                mainReference]]
        testDispShift[i, :] = iteratorResults[i]['disp_shift'] - \
            iteratorResults[i]['disp_shift'][referenceIndex[mainReference]]

    relativeAngle = np.median(testAngle, axis=0)
    relativeScale = np.median(testScale, axis=0)
    crossDispersionShift = np.median(testCrossDispShift, axis=0)
    dispersionShift = np.median(testDispShift, axis=0)
    # shift to first time index
    testAngle = testAngle - relativeAngle[0]
    testScale = testScale / relativeScale[0]
    testCrossDispShift = testCrossDispShift - crossDispersionShift[0]
    testDispShift = testDispShift - dispersionShift[0]
    relativeAngle = relativeAngle - relativeAngle[0]
    relativeScale = relativeScale / relativeScale[0]
    crossDispersionShift = crossDispersionShift - crossDispersionShift[0]
    dispersionShift = dispersionShift - dispersionShift[0]

    if verbose:
        sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2.5})
        sns.set_style("white", {"xtick.bottom": True, "ytick.left": True})
        fig, axes = plt.subplots(figsize=(14, 12), nrows=2, ncols=2)
        ax0, ax1, ax2, ax3 = axes.flatten()
        ax0.plot(testAngle.T)
        ax0.plot(relativeAngle, lw=5)
        ax0.set_title('Relative Angle')
        ax0.set_xlabel('Integration #')
        ax0.set_ylabel('Angle [degrees]')
        ax1.plot(testScale.T)
        ax1.plot(relativeScale, lw=5)
        ax1.set_title('Relative Scale')
        ax1.set_xlabel('Integration #')
        ax1.set_ylabel('Scaling Factor')
        ax2.plot(testCrossDispShift.T)
        ax2.plot(crossDispersionShift, lw=5)
        ax2.set_title('Relative Cross-dispersion shift')
        ax2.set_ylabel('Shift [pixles]')
        ax2.set_xlabel('Integration #')
        ax3.plot(testDispShift.T)
        ax3.plot(dispersionShift, lw=5)
        ax3.set_title('Relative Dispersion shift')
        ax3.set_xlabel('Integration #')
        ax3.set_ylabel('Shift [pixles]')
        fig.subplots_adjust(hspace=0.3)
        fig.subplots_adjust(wspace=0.45)
        plt.show()
        if verboseSaveFile is not None:
            fig.savefig(verboseSaveFile, bbox_inches='tight')

    spectralMovement = \
        collections.OrderedDict(relativeAngle=relativeAngle,
                                relativeScale=relativeScale,
                                crossDispersionShift=crossDispersionShift,
                                dispersionShift=dispersionShift,
                                referenceIndex=referenceIndex[mainReference])
    return spectralMovement


def determine_center_of_light_posision(cleanData, ROI=None, verbose=False,
                                       quantileCut=0.5, orderTrace=2):
    """
    Determine the center of light position.

    This routine determines the center of light position (cross-dispersion)
    of the dispersed light. The center of light  is defined in a similar
    way as the center of mass.  This routine also fits a polynomial to the
    spectral trace.

    Parameters
    ----------
    cleanData : 'maskedArray' or 'ndarray'
        Input data
    ROI : 'ndarray' of 'bool', optional
        Region of interest
    verbose : 'bool'
        Default is False
    quantileCut : 'float', optional
        Default is 0.5
    orderTrace : 'int'
        Default is 2

    Returns
    -------
    total_light : 'ndarray'
        Total summed signal on the detector as function of wavelength.
    idx : 'int'
    COL_pos : 'ndarray'
        Center of light position of the dispersed light.
    ytrace : 'ndarray'
        Spectral trace position in fraction of pixels in the dispersion
        direction
    xtrace : 'ndarray'
        Spectral trace position in fraction of pixels in the cross dispersion
        direction
    """
    if isinstance(cleanData, np.ma.core.MaskedArray):
        data_use = cleanData.data
        if ROI is not None:
            mask_use = cleanData.mask | ROI
        else:
            mask_use = cleanData.mask
    else:
        data_use = cleanData
        if ROI is not None:
            mask_use = ROI
        else:
            mask_use = np.zeros_like(cleanData, dtype='bool')

    data = np.ma.array(data_use, mask=mask_use)
    npix, mpix = data.shape

    position_grid = np.mgrid[0:npix, 0:mpix]
    total_light = np.ma.sum(data, axis=1)

    COL = np.ma.sum(data*position_grid[1, ...], axis=1) / \
        total_light

    treshhold = np.quantile(total_light[~total_light.mask], quantileCut)
    idx_use = np.ma.where(total_light > treshhold)[0]
    ytrace = np.arange(npix)
    idx = ytrace[idx_use]
    X = []
    for i in range(orderTrace+1):
        X.append(idx**i)
    X = np.array(X).T
    robust_fit = sm.RLM(COL[idx_use], X).fit()
    z = robust_fit.params[::-1]
    f = np.poly1d(z)
    xtrace = f(ytrace)

    if verbose:
        sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2.5})
        sns.set_style("white", {"xtick.bottom": True, "ytick.left": True})
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(idx_use, total_light[idx_use])
        ax.set_title('Integrated Signal')
        ax.set_xlabel('Pixel Position Dispersion Direction')
        ax.set_ylabel('Integrated Signal')
        plt.show()

    return total_light[idx_use], idx, COL[idx_use], ytrace, xtrace


def correct_initial_wavelength_shift(referenceDataset, cascade_configuration,
                                     *otherDatasets):
    """
    Determine if there is an initial wavelength shift and correct.

    Parameters
    ----------
    referenceDataset : 'cascade.data_model.SpectralDataTimeSeries'
        Dataset who's wavelength is used as refernce of the wavelength
        correction.
    cascade_configuration : 'cascade.initialize.initialize.configurator'
        Singleton containing the confifuration parameters of cascade.
    **otherDatasets : 'cascade.data_model.SpectralDataTimeSeries'
        Optional.
        Other datasets assumed to have the same walengths as the reference
        dataset and which will be corrected simultaneously with the reference.

    Returns
    -------
    referenceDataset : 'list' of 'cascade.data_model.SpectralDataTimeSeries'
        Dataset with corrected wavelengths.
    otherDatasets_list : 'list' of 'cascade.data_model.SpectralDataTimeSeries'
        Optinal output.
    modeled_observations : 'list' of 'ndarray'
    stellar_model : 'list' of 'ndarray'
    corrected_observations : 'list' of 'ndarray'
    """
    model_spectra = SpectralModel(cascade_configuration)
    wave_shift, error_wave_shift = \
        model_spectra.determine_wavelength_shift(referenceDataset)
    referenceDataset.wavelength = referenceDataset.wavelength+wave_shift
    referenceDataset.add_auxilary(wave_shift=wave_shift.to_string())
    referenceDataset.add_auxilary(error_wave_shift=error_wave_shift.to_string())
    otherDatasets_list = list(otherDatasets)
    for i, dataset in enumerate(otherDatasets_list):
        dataset.wavelength = dataset.wavelength+wave_shift
        dataset.add_auxilary(wave_shift=wave_shift.to_string())
        dataset.add_auxilary(error_wave_shift=error_wave_shift.to_string())
        otherDatasets_list[i] = dataset
    modeled_observations = \
        [model_spectra.model_wavelength, model_spectra.model_observation,
         model_spectra.scaling, model_spectra.relative_distanc_sqr,
         model_spectra.sensitivity]
    stellar_model = \
        [model_spectra.model_wavelength, model_spectra.rebinned_stellar_model]
    input_stellar_model = [model_spectra.sm[2], model_spectra.sm[3]]
    corrected_observations = \
        [model_spectra.corrected_wavelength, model_spectra.observation,
         wave_shift, error_wave_shift]
    stellar_model_parameters = model_spectra.par
    if len(otherDatasets_list) > 0:
        return [referenceDataset] + otherDatasets_list, modeled_observations,\
            stellar_model, corrected_observations, input_stellar_model, \
            stellar_model_parameters
    return referenceDataset,  modeled_observations, stellar_model, \
        corrected_observations, input_stellar_model, \
        stellar_model_parameters


def renormalize_spatial_scans(referenceDataset, *otherDatasets):
    """
    bla.

    Parameters
    ----------
    referenceDataset : TYPE
        DESCRIPTION.
    *otherDatasets : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    otherDatasets_list = list(otherDatasets)

    try:
        scan_direction = np.array(referenceDataset.scan_direction)
    except AttributeError:
        if len(otherDatasets_list) > 0:
            return [referenceDataset] + otherDatasets_list
        return referenceDataset

    unique_scan_directions = np.unique(scan_direction)
    if len(unique_scan_directions) != 2:
        if len(otherDatasets_list) > 0:
            return [referenceDataset] + otherDatasets_list
        return referenceDataset

    idx = scan_direction == 0.0
    med0 = np.median(referenceDataset.data[...,idx]).value
    med1 = np.median(referenceDataset.data[...,~idx]).value
    med = np.median(referenceDataset.data).value
    scaling0 = med / med0
    scaling1 = med / med1

    reference_data = copy.deepcopy(referenceDataset.data)
    reference_data[..., idx] = reference_data[..., idx]*scaling0
    reference_data[..., ~idx] = reference_data[..., ~idx]*scaling1
    referenceDataset.data = reference_data
    reference_uncertainty = copy.deepcopy(referenceDataset.uncertainty)
    reference_uncertainty[..., idx] = reference_uncertainty[..., idx]*scaling0
    reference_uncertainty[...,~idx] = reference_uncertainty[...,~idx]*scaling1
    referenceDataset.uncertainty = reference_uncertainty

    for i, dataset in enumerate(otherDatasets_list):
        reference_data = copy.deepcopy(dataset.data)
        reference_data[..., idx] = reference_data[..., idx]*scaling0
        reference_data[..., ~idx] = reference_data[..., ~idx]*scaling1
        dataset.data = reference_data
        reference_uncertainty = copy.deepcopy(dataset.uncertainty)
        reference_uncertainty[..., idx] = reference_uncertainty[..., idx]*scaling0
        reference_uncertainty[...,~idx] = reference_uncertainty[...,~idx]*scaling1
        dataset.uncertainty = reference_uncertainty
        otherDatasets_list[i] = dataset
    if len(otherDatasets_list) > 0:
        return [referenceDataset] + otherDatasets_list
    return referenceDataset


def determine_absolute_cross_dispersion_position(cleanedDataset, initialTrace,
                                                 ROI=None,
                                                 verbose=False,
                                                 verboseSaveFile=None,
                                                 quantileCut=0.5,
                                                 orderTrace=2):
    """
    Determine the initial cross dispersion position.

    This routine updates the initial spectral trace for positional shifts in
    the cross dispersion direction for the first exposure of the the time
    series observation.

    Parameters
    ----------
    cleanedDataset : 'SpectralDataTimeSeries'
    initialTrace : 'OrderedDict'
        input spectral trace.
    ROI : 'ndarray' of 'bool'
        Region of interest.
    verbose : 'bool', optional
        If true diagnostic plots will be generated. Default is False
    verboseSaveFile : 'str', optional
        If not None, verbose output will be saved to the specified file.
    quantileCut : 'float', optional
        Default is 0.5
    orderTrace : 'int', optional
        Default is 2

    Returns
    -------
    newShiftedTrace : 'OrderedDict'
        To the observed source poisiton shifted spectral trace
    newFittedTrace : 'OrderedDict'
        Trace determined by fit to the center of light position.
    initialCrossDispersionShift : 'float'
        Shift between initial guess for spectral trace position and
        fitted trace position of the first spectral image.
    """
    cleanedData = cleanedDataset.return_masked_array('data')

    newShiftedTrace = copy.copy(initialTrace)
    newFittedTrace = copy.copy(initialTrace)

    if ROI is not None:
        roiUse = cleanedData[..., 0].mask | ROI
    else:
        roiUse = cleanedData[..., 0].mask

    kernel = Gaussian2DKernel(1.0)
    convolvedFirstImage = convolve(cleanedData[..., 0], kernel,
                                   boundary='extend')

    _, idx, col, yTrace, xTrace = \
        determine_center_of_light_posision(convolvedFirstImage, ROI=roiUse,
                                           quantileCut=quantileCut,
                                           orderTrace=orderTrace)

    medianCrossDispersionPosition = np.ma.median(xTrace[idx])
    medianCrossDispersionPositionInitialTrace = \
        np.ma.median(initialTrace['positional_pixel'].value[idx])

    initialCrossDispersionShift = \
        medianCrossDispersionPosition-medianCrossDispersionPositionInitialTrace

    newShiftedTrace['positional_pixel'] = \
        newShiftedTrace['positional_pixel'] + \
        initialCrossDispersionShift*newShiftedTrace['positional_pixel'].unit
    newFittedTrace['positional_pixel'] = \
        xTrace*newFittedTrace['positional_pixel'].unit

    if verbose:
        sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2.5})
        sns.set_style("white", {"xtick.bottom": True, "ytick.left": True})
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(idx, col, label='COL')
        ax.plot(yTrace, xTrace, label='Fitted Trace')
        ax.plot(newShiftedTrace['positional_pixel'].value,
                label='Shifted Instrument Trace')
        ax.plot(initialTrace['positional_pixel'].value,
                label='Initial Instrument Trace')
        ax.legend(loc='best')
        ax.set_title('Initial Trace Position')
        ax.set_xlabel('Pixel Position Dispersion Direction')
        ax.set_ylabel('Pixel Position Cross-Dispersion Direction')
        plt.show()
        if verboseSaveFile is not None:
            fig.savefig(verboseSaveFile, bbox_inches='tight')

    return newShiftedTrace, newFittedTrace, medianCrossDispersionPosition, \
        initialCrossDispersionShift


def correct_wavelength_for_source_movent(datasetIn, spectral_movement,
                                         useScale=False,
                                         useCrossDispersion=False,
                                         verbose=False, verboseSaveFile=None):
    """
    Correct wavelengths for source movement.

    This routine corrects the wavelength cube attached to the spectral
    image data cube for source (telescope) movements

    Parameters
    ----------
    datasetIn : 'SpectralDataTimeSeries'
        Input dataset for which the waveength will be corrected for telescope
        movement
    spectral_movement : 'OrderedDict'
        Ordered dict containing the relative rotation, scaling,
        and movement in the dispersion and cross dispersion direction.
     useScale : 'bool', optional
         If set the scale parameter is used to correct the wavelength.
         Default is False.
    useCrossDispersion : 'bool', optional
        If set the coress dispersion movement is used to correct the
        wavelength. Default is False.
    verbose : 'bool', optional
        If true diagnostic plots will be generated. Default is False
    verboseSaveFile : 'str', optional
        If not None, verbose output will be saved to the specified file.

    Returns
    -------
    dataset_out : 'SpectralDataTimeSeries'
        The flag isMovementCorrected=True is set to indicate that this dataset
        is corrected

    Notes
    -----
    Scaling changes are not corrected at the moment. Note that the used
    rotation and translation to correct the wavelengths is the relative
    source movement defined such that shifting the observed spectral image by
    these angles and shifts the position would be identical to the reference
    image. The correction of the wavelength using the reference spectral image
    is hence in the oposite direction.
    """
    dataset_out = copy.deepcopy(datasetIn)

    correctedWavelength = dataset_out.return_masked_array('wavelength').copy()
    # no need for mask here as wavekength should be difined for all pixels
    correctedWavelength = correctedWavelength.data

    ntime = correctedWavelength.shape[-1]
    for it in range(ntime):
        rows, cols = (np.array(correctedWavelength.shape)[:2] / 2) - 0.5
        center = np.array((cols, rows)) / 2. - 0.5
        tform1 = SimilarityTransform(translation=center)
        angle_rad = np.deg2rad(-spectral_movement['relativeAngle'][it])
        scale = spectral_movement['relativeScale'][it]
        tform2 = SimilarityTransform(rotation=angle_rad,
                                     scale=(1.0/scale-1.0)*int(useScale)+1.0)
        tform3 = SimilarityTransform(translation=-center)
        tform_rotate = tform3 + tform2 + tform1
        translation = (-spectral_movement['crossDispersionShift'][it] *
                       int(useCrossDispersion),
                       -spectral_movement['dispersionShift'][it])
        tform_translate = SimilarityTransform(translation=translation)
        tform_combined = tform_translate + tform_rotate
        correctedWavelength[..., it] = warp(correctedWavelength[..., it],
                                            tform_combined, order=3,
                                            cval=np.nan)

    # mask those regions of the images which are on the edge and migth
    # not be present at all times.
    correctedWavelength = np.ma.masked_invalid(correctedWavelength)
    ncols = correctedWavelength.shape[1]
    for ic in range(ncols):
        correctedWavelength[:, ic, :] = \
            np.ma.mask_rows(correctedWavelength[:, ic, :])
    # replace old wavelengths and update mask.
    dataset_out._wavelength = correctedWavelength.data
    dataset_out.mask = np.logical_or(dataset_out.mask,
                                     correctedWavelength.mask)
    dataset_out.isMovementCorrected = True

    if verbose:
        wnew = dataset_out.return_masked_array('wavelength')
        index_valid = np.ma.all(wnew[..., 0].mask, axis=1)
        index_valid = ~index_valid.data
        wnew = np.ma.median(wnew[index_valid, ...][1:8, ...], axis=1)
        wold = np.ma.median(datasetIn.wavelength[index_valid, ...][1:8, ...],
                            axis=1)
        sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2.5})
        sns.set_style("white", {"xtick.bottom": True, "ytick.left": True})
        fig, ax0 = plt.subplots(figsize=(6, 5), nrows=1, ncols=1)
        ax0.plot(wnew.T, zorder=5, lw=3)
        ax0.plot(wold.T, color='gray', zorder=4)
        ax0.set_ylabel('Wavelength [{}]'.format(datasetIn.wavelength_unit))
        ax0.set_xlabel('Integration #')
        ax0.set_title('Wavelength shifts')
        plt.show()
        if verboseSaveFile is not None:
            fig.savefig(verboseSaveFile, bbox_inches='tight')
    return dataset_out


def rebin_to_common_wavelength_grid(dataset, referenceIndex, nrebin=None,
                                    verbose=False, verboseSaveFile=None):
    """
    Rebin the spectra to single wavelength per row.

    Parameters
    ----------
    dataset : 'SpectralDataTimeSeries'
        Input dataset
    referenceIndex : 'int'
        Exposure index number which will be used as reference defining the
        uniform wavelength grid.
    nrebin : 'float', optional
        rebinning factor for the new wavelength grid compare to the old.
    verbose : 'bool', optional
        If True, diagnostic plots will be created
    verboseSaveFile : 'str', optional
        If not None, verbose output will be saved to the specified file.

    Returns
    -------
    rebinnedDataset : 'SpectralDataTimeSeries'
        Output to common wavelength grid rebinned dataset
    """
    if not isinstance(dataset, SpectralDataTimeSeries):
        raise TypeError("the input data to rebin_to_common_wavelength_grid "
                        "function needs to be a SpectralDataTimeSeries. "
                        "Aborting rebin to a common wavelength grid.")
    # all data with wavelength dependency + time
    spectra = dataset.return_masked_array('data')
    uncertainty = dataset.return_masked_array('uncertainty')
    wavelength = dataset.return_masked_array('wavelength')
    time = dataset.return_masked_array('time')

    # A pixel row (time) does not have the same wavelength in time
    # Need to find the miximum-lowest or minimum-higest wavelength for a
    # proper rebinning.
    min_wavelength = np.ma.min(np.ma.max(wavelength, axis=-1))
    max_wavelength = np.ma.max(np.ma.min(wavelength, axis=-1))

    referenceWavelength = np.sort(np.array(wavelength[1:-1, referenceIndex]))
    idx_min_select = np.where(referenceWavelength >= min_wavelength)[0][0]
    idx_max_select = np.where(referenceWavelength <= max_wavelength)[0][-1]
    referenceWavelength = referenceWavelength[idx_min_select:idx_max_select]

    lr, ur = _define_band_limits(wavelength)

    if nrebin is not None:
        referenceWavelength = \
            np.linspace(referenceWavelength[0+int(nrebin/2)],
                        referenceWavelength[-1-int(nrebin/2)],
                        int(len(referenceWavelength)/nrebin))
    lr0, ur0 = _define_band_limits(referenceWavelength)
    weights = _define_rebin_weights(lr0, ur0, lr, ur)
    rebinnedSpectra, rebinnedUncertainty = \
        _rebin_spectra(spectra, uncertainty, weights)
    rebinnedWavelength = np.tile(referenceWavelength,
                                 (rebinnedSpectra.shape[-1], 1)).T

    ndim = dataset.data.ndim
    selection = tuple((ndim-1)*[0]+[Ellipsis])

    dictTimeSeries = {}

    dictTimeSeries['data'] = rebinnedSpectra
    dictTimeSeries['data_unit'] = dataset.data_unit
    dictTimeSeries['uncertainty'] = rebinnedUncertainty
    dictTimeSeries['wavelength'] = rebinnedWavelength
    dictTimeSeries['wavelength_unit'] = dataset.wavelength_unit
    dictTimeSeries['time'] = time[selection]
    dictTimeSeries['time_unit'] = dataset.time_unit
    dictTimeSeries['isRebinned'] = True

    # get everything else apart from data, wavelength, time and uncertainty
    for key in vars(dataset).keys():
        if key[0] != "_":
            if isinstance(vars(dataset)[key], MeasurementDesc):
                measurement = getattr(dataset, key)
                dictTimeSeries[key] = measurement[selection]
            else:
                # print('can be added withour rebin')
                dictTimeSeries[key] = getattr(dataset, key)

    rebinnedDataset = SpectralDataTimeSeries(**dictTimeSeries)

    if verbose:
        index_valid = np.ma.all(wavelength.mask, axis=1)
        index_valid = ~index_valid.data
        sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2.5})
        sns.set_style("white", {"xtick.bottom": True, "ytick.left": True})
        fig, axes = plt.subplots(figsize=(10, 5), nrows=1, ncols=2)
        ax0, ax1 = axes.flatten()
        ax0.plot(rebinnedWavelength[1:6].T, zorder=5, lw=3)
        ax0.plot(wavelength[index_valid, :][2:7].T, color='gray', zorder=4)
        ax0.set_ylabel('Wavelength [{}]'.format(dataset.wavelength_unit))
        ax0.set_xlabel('Integration #')
        ax0.set_title('Rebinned Wavelengths')
        ax1.plot(rebinnedSpectra[1:6].T, zorder=5, lw=3)
        ax1.plot(spectra[index_valid, :][2:7].T, color='gray', zorder=4)
        ax1.set_ylabel('Flux [{}]'.format(dataset.data_unit))
        ax1.set_xlabel('Integration #')
        ax1.set_title('Rebinned Signal')
        fig.subplots_adjust(hspace=0.3)
        fig.subplots_adjust(wspace=0.45)
        plt.show()
        if verboseSaveFile is not None:
            fig.savefig(verboseSaveFile, bbox_inches='tight')
    return rebinnedDataset


