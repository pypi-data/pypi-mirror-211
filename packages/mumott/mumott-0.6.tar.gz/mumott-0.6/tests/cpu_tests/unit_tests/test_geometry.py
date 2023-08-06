import pytest
import numpy as np

from mumott import Geometry
from mumott.data_handling.geometry import GeometryTuple


tuple_list = [GeometryTuple(rotation=np.eye(3), j_offset=0.3, k_offset=0.7),
              GeometryTuple(rotation=np.eye(3) * 0.732, j_offset=0.3, k_offset=0.7),
              GeometryTuple(rotation=-np.eye(3), j_offset=0.3, k_offset=0.7)]

rotation_array = np.array([[[0.955336, 0.190379, 0.226026],
                           [0., 0.764842, -0.644218],
                           [-0.2955, 0.615445,  0.730682]],
                          [[0.955336, 0.190379,  0.226026],
                           [0., 0.764842, -0.644218],
                           [-0.29552, 0.615445,  0.730682]]])

rotation_list = [np.array([[0.955336, 0.190379, 0.226026],
                          [0., 0.764842, -0.644218],
                          [-0.2955, 0.615445,  0.730682]]),
                 np.array([[0.955336, 0.190379,  0.226026],
                          [0., 0.764842, -0.644218],
                          [-0.29552, 0.615445,  0.730682]])]

j_list = [0.7, 0.8, 0.4]
k_list = [0.3, 0.5, 0.1]

j_array = np.array([2.1, -1, 0.2322])
k_array = np.array([2.1, -1, 0.2322])


@pytest.mark.parametrize('test_list', [(tuple_list)])
def test_input_output(test_list, tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'test.geo'
    g = Geometry()
    for t in tuple_list:
        g.append(t)
    for a, b in zip(g, tuple_list):
        assert np.allclose(a.rotation, b.rotation)
        assert np.isclose(a.j_offset, b.j_offset)
        assert np.isclose(a.k_offset, b.k_offset)
    g.write(p)
    k = Geometry()
    k.read(p)
    for a, b in zip(k, tuple_list):
        assert np.allclose(a.rotation, b.rotation)
        assert np.isclose(a.j_offset, b.j_offset)
        assert np.isclose(a.k_offset, b.k_offset)
    assert hash(k) == hash(g)
    m = Geometry(p)
    for a, b in zip(m, tuple_list):
        assert np.allclose(a.rotation, b.rotation)
        assert np.isclose(a.j_offset, b.j_offset)
        assert np.isclose(a.k_offset, b.k_offset)
    assert hash(g) == hash(m)


@pytest.mark.parametrize('test_list,test_array', [(rotation_list, rotation_array)])
def test_rotation_list_array(test_list, test_array):
    g = Geometry()
    print(test_array)
    print(test_list)
    g.rotations = test_array
    assert np.allclose(g.rotations_as_array, test_array)
    for a, b in zip(g, test_array):
        assert np.allclose(a.rotation, b)
    for a, b in zip(g.rotations, test_array):
        assert np.allclose(a, b)

    g.rotations = test_list
    assert np.allclose(g.rotations_as_array, test_list)
    for a, b in zip(g, test_list):
        assert np.allclose(a.rotation, b)
    for a, b in zip(g.rotations, test_list):
        assert np.allclose(a, b)


@pytest.mark.parametrize('test_list,test_array', [(j_list, j_array)])
def test_j_list_array(test_list, test_array):
    g = Geometry()
    g.j_offsets = test_array
    assert np.allclose(g.j_offsets_as_array, test_array)
    for a, b in zip(g, test_array):
        assert np.allclose(a.j_offset, b)
    for a, b in zip(g.j_offsets, test_array):
        assert np.allclose(a, b)

    g.j_offsets = test_list
    assert np.allclose(g.j_offsets, test_list)
    for a, b in zip(g, test_list):
        assert np.allclose(a.j_offset, b)
    for a, b in zip(g.j_offsets, test_list):
        assert np.allclose(a, b)


@pytest.mark.parametrize('test_list,test_array',  [(k_list, k_array)])
def test_k_list_array(test_list, test_array):
    g = Geometry()
    g.k_offsets = test_array
    assert np.allclose(g.k_offsets_as_array, test_array)
    for a, b in zip(g, test_array):
        assert np.allclose(a.k_offset, b)
    for a, b in zip(g.k_offsets, test_array):
        assert np.allclose(a, b)

    g.k_offsets = test_list
    assert np.allclose(g.k_offsets, test_list)
    for a, b in zip(g, test_list):
        assert np.allclose(a.k_offset, b)
    for a, b in zip(g.k_offsets, test_list):
        assert np.allclose(a, b)


def test_empty_hash():
    g = Geometry()
    assert str(hash(g))[:6] == '135563'
    assert g.hash_rotations[:6] == '786a02'
    assert g.hash_j_offsets[:6] == '786a02'
    assert g.hash_k_offsets[:6] == '786a02'


hash_list = ['119687', '134744', '334171']


@pytest.mark.parametrize('tup,hsh', [t for t in zip(tuple_list, hash_list)])
def test_gm_tuple_hash(tup, hsh):
    assert str(hash(tup))[:6] == hsh
