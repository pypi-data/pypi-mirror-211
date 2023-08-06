import logging
from typing import Dict

import numpy as np
from numpy.typing import NDArray

from ... import DataContainer
from ...core.hashing import list_to_hash
from .base_functional import Functional
from ..basis_sets.base_basis_set import BasisSet
from ..projectors.base_projector import Projector


logger = logging.getLogger(__name__)


class GradientFunctional(Functional):
    """Class that implements the GradientFunctional method.
    This ``Functional`` is an appropriate choice for :term:`SAXS` tensor tomography, as it relies
    on the small-angle approximation. It relies on inverting the John transform
    (also known as the X-ray transform) of a tensor field (where each tensor is a
    representation of a spherical function) by comparing it to scattering data which
    has been corrected for transmission.

    Parameters
    ----------
    data_container : DataContainer
        Container for the data which is to be reconstructed.
    basis_set : BasisSet
        The basis set used for representing spherical functions.
    projector : Projector
        The type of projector used together with this method.
    integration_samples : Optional, int
        Number of samples to use when calculating the mapping from the
        detector to the sphere. Defaults to ``11``, which is sufficiently dense
        without being computationally onerous. If a different method than
        binning detector pixels is used, e.g., fitting a function and selecting
        points from this function, a different nuimber, such as ``1``, may be
        a more appropriate choice.
    use_scalar_projections : bool
        Whether to use a stack of scalar_projections, rather than the data
        in :attr:`data_container`.
    scalar_projections : NDArray[float]
        If :attr:`use_scalar_projections` is true, the stack of scalar projections to use.
        Should have the same shape as :attr:`data_container.data`, except with
        only one channel in the last index.
    """

    def __init__(self,
                 data_container: DataContainer,
                 basis_set: BasisSet,
                 projector: Projector,
                 integration_samples: int = 11,
                 use_scalar_projections: bool = False,
                 scalar_projections: NDArray[float] = None):
        super().__init__(data_container, basis_set, projector, use_scalar_projections, scalar_projections)
        self._integration_samples = integration_samples
        # Check if full circle appears covered in data or not.
        delta = np.abs(self._detector_angles[0] -
                       self._detector_angles[-1] % (2 * np.pi))
        if abs(delta - np.pi) < min(delta, abs(delta - 2 * np.pi)) or use_scalar_projections:
            self._full_circle_covered = False
        else:
            logger.warning('The detector angles appear to cover a full circle.'
                           ' Friedel symmetry will be assumed in the calculation.\n'
                           'If this is incorrect, please set the property full_circle_covered'
                           ' to False.')
            self._full_circle_covered = True
        self._basis_set.probed_coordinates.vector = self._get_probed_coordinates()

    def get_residuals(self,
                      get_gradient: bool = False,
                      get_weights: bool = False) -> Dict:
        """ Calculates a residuals and possibly a gradient between
        coefficients projected using the :attr:`BasisSet` and :attr:`Projector`
        attached to this instance.

        Parameters
        ----------
        get_gradient
            Whether to return the gradient. Default is ``False``.
        get_weights
            Whether to return weights. Default is ``False``. If ``True`` along with
            :attr:`get_gradient`, the gradient will be computed with weights.

        Returns
        -------
            A dictionary containing the residuals, and possibly the
            gradient and/or weights. If gradient and/or weights
            are not returned, their value will be ``None``.
        """
        projection = self._basis_set.forward(self._projector.forward(self._coefficients))
        residuals = projection - self._data
        if get_gradient:
            # todo: consider if more complicated behaviour is useful,
            # e.g. providing function to be applied to weights
            if get_weights:
                gradient = self._projector.adjoint(
                    self._basis_set.gradient(residuals * self._weights).astype(self._dtype))
            else:
                gradient = self._projector.adjoint(
                    self._basis_set.gradient(residuals).astype(self._dtype))
        else:
            gradient = None

        if get_weights:
            weights = self._weights
        else:
            weights = None

        return dict(residuals=residuals, gradient=gradient, weights=weights)

    # Do not simply reuse contents of this method by copying and pasting, refactor instead.
    def _get_probed_coordinates(self) -> NDArray:
        """
        Calculates and returns the probed polar and azimuthal coordinates on the unit sphere at
        each angle of projection and for each detector segment in the system's geometry.
        """
        n_proj = len(self._data_container.geometry)
        n_seg = len(self._detector_angles)
        probed_directions_zero_rot = np.zeros((n_seg,
                                               self._integration_samples,
                                               3))
        # Impose symmetry if needed.
        if not self._full_circle_covered:
            shift = np.pi
        else:
            shift = 0
        det_bin_middles_extended = np.copy(self._detector_angles)
        det_bin_middles_extended = np.insert(det_bin_middles_extended, 0,
                                             det_bin_middles_extended[-1] + shift)
        det_bin_middles_extended = np.append(det_bin_middles_extended, det_bin_middles_extended[1] + shift)

        for ii in range(n_seg):

            # Check if the interval from the previous to the next bin goes over the -pi +pi discontinuity
            before = det_bin_middles_extended[ii]
            now = det_bin_middles_extended[ii + 1]
            after = det_bin_middles_extended[ii + 2]

            if abs(before - now + 2 * np.pi) < abs(before - now):
                before = before + 2 * np.pi
            elif abs(before - now - 2 * np.pi) < abs(before - now):
                before = before - 2 * np.pi

            if abs(now - after + 2 * np.pi) < abs(now - after):
                after = after - 2 * np.pi
            elif abs(now - after - 2 * np.pi) < abs(now - after):
                after = after + 2 * np.pi

            # Generate a linearly spaced set of angles covering the detector segment
            start = 0.5 * (before + now)
            end = 0.5 * (now + after)
            inc = (end - start) / self._integration_samples
            angles = np.linspace(start + inc / 2, end - inc / 2, self._integration_samples)

            # Make the zero-rotation-frame vectors corresponding to the given angles
            probed_directions_zero_rot[ii, :, :] = np.cos(angles[:, np.newaxis]) * \
                self._data_container.geometry.detector_direction_origin[np.newaxis, :]
            probed_directions_zero_rot[ii, :, :] += np.sin(angles[:, np.newaxis]) * \
                self._data_container.geometry.detector_direction_positive_90[np.newaxis, :]

        # Initialize array for vectors
        probed_direction_vectors = np.zeros((n_proj,
                                             n_seg,
                                             self._integration_samples,
                                             3), dtype=np.float64)
        # Calculate all the rotations
        probed_direction_vectors[...] = \
            np.einsum('kij,mli->kmlj',
                      self._data_container.geometry.rotations_as_array,
                      probed_directions_zero_rot)
        return probed_direction_vectors

    def get_gradient_from_residual_gradient(self, residual_gradient: NDArray[float]) -> Dict:
        """ Projects a residual gradient into coefficient and volume space. Used
        to get gradients from more complicated residuals, e.g., the Huber loss.
        Assumes that any weighting to the residual gradient has already been applied.

        Parameters
        ----------
        residual_gradient
            The residual gradient, from which to calculate the gradient.

        Returns
        -------
            An ``NDArray`` containing the gradient.
        """
        return self._projector.adjoint(
                    self._basis_set.gradient(residual_gradient).astype(self._dtype))

    def _update(self, force_update: bool = False) -> None:
        """ Carries out necessary updates if anything changes with respect to
        the geometry or basis set. """
        if not (self.is_dirty or force_update):
            return
        self._dtype = self._projector.dtype
        self._basis_set.probed_coordinates.vector = self._get_probed_coordinates()
        len_diff = len(self._basis_set) - self._coefficients.shape[-1]
        vol_diff = self._data_container.geometry.volume_shape - np.array(self._coefficients.shape[:-1])
        # TODO: Think about whether the ``Method`` should do this or handle it differently
        if np.any(vol_diff != 0) or len_diff != 0:
            logger.warning('Shape of coefficient array has changed, array will be padded'
                           ' or truncated.')
            # save old array, no copy needed
            old_coefficients = self._coefficients
            # initialize new array
            self._coefficients = \
                np.zeros((*self._data_container.geometry.volume_shape, len(self._basis_set)),
                         dtype=self._dtype)
            # for comparison of volume shapes
            shapes = zip(old_coefficients.shape[:-1], self._coefficients.shape[:-1])
            # old coefficients go into middle of new coefficients except in last index
            slice_1 = tuple([slice(max(0, (d-s) // 2), min(d, (s + d) // 2)) for s, d in shapes]) + \
                (slice(0, min(old_coefficients.shape[-1], self._coefficients.shape[-1])),)
            # zip objects are depleted
            shapes = zip(old_coefficients.shape[:-1], self._coefficients.shape[:-1])
            slice_2 = tuple([slice(max(0, (s-d) // 2), min(s, (s + d) // 2)) for s, d in shapes]) + \
                (slice(0, min(old_coefficients.shape[-1], self._coefficients.shape[-1])),)
            # assumption made that old_coefficients[..., 0] correspnds to self._coefficients[..., 0]
            self._coefficients[slice_1] = old_coefficients[slice_2]
            # Assumption may not be true for all representations!
            # TODO: Consider more logic here using e.g. basis set properties.
            if len_diff != 0:
                logger.warning('Size of basis set has changed. Coefficients have'
                               ' been copied over starting at index 0. If coefficients'
                               ' of new size do not line up with the old size,'
                               ' please reinitialize the coefficients.')
        self._geometry_hash = hash(self._data_container.geometry)
        self._basis_set_hash = hash(self._basis_set)

    @property
    def probed_coordinates(self) -> NDArray:
        """ An array of 3-vectors with the (x, y, z)-coordinates
        on the reciprocal space map probed by the method.
        Structured as ``(N, K, I, 3)``, where ``N``
        is the number of projections, ``K`` is the number of
        detector segments, ``I`` is the number of points to be
        integrated over, and the last axis contains the
        (x, y, z)-coordinates.

        Notes
        -----
        The region of the reciprocal space map spanned by
        each detector segment is represented as a parametric curve
        between each segment. This is intended to simulate the effect
        of summing up pixels on a detector screen. For other methods of
        generating data (e.g., by fitting measurements to a curve),
        it may be more appropriate to only include a single point, which
        will then have the same coordinates as the center of a detector
        segments. This can be achieved by setting the property
        :attr:`integration_samples`.
        """
        return self._get_probed_coordinates()

    def __hash__(self) -> int:
        """ Returns a hash of the current state of this instance. """
        to_hash = [self._coefficients,
                   self.probed_coordinates,
                   hash(self._projector),
                   hash(self._data_container.geometry),
                   self._basis_set_hash,
                   self._geometry_hash]
        return int(list_to_hash(to_hash), 16)

    @property
    def coefficients(self) -> NDArray:
        """Optimization coefficients for this method."""
        return self._coefficients

    @coefficients.setter
    def coefficients(self, val: NDArray) -> None:
        self._coefficients = val.reshape(self._coefficients.shape).astype(self._dtype)

    @property
    def is_dirty(self) -> bool:
        """ ``True`` if stored hashes of geometry or basis set objects do
        not match their current hashes. Used to trigger updates """
        return ((self._geometry_hash != hash(self._data_container.geometry)) or
                (self._basis_set_hash != hash(self._basis_set)))

    def __str__(self) -> str:
        wdt = 74
        s = []
        s += ['=' * wdt]
        s += [self.__class__.__name__.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=4, precision=5, linewidth=60, edgeitems=1):
            s += ['{:18} : {}'.format('BasisSet', self._basis_set.__class__.__name__)]
            s += ['{:18} : {}'.format('Projector', self._projector.__class__.__name__)]
            s += ['{:18} : {}'.format('is_dirty', self.is_dirty)]
            s += ['{:18} : {}'.format('probed_coordinates (hash)',
                                      list_to_hash([self.probed_coordinates])[:6])]
            s += ['{:18} : {}'.format('hash', hex(hash(self))[2:8])]
        s += ['-' * wdt]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += [f'<h3>{self.__class__.__name__}</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th><th>Data</th></tr></thead>']
        s += ['<tbody>']
        with np.printoptions(threshold=4, edgeitems=2, precision=2, linewidth=40):
            s += ['<tr><td style="text-align: left;">BasisSet</td>']
            s += [f'<td>{1}</td><td>{self._basis_set.__class__.__name__}</td></tr>']
            s += ['<tr><td style="text-align: left;">Projector</td>']
            s += [f'<td>{len(self._projector.__class__.__name__)}</td>'
                  f'<td>{self._projector.__class__.__name__}</td></tr>']
            s += ['<tr><td style="text-align: left;">Is dirty</td>']
            s += [f'<td>{1}</td><td>{self.is_dirty}</td></tr>']
            s += ['<tr><td style="text-align: left;">probed_coordinates</td>']
            s += [f'<td>{self.probed_coordinates.shape}</td>'
                  f'<td>{list_to_hash([self.probed_coordinates])[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">Hash</td>']
            h = hex(hash(self))
            s += [f'<td>{len(h)}</td><td>{h[2:8]}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return '\n'.join(s)
