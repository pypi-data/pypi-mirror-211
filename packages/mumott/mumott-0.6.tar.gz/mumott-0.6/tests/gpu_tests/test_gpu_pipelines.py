import pytest # noqa
import numpy as np
from mumott.pipelines import run_sirt, run_sigtt, run_cross_correlation_alignment
from mumott.data_handling import DataContainer


@pytest.fixture
def data_container():
    return DataContainer('tests/test_half_circle.h5')


def test_sirt(data_container):
    result = run_sirt(data_container, maxiter=2, use_gpu=True)
    assert result['result']['loss'] == 0
    result = run_sirt(data_container, use_absorbances=False, maxiter=2, use_gpu=True)
    assert np.isclose(result['result']['loss'], 45226.69)


def test_sigtt(data_container):
    result = run_sigtt(data_container, use_gpu=True)
    print(result.keys())
    assert np.isclose(result['result']['fun'], 370.998)


def test_alignment(data_container, caplog):
    data_container.geometry.j_offsets[0] = -1.3
    data_container.geometry.k_offsets[0] = -2.213
    data_container.stack[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, reconstruction_pipeline_kwargs=dict(maxiter=1,
                                    use_absorbances=False), use_gpu=True,
                                    maxiter=5, shift_tolerance=0.001, upsampling=25, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0.)
    assert 'Maximal number of iterations' in caplog.text
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, -1.38)
    assert np.allclose(data_container.geometry.k_offsets, -2.013)
    with pytest.raises(ValueError, match='align_j and align_k'):
        run_cross_correlation_alignment(data_container, use_gpu=True, align_j=False, align_k=False)
