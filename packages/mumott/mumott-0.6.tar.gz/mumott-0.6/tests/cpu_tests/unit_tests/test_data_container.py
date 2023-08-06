import pytest # noqa
import numpy as np
from mumott.data_handling import DataContainer


def test_load():
    dc = DataContainer('tests/test_half_circle.h5')
    assert np.allclose(dc.data.shape, (1, 4, 4, 3))
    assert np.allclose(dc.weights.shape, (1, 4, 4, 3))
    old_gm = dc.geometry
    old_frame = dc.stack[0]
    dc = DataContainer('tests/test_half_circle.h5', skip_data=True)
    assert np.allclose(dc.diode.shape, (1, 4, 4))
    assert np.allclose(dc.weights.shape, (1, 4, 4))
    assert np.allclose(dc.geometry[0].rotation, old_gm[0].rotation)
    assert np.allclose(dc.geometry[0].j_offset, old_gm[0].j_offset)
    assert np.allclose(dc.geometry[0].k_offset, old_gm[0].k_offset)
    assert hash(dc.geometry) != hash(old_gm)
    old_gm.projection_shape = dc.geometry.projection_shape
    old_gm.detector_angles = dc.geometry.detector_angles
    assert hash(dc.geometry) == hash(old_gm)
    assert np.all(dc.stack[0].data == np.array([]).reshape(0, 0))
    assert np.allclose(dc.stack[0].diode, old_frame.diode)
    assert np.allclose(dc.stack[0].weights, old_frame.weights[..., 0])


new_diode = np.arange(16).reshape(1, 4, 4)
new_diode_list = [new_diode[0].copy()]


def test_set_diode():
    dc = DataContainer('tests/test_half_circle.h5')
    dc.stack.diode = new_diode
    assert np.allclose(dc.diode, new_diode)
    assert np.allclose(dc.stack[0].diode, new_diode[0])
    dc.stack.diode = new_diode_list
    assert np.allclose(dc.diode, new_diode_list)
    assert np.allclose(dc.stack[0].diode, new_diode_list[0])


def test_set_weights():
    dc = DataContainer('tests/test_half_circle.h5', skip_data=True)
    dc.stack.weights = new_diode
    assert np.allclose(dc.weights, new_diode)
    assert np.allclose(dc.stack[0].weights, new_diode[0])
    dc.stack.weights = new_diode_list
    assert np.allclose(dc.weights, new_diode_list)
    assert np.allclose(dc.stack[0].weights, new_diode_list[0])


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    s = str(dc)
    assert s.count('\n') <= 50


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    s = dc._repr_html_()
    assert s.count('</tr>') <= 25


def test_correct_for_transmission():
    dc = DataContainer('tests/test_half_circle.h5')
    dc.stack.diode = dc.diode * 0.5
    data = dc.stack.data
    dc.correct_for_transmission()
    assert np.allclose(data * 2, dc.stack.data)
    assert dc._correct_for_transmission_called


def test_get_str():
    dc = DataContainer('tests/test_half_circle.h5')
    s = dc._get_str_representation(5)
    assert s.count('\n') <= 6


def test_get_html():
    dc = DataContainer('tests/test_half_circle.h5')
    s = dc._get_html_representation(5)
    assert s.count('</tr>') <= 6
