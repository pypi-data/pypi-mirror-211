from abc import ABC, abstractmethod
from typing import Dict

import numpy as np
from numpy.typing import NDArray

from ... import DataContainer
from ..basis_sets.base_basis_set import BasisSet
from ..projectors.base_projector import Projector


class Functional(ABC):

    """This is the base class from which specific functionals are being derived.
    """

    def __init__(self,
                 data_container: DataContainer,
                 basis_set: BasisSet,
                 projector: Projector,
                 use_scalar_projections: bool = False,
                 scalar_projections: NDArray[float] = None):
        self._data_container = data_container
        self._geometry_hash = hash(data_container.geometry)
        self._basis_set = basis_set
        self._basis_set_hash = hash(self._basis_set)
        self._projector = projector
        # GPU-based projectors need float32
        self._dtype = projector.dtype
        self._coefficients = np.zeros((*self._data_container.geometry.volume_shape,
                                      len(self._basis_set)), dtype=self._dtype)
        self._use_scalar_projections = use_scalar_projections
        self._scalar_projections = scalar_projections

    @abstractmethod
    def get_residuals(self) -> Dict:
        pass

    @property
    def _data(self) -> NDArray:
        """ Internal method for choosing between scalar_projections and data. """
        if self._use_scalar_projections:
            return self._scalar_projections
        else:
            return self._data_container.data

    @property
    def _weights(self) -> NDArray:
        """ Internal method for choosing between weights for the
        scalar_projections or weights for the data. """
        if self._use_scalar_projections:
            return np.mean(self._data_container.weights, axis=-1)[..., None]
        else:
            return self._data_container.weights

    @property
    def _detector_angles(self) -> NDArray:
        """ Internal method for choosing between detector angles for the data
        or detector angles for the scalar_projections. """
        if self._use_scalar_projections:
            return np.array((0.,))
        else:
            return self._data_container.geometry.detector_angles

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def _repr_html_(self) -> str:
        pass
