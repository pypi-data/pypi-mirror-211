import pytest # noqa
import numpy as np
from mumott.data_handling import DataContainer
from mumott.data_handling.stack import Stack, Frame
from mumott.data_handling.geometry import GeometryTuple


def test_hashes():
    dc = DataContainer('tests/test_half_circle.h5')
    assert dc.stack[0].hash_data.startswith('ab1de1')
    assert dc.stack[0].hash_diode.startswith('dcf160')
    assert dc.stack[0].hash_weights.startswith('65e22e')
    assert dc.stack.hash_data.startswith('ab1de1')
    assert dc.stack.hash_diode.startswith('dcf160')
    assert dc.stack.hash_weights.startswith('65e22e')
    dc = DataContainer('tests/test_full_circle.h5')
    assert dc.stack[0].hash_data.startswith('475981')
    assert dc.stack[0].hash_diode.startswith('40a75d')
    assert dc.stack[0].hash_weights.startswith('a213c4')
    assert dc.stack.hash_data.startswith('475981')
    assert dc.stack.hash_diode.startswith('40a75d')
    assert dc.stack.hash_weights.startswith('a213c4')


def test_empty_hashes():
    s = Stack()
    assert s.hash_data.startswith('786a02')
    assert s.hash_diode.startswith('786a02')
    assert s.hash_weights.startswith('786a02')
    f = Frame()
    assert f.hash_data.startswith('786a02')
    assert f.hash_diode.startswith('786a02')
    assert f.hash_weights.startswith('786a02')
    s.append(f)
    assert s.hash_data.startswith('786a02')
    assert s.hash_diode.startswith('786a02')
    assert s.hash_weights.startswith('786a02')
    assert s[0].hash_data.startswith('786a02')
    assert s[0].hash_diode.startswith('786a02')
    assert s[0].hash_weights.startswith('786a02')


def test_append():
    stack = Stack()
    for i in range(5):
        f = Frame(diode=np.array((0.5, 1.5)).reshape(1, 2), j_offset=i)
        stack.append(f)
    assert np.allclose(stack[0].diode, (0.5, 1.5))
    f = Frame(diode=np.array((0.5, 1.5)).reshape(2, 1))

    with pytest.raises(ValueError, match='Appended'):
        stack.append(f)
    with pytest.raises(ValueError, match='New'):
        stack[0] = f
    with pytest.raises(ValueError, match='Inserted'):
        stack.insert(0, f)


def test_insert():
    stack = Stack()
    for i in range(5):
        f = Frame(j_offset=i)
        stack.append(f)
    f = Frame(j_offset=5)
    stack.insert(1, f)
    assert len(stack) == 6
    assert stack[1] == f
    assert stack[1].j_offset == 5
    assert stack[5].j_offset == 4


def test_setitem():
    stack = Stack()
    for i in range(5):
        f = Frame(j_offset=i)
        stack.append(f)
    f = Frame(j_offset=5)
    stack[1] = f
    assert len(stack) == 5
    assert stack[1] == f
    assert stack[1].j_offset == 5
    assert stack[4].j_offset == 4


def test_attached():
    stack = Stack()
    for i in range(5):
        f = Frame(j_offset=i)
        stack.append(f)
    other_stack = Stack()
    with pytest.raises(ValueError, match='attached'):
        other_stack.append(f)
    other_stack.append(Frame())

    with pytest.raises(ValueError, match='attached'):
        other_stack[0] = f

    with pytest.raises(ValueError, match='attached'):
        other_stack.insert(0, f)

    del stack[4]
    other_stack.append(f)


def test_size():
    stack = Stack()
    for i in range(5):
        f = Frame(j_offset=i)
        stack.append(f)
    with pytest.raises(IndexError, match='bounds'):
        f = stack[5]
    with pytest.raises(IndexError, match='bounds'):
        f = stack[-6]


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    stack = dc.stack
    s = stack._get_str_representation(5)
    assert s.count('\n') <= 6


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    stack = dc.stack
    s = stack._get_html_representation(5)
    assert s.count('</tr>') <= 6


def test_set_frame_geo():
    f = Frame()
    g = GeometryTuple(rotation=np.ones(3), j_offset=0, k_offset=5)
    f.geometry = g
    assert np.allclose(f.rotation, g.rotation)
    assert np.allclose(f.j_offset, g.j_offset)
    assert np.allclose(f.k_offset, g.k_offset)
