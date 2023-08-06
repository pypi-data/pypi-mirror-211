import logging

from typing import Tuple

import numpy as np
from numpy.typing import NDArray
from numba.cuda import is_cuda_array

from ...core.cuda_utils import cuda_calloc
from ...core.john_transform_cuda import john_transform_cuda, john_transform_adjoint_cuda
from ...core.hashing import list_to_hash
from ... import Geometry
from .base_projector import Projector

logger = logging.getLogger(__name__)


class SAXSProjectorCUDA(Projector):
    """
    Projector for transforms of tensor fields from three-dimensional space
    to projection space. Uses a projection algorithm implemented in
    ``numba.cuda``.

    Parameters
    ----------
    geometry : Geometry
        An instance of :class:`Geometry <mumott.Geometry>` containing the
        necessary vectors to compute forwared and adjoint projections.
    """
    def __init__(self,
                 geometry: Geometry):

        super().__init__(geometry)
        self._update(force_update=True)

    def _get_john_transform_parameters(self,
                                       indices: NDArray[int] = None) -> Tuple:
        if indices is None:
            indices = np.arange(len(self._geometry))
        vector_p = self._basis_vector_projection[indices]
        vector_j = self._basis_vector_j[indices]
        vector_k = self._basis_vector_k[indices]
        j_offsets = self._geometry.j_offsets_as_array[indices]
        k_offsets = self._geometry.k_offsets_as_array[indices]
        return (vector_p, vector_j, vector_k, j_offsets, k_offsets)

    @staticmethod
    def _get_zeros_method(array: NDArray):
        """ Internal method for returning `cupy` or `numpy` based on the type of array given. """
        if is_cuda_array(array):
            return cuda_calloc
        else:
            return np.zeros

    def forward(self,
                field: NDArray[np.float32],
                indices: NDArray[int] = None) -> NDArray:
        """ Compute the forward projection of a tensor field.

        Parameters
        ----------
        field
            An array containing coefficients in its fourth dimension,
            which are to be projected into two dimensions. The first three
            dimensions should match the :attr:`volume_shape` of the sample.
            Can be either a ``numpy.ndarray`` or any array that implements
            the CUDA array interface. Must be single-precision.
        indices
            A one-dimensional array containing one or more indices
            indicating which projections are to be computed. If ``None``,
            all projections will be computed.

        Returns
        -------
            An array with four dimensions ``(I, J, K, L)``, where
            the first dimension matches :attr:`indices`, such that
            ``projection[i]`` corresponds to the geometry of projection
            ``indices[i]``. The second and third dimension contain
            the pixels in the ``J`` and ``K`` dimension respectively, whereas
            the last dimension is the coefficient dimension, matching ``field[-1]``.
        """
        if not np.allclose(field.shape[:-1], self._geometry.volume_shape):
            raise ValueError(f'The shape of the input field ({field.shape}) does not match the'
                             f' volume shape expected by the projector ({self._geometry.volume_shape})')
        self._update()
        if indices is None:
            return self._forward_stack(field)
        return self._forward_subset(field, indices)

    def _forward_subset(self,
                        field: NDArray[np.float32],
                        indices: NDArray[int]) -> NDArray:
        """ Internal method for computing a subset of projections.

        Parameters
        ----------
        field
            The field to be projected. Must be single-precision.
        indices
            The indices indicating the subset of all projections in the
            system geometry to be computed.

        Returns
        -------
            The resulting projections.
        """
        indices = np.array(indices).ravel()
        self._check_indices_kind_is_integer(indices)
        init_method = self._get_zeros_method(field)
        projections = init_method((indices.size,) +
                                  tuple(self._geometry.projection_shape) +
                                  (field.shape[-1],), dtype=np.float32)
        john_transform_cuda(field, projections, *self._get_john_transform_parameters(indices))
        return projections

    def _forward_stack(self,
                       field: NDArray[np.float32]) -> NDArray:
        """Internal method for forward projecting an entire stack.

        Parameters
        ----------
        field
            The field to be projected. Must be single-precision.

        Returns
        -------
            The resulting projections.
        """
        init_method = self._get_zeros_method(field)
        projections = init_method((len(self._geometry),) +
                                  tuple(self._geometry.projection_shape) +
                                  (field.shape[-1],), dtype=np.float32)
        john_transform_cuda(field, projections, *self._get_john_transform_parameters())
        return projections

    def adjoint(self,
                projections: NDArray[np.float32],
                indices: NDArray[int] = None) -> NDArray:
        """ Compute the adjoint of a set of projections according to the system geometry.

        Parameters
        ----------
        projections
            An array containing coefficients in its last dimension,
            from, e.g., the residual of measured data and forward projections.
            The first dimension should match :attr:`indices` in size, and the
            second and third dimensions should match the system projection geometry.
            Can be either a ``numpy.ndarray`` or any array that implements
            the CUDA array interface. Must be single-precision.
        indices
            A one-dimensional array containing one or more indices
            indicating from which projections the adjoint is to be computed.

        Returns
        -------
            The adjoint of the provided projections.
            An array with four dimensions ``(X, Y, Z, P)``, where the first
            three dimensions are spatial and the last dimension runs over
            coefficients.
        """
        if not np.allclose(projections.shape[-3:-1], self._geometry.projection_shape):
            raise ValueError(f'The shape of the projections ({projections.shape}) does not match the'
                             f' projection shape expected by the projector'
                             f' ({self._geometry.projection_shape})')
        self._update()
        if indices is None:
            return self._adjoint_stack(projections)
        return self._adjoint_subset(projections, indices)

    def _adjoint_subset(self,
                        projections: NDArray[np.float32],
                        indices: NDArray[int]) -> NDArray:
        """ Internal method for computing the adjoint of only a subset of projections.

        Parameters
        ----------
        projections
            An array containing coefficients in its last dimension,
            from, e.g., the residual of measured data and forward projections.
            The first dimension should match :attr:`indices` in size, and the
            second and third dimensions should match the system projection geometry.
            Must be single-precision.
        indices
            A one-dimensional array containing one or more indices
            indicating from which projections the adjoint is to be computed.

        Returns
        -------
            The adjoint of the provided projections.
            An array with four dimensions ``(X, Y, Z, P)``, where the first
            three dimensions are spatial and the last dimension runs over
            coefficients. """
        indices = np.array(indices).ravel()
        if projections.ndim == 3:
            assert indices.size == 1
            projections = projections[np.newaxis, ...]
        else:
            assert indices.size == projections.shape[0]
        self._check_indices_kind_is_integer(indices)
        init_method = self._get_zeros_method(projections)
        field = init_method(tuple(self._geometry.volume_shape) +
                            (projections.shape[-1],), dtype=np.float32)
        # Note that we assume projections match ``indices`` in their layout.
        john_transform_adjoint_cuda(field,
                                    projections[indices],
                                    *self._get_john_transform_parameters(indices))
        return field

    def _adjoint_stack(self,
                       projections: NDArray[np.float32]) -> NDArray:
        """ Internal method for computing the adjoint of a whole stack of projections.

        Parameters
        ----------
        projections
            An array containing coefficients in its last dimension,
            from e.g. the residual of measured data and forward projections.
            The first dimension should run over all the projection directions
            in the system geometry. Must be single-precision.

        Returns
        -------
            The adjoint of the provided projections.
            An array with four dimensions ``(X, Y, Z, P)``, where the first
            three dimensions are spatial, and the last dimension runs over
            coefficients. """
        assert projections.shape[0] == len(self._geometry)
        init_method = self._get_zeros_method(projections)
        field = init_method(tuple(self._geometry.volume_shape) +
                            (projections.shape[-1],), dtype=np.float32)
        john_transform_adjoint_cuda(field, projections, *self._get_john_transform_parameters())
        return field

    def __hash__(self) -> int:
        to_hash = [self._basis_vector_projection,
                   self._basis_vector_j,
                   self._basis_vector_k,
                   self._geometry_hash,
                   hash(self._geometry)]
        return int(list_to_hash(to_hash), 16)

    def __str__(self) -> str:
        wdt = 74
        s = []
        s += ['-' * wdt]
        s += [self.__class__.__name__.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=4, edgeitems=2, precision=5, linewidth=60):
            s += ['{:18} : {}'.format('is_dirty', self.is_dirty)]
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
            s += ['<tr><td style="text-align: left;">is_dirty</td>']
            s += [f'<td>1</td><td>{self.is_dirty}</td></tr>']
            s += ['<tr><td style="text-align: left;">hash</td>']
            s += [f'<td>{len(hex(hash(self)))}</td><td>{hex(hash(self))[2:8]}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return '\n'.join(s)
