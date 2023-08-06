import logging

import numpy as np
from numpy.typing import NDArray

from ..projectors.base_projector import Projector

logger = logging.getLogger(__name__)


def get_sirt_preconditioner(projector: Projector, cutoff: int = 200) -> NDArray[float]:
    r""" Retrieves the :term:`SIRT` preconditioner, which can be used together
    with the :term:`SIRT` weights to condition the
    gradient of tomographic calculations for faster convergence and scaling of the
    step size for gradient descent.

    Notes
    -----
    The preconditioner normalizes the gradient according to the number
    of data points that map to each voxel in the computation of
    the projection adjoint. This preconditioner scales and conditions
    the gradient for better convergence. It is best combined with the :term:`SIRT`
    weights, which normalize the residual for the number of voxels.
    When used together, they condition the reconstruction sufficiently
    well that a gradient descent optimizer with step size unity can arrive
    at a good solution. Other gradient-based solvers can also benefit from this
    preconditioning.

    In addition, the calculation of these preconditioning terms makes it easy to identify
    regions of the volume or projections that are rarely probed, allowing them to be
    masked from the solution altogether.

    If the projection operation is written in sparse matrix form as

    .. math::
        P_{ij} X_{j} = Y_i

    where :math:`P_{ij}` is the projection matrix, :math:`X_j` is a vector of voxels, and :math:`Y_i`
    is the projection, then the preconditioner can be understood as

    .. math::
        C_{jj} = \frac{I(n_j)}{\sum_i P_{ij}}

    where :math:`I(n_j)` is the identity matrix of the same size as :math:`X_j`. Similarly,
    the weights (of :func:`~.get_sirt_weights`) are computed as

    .. math::
        W_{ii} = \frac{I(n_i)}{\sum_j P_{ij}}.

    Here, any singularities in the system (e.g., where :math:`\sum_j P_{ij} = 0`) can be masked out
    by setting the corresponding weight to zero.
    We thus end up with a weighted least-squares system

    .. math::
        \text{argmin}_X(\Vert W_{ii}(P_{ij}X_{j} - D_{i})\Vert^2_2)

    where :math:`D_{i}` is some data, which we can solve iteratively by preconditioned gradient descent,

    .. math::
        X_j^{k + 1} = X_j^k - C_{jj}P_{ji}^TW_{ii}(P_ij X_j^k - D_i)

    As mentioned, we can add additional regularization terms, and because the preconditioning
    scales the problem appropriately, computing an optimal step size is not a requirement,
    although it can speed up the solution. This establishes a very flexible system, where
    quasi-Newton solvers such as :term:`LBFGS` can be seamlessly combined with less restrictive
    gradient descent methods.

    A good discussion of the algorithmic properties of :term:`SIRT` can be found in
    `this article by Gregor *et al.* <https://doi.org/10.1109%2FTCI.2015.2442511>`_,
    while `this article by van der Sluis *et al.* <https://doi.org/10.1016/0024-3795(90)90215-X>`_
    discusses :term:`SIRT` as a least squares solver in comparison to the
    conjugate gradient (:term:`CG`) method.

    Parameters
    ----------
    projector
        A :class:`Projector <insert_reference>` object which is used to calculate the weights.
        The computation of the weights is based on the geometry attached to the projector.
    cutoff
        The minimal number of rays that need to map to a voxel for it
        to be considered valid. Default is ``200``. Invalid voxels will
        be masked from the preconditioner.
    """
    sirt_projections = np.ones((projector.number_of_projections,) +
                               projector.projection_shape +
                               (1,), dtype=projector.dtype)
    inverse_preconditioner = projector.adjoint(sirt_projections)
    mask = (inverse_preconditioner > cutoff).astype(int)
    return mask * np.reciprocal(inverse_preconditioner + 1 - mask)


def get_sirt_weights(projector: Projector, cutoff: int = 10) -> NDArray[float]:
    """ Retrieves the :term:`SIRT` weights, which can be used together with the
    :term:`SIRT` preconditioner to weight the
    residual of tomographic calculations for faster convergence and
    scaling of the step size for gradient descent.

    Notes
    -----
    See :func:`~.get_sirt_preconditioner` for theoretical details.

    Parameters
    ----------
    projector
        A :class:`Projector <insert_reference>` object which is used to calculate the weights.
        The computation of the weights is based on the geometry attached to the projector.
    cutoff
        The minimal number of voxels that need to map to a point for it
        to be considered valid. Default is ``10``. Invalid pixels will be
        masked.
    """
    sirt_field = np.ones(projector.volume_shape +
                         (1,), dtype=projector.dtype)
    inverse_weights = projector.forward(sirt_field)
    mask = (inverse_weights > cutoff).astype(int)
    return mask * np.reciprocal(projector.forward(sirt_field) + 1 - mask)
