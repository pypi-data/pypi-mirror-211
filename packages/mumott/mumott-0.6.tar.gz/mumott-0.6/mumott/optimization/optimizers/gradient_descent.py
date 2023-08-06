import logging

from typing import Dict, Any

import numpy as np

from ...core.hashing import list_to_hash
from .base_optimizer import Optimizer
from ..loss_functions.base_loss_function import LossFunction


logger = logging.getLogger(__name__)


class GradientDescent(Optimizer):
    """This Optimizer is a simple gradient descent (sometimes called steepest descent)
    solver, which can be set to terminate based on the loss function and/or the maximum
    number of iterations.

    Parameters
    ----------
    loss_function : LossFunction
        The :ref:`loss function <loss_functions>` to be minimized using this algorithm.
    kwargs : Dict[str, Any]
        Miscellaneous options. See notes for valid entries.

    Notes
    -----
    Valid entries in :attr:`kwargs` are
        x0
            Initial guess for solution vector. Must be the same size as
            :attr:`functional.coefficients`. Defaults to :attr:`loss_function.initial_values`.
        maxiter : int
            Maximum number of iterations. Default value is ``5``.
        ftol : float
            The tolerance for relative change in the loss function before
            termination. If ``None``, termination only occurs once :attr:`maxiter` iterations
            have been performed. Default value is ``None``.
        enforce_non_negativity : bool
            Enforces strict positivity on all the coefficients. Should only be used
            with local or scalar representations. Default value is ``False``.
    """

    def __init__(self,
                 loss_function: LossFunction,
                 **kwargs: Dict[str, Any]):
        super().__init__(loss_function, **kwargs)

    def optimize(self) -> Dict:
        """ Executes the optimization using the options stored in this class
        instance. The optimization will continue until convergence,
        or until the maximum number of iterations (:attr:`maxiter`) is exceeded.

        Returns
        -------
            A ``dict`` of optimization results. See `scipy.optimize.OptimizeResult
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html>`_
            for details. The entry ``'x'``, which contains the result, will be reshaped using
            the shape of the gradient from :attr:`loss_function`.
        """
        opt_kwargs = dict(x0=self._loss_function.initial_values,
                          ftol=None,
                          maxiter=5,
                          enforce_non_negativity=False)

        for k in opt_kwargs:
            if k in dict(self):
                opt_kwargs[k] = self[k]

        for k in dict(self):
            if k not in opt_kwargs:
                logger.warning(f'Unknown option {k}, with value {self[k]}, has been ignored.')
        coefficients = opt_kwargs['x0']

        if opt_kwargs['ftol'] is None:
            ftol = -np.inf
        else:
            ftol = opt_kwargs['ftol']

        previous_loss = -1
        for i in self._tqdm(opt_kwargs['maxiter']):
            if opt_kwargs['enforce_non_negativity']:
                np.clip(coefficients, 0, None, out=coefficients)
            d = self._loss_function.get_loss(coefficients, get_gradient=True)
            relative_change = (previous_loss - d['loss']) / d['loss']
            logger.info(f'Iteration: {i}\nLoss function: {d["loss"]}\nRelative change: {relative_change}')
            if i > 5 and relative_change < ftol:
                logger.info(f'Relative change ({relative_change}) is less than ftol ({ftol})!'
                            ' Optimization finished.')
                break
            coefficients -= d['gradient']
            previous_loss = d['loss']

        result = dict(x=coefficients, loss=d['loss'], nit=i+1)
        return dict(result)

    def __hash__(self) -> int:
        to_hash = [self._options, hash(self._loss_function)]
        return int(list_to_hash(to_hash), 16)
