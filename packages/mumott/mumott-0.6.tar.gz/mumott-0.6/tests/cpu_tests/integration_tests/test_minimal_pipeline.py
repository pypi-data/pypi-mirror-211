import pytest # noqa
from io import StringIO
import logging
import numba
import numpy as np
from mumott.data_handling import DataContainer
from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.functionals import GradientFunctional
from mumott.optimization.loss_functions import SquaredLoss
from mumott.optimization.optimizers import LBFGS


def test_minimal_pipeline():
    numba.config.NUMBA_NUM_THREADS = 1
    numba.set_num_threads(1)

    # check that the functionality for deleting frames works
    data_container = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    stack = data_container.stack
    assert len(stack) == 1
    del stack[0]
    assert len(stack) == 0

    # minimal check for append functionality
    dc1 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    stack1 = dc1.stack
    dc2 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    stack2 = dc2.stack
    assert len(stack1) == 1
    frame = stack2[0]
    del stack2[0]
    stack1.append(frame)
    assert len(stack1) == 2

    # minimal check for setitem functionality
    dc1 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    dc2 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    frame = dc2.stack[0]
    frame.j_offset = 1.243

    assert dc2.geometry.j_offsets[0] == 1.243

    dc2.geometry.k_offsets[0] = 4.214

    assert frame.k_offset == 4.214

    assert dc2.stack.geometry[0] == frame.geometry

    del dc2.stack[0]

    assert frame.j_offset == 1.243
    assert frame.k_offset == 4.214
    frame.data[0][0] = [1, 2, 3]
    dc1.stack[0] = frame

    assert np.all(dc1.stack[0].data[0][0] == [1, 2, 3])
    assert dc1.stack[0].j_offset == 1.243
    assert dc1.stack[0].k_offset == 4.214
    assert dc1.stack[0].geometry == dc1.stack.geometry[0]

    # load data container and check its basic output
    data_container = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    s = str(data_container)
    assert 'DataContainer' in s
    assert 'Corrected for transmission' in s
    assert 'Corrected for transmission' in s
    s = data_container._repr_html_()
    assert 'DataContainer' in s
    assert 'Corrected for transmission' in s
    assert 'Corrected for transmission' in s

    s = str(data_container.geometry)
    assert 'Geometry' in s
    s = data_container.geometry._repr_html_()
    assert 'Geometry' in s
    s = str(data_container.stack)
    assert 'Stack' in s
    s = data_container.stack._repr_html_()
    assert 'Stack' in s

    s = str(data_container.stack[0])
    assert 'Frame' in s
    assert 'diode' in s
    assert 'dcf160' in s
    s = data_container.stack[0]._repr_html_()
    assert 'Frame' in s
    assert 'diode' in s
    assert 'dcf160' in s

    bs = SphericalHarmonics(ell_max=6)
    pr = SAXSProjectorNumba(data_container.geometry)
    meth = GradientFunctional(data_container, bs, pr)
    lf = SquaredLoss(meth)
    optimizer = LBFGS(lf, maxiter=5)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    # - send logging to stream
    f = StringIO()
    logging.basicConfig(stream=f, level=logging.INFO)
    # run optimization
    optimizer.optimize()

    # check that coefficients are correct
    coeffs = meth.coefficients
    assert coeffs.size == 1792
    reference_coeffs = np.array(
        [0.87601399, 0.08113027, -0.00716787,  0.48052269, -0.15047219, 0.84963459,
         0.13741241, -0.01485878, 0.05635246, -0.00441374,  0.31243902, -0.09265587,
         0.5901497, -0.10334509, 0.71296326, 0.18458887, -0.01809086, 0.10050705,
         -0.01510339, 0.04192086, -0.00137633,  0.26808559, -0.02889264, 0.43901513,
         -0.10504635, 0.52148008, -0.07457155,  0.62865195, 0.88099492, 0.07854443,
         -0.01004529, 0.53877781, -0.21087649,  0.82255451, 0.1297739, -0.02188681,
         0.0632176, -0.00524503, 0.29931401, -0.11010673])

    print(coeffs.ravel()[:40])
    assert np.allclose(coeffs.ravel()[:40], reference_coeffs)
