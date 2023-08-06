import pytest # noqa
import numpy as np
from mumott.pipelines import run_sirt, run_sigtt, run_cross_correlation_alignment
from mumott.data_handling import DataContainer
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.functionals import GradientFunctional
from mumott.methods.basis_sets import SphericalHarmonics, TrivialBasis
from mumott.optimization.loss_functions import SquaredLoss, HuberLoss
from mumott.optimization.regularizers import Laplacian, L1Norm
from mumott.optimization.optimizers import GradientDescent, LBFGS


@pytest.fixture
def data_container():
    return DataContainer('tests/test_half_circle.h5')


def test_sirt(data_container):
    result = run_sirt(data_container, maxiter=2)
    assert result['result']['loss'] == 0
    assert isinstance(result['basis_set'], TrivialBasis)
    assert result['projector']._geometry == data_container.geometry
    assert result['basis_set'].channels == 1
    result = run_sirt(data_container, use_absorbances=False, maxiter=2)
    assert result['projector']._geometry == data_container.geometry
    assert np.isclose(result['result']['loss'], 46893.607)
    assert isinstance(result['projector'], SAXSProjectorNumba)
    assert isinstance(result['functional'], GradientFunctional)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert isinstance(result['loss_function'], SquaredLoss)
    assert isinstance(result['optimizer'], GradientDescent)


def test_sirt_kwargs(data_container):
    result = run_sirt(data_container,
                      preconditioner_cutoff=0,
                      weights_cutoff=0,
                      maxiter=3,
                      absorbances=data_container.diode,
                      projector=SAXSProjectorNumba,
                      BasisSet=SphericalHarmonics,
                      basis_set_kwargs=dict(ell_max=2),
                      Functional=GradientFunctional,
                      functional_kwargs=dict(use_scalar_projections=False,
                                             scalar_projections=data_container.diode[..., None]),
                      Regularizers=[dict(name='l1', regularizer=L1Norm(), regularization_weight=1e-3)],
                      LossFunction=HuberLoss,
                      loss_function_kwargs=dict(delta=1e2),
                      Optimizer=GradientDescent,
                      optimizer_kwargs=dict(ftol=1e-1))
    assert isinstance(result['projector'], SAXSProjectorNumba)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['functional'], GradientFunctional)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert result['basis_set'].ell_max == 2
    assert not result['functional']._use_scalar_projections
    assert isinstance(result['loss_function'].regularizers['l1'], L1Norm)
    assert isinstance(result['loss_function'], HuberLoss)
    assert np.isclose(result['loss_function']._delta, 1e2)
    assert isinstance(result['optimizer'], GradientDescent)
    assert np.isclose(result['optimizer']['ftol'], 1e-1)
    assert np.isclose(result['result']['loss'], 15.429036)


def test_sigtt_kwargs(data_container):
    result = run_sigtt(data_container,
                       maxiter=3,
                       projector=SAXSProjectorNumba,
                       BasisSet=SphericalHarmonics,
                       basis_set_kwargs=dict(ell_max=4),
                       Functional=GradientFunctional,
                       functional_kwargs=dict(use_scalar_projections=False,
                                              scalar_projections=data_container.diode[..., None]),
                       Regularizers=[dict(name='l1', regularizer=L1Norm(), regularization_weight=1e-3)],
                       LossFunction=HuberLoss,
                       loss_function_kwargs=dict(delta=1e2),
                       Optimizer=GradientDescent,
                       optimizer_kwargs=dict(ftol=1e-1))
    assert isinstance(result['projector'], SAXSProjectorNumba)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['functional'], GradientFunctional)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert result['basis_set'].ell_max == 4
    assert not result['functional']._use_scalar_projections
    assert isinstance(result['loss_function'].regularizers['l1'], L1Norm)
    assert isinstance(result['loss_function'], HuberLoss)
    assert np.isclose(result['loss_function']._delta, 1e2)
    assert isinstance(result['optimizer'], GradientDescent)
    assert np.isclose(result['optimizer']['ftol'], 1e-1)
    assert np.isclose(result['result']['loss'], 13.13452)


def test_sigtt(data_container):
    result = run_sigtt(data_container)
    assert np.isclose(result['result']['fun'], 0.045408)
    assert isinstance(result['projector'], SAXSProjectorNumba)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['functional'], GradientFunctional)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert isinstance(result['loss_function'], SquaredLoss)
    assert isinstance(result['loss_function'].regularizers['laplacian'], Laplacian)
    assert isinstance(result['optimizer'], LBFGS)
    assert result['basis_set'].ell_max == 2


def test_alignment_upsampled(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.stack[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, reconstruction_pipeline_kwargs=dict(maxiter=1,
                                    use_absorbances=True),
                                    maxiter=5, shift_tolerance=0.001, upsampling=20, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0.)
    assert 'Maximal number of iterations' in caplog.text
    assert 'Maximal shift' not in caplog.text
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, 2.934)
    assert np.allclose(data_container.geometry.k_offsets, 2.596)
    with pytest.raises(ValueError, match='align_j and align_k'):
        run_cross_correlation_alignment(data_container, align_j=False, align_k=False)


def test_alignment(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.stack[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, reconstruction_pipeline_kwargs=dict(maxiter=1,
                                    use_absorbances=False),
                                    maxiter=5, shift_tolerance=0.001, upsampling=20, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0.)
    assert 'Maximal number of iterations' in caplog.text
    assert 'Maximal shift' not in caplog.text
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, -0.4659999)
    assert np.allclose(data_container.geometry.k_offsets, -1.50399999)


def test_alignment_no_k(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.stack[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, reconstruction_pipeline_kwargs=dict(maxiter=1,
                                    use_absorbances=False),
                                    maxiter=5, shift_tolerance=0.001, upsampling=20, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0., align_k=False)
    assert 'Maximal number of iterations' in caplog.text
    assert 'Maximal shift' not in caplog.text
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, -0.4659999)
    assert np.allclose(data_container.geometry.k_offsets, -0.754)


def test_alignment_no_j(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.stack[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, reconstruction_pipeline_kwargs=dict(maxiter=1,
                                    use_absorbances=True),
                                    maxiter=5, shift_tolerance=0.001, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0., align_j=False)
    assert 'Maximal number of iterations' not in caplog.text
    assert 'Maximal shift' in caplog.text
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, 0.534)
    assert np.allclose(data_container.geometry.k_offsets, -2.754)
