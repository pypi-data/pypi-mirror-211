import pytest  # noqa:F401
import numpy as np

from numba import cuda

from mumott.data_handling import DataContainer
from mumott.core import john_transform_cuda, john_transform_adjoint_cuda

dc = DataContainer('tests/test_half_circle.h5')
gm = dc.geometry
fields = [np.arange(192, dtype=np.float32).reshape(4, 4, 4, 3)]
outs = [np.array([[[[72.,  76,  80],
                  [84,  88,  92],
                  [96, 100, 104],
                  [108, 112, 116]],
                 [[264, 268, 272],
                  [276, 280, 284],
                  [288, 292, 296],
                  [300, 304, 308]],
                 [[456, 460, 464],
                  [468, 472, 476],
                  [480, 484, 488],
                  [492, 496, 500]],
                 [[648, 652, 656],
                  [660, 664, 668],
                  [672, 676, 680],
                  [684, 688, 692]]]], dtype=np.float32)]

outs90 = [np.array([[[[288, 292, 296],
                      [300, 304, 308],
                      [312, 316, 320],
                      [324, 328, 332]],
                     [[336, 340, 344],
                      [348, 352, 356],
                      [360, 364, 368],
                      [372, 376, 380]],
                     [[384, 388, 392],
                      [396, 400, 404],
                      [408, 412, 416],
                      [420, 424, 428]],
                     [[432, 436, 440],
                      [444, 448, 452],
                      [456, 460, 464],
                      [468, 472, 476]]]], dtype=np.float32)]

out_fields = [np.arange(48)]
projs = [np.arange(48, dtype=np.float32).reshape(1, 4, 4, 3)]


@pytest.mark.parametrize('field,out', [t for t in zip(fields, outs)])
def test_john_transform_cuda(field, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    projections = np.zeros_like(out).astype(np.float32)
    john_transform_cuda(field, projections, vector_p, vector_j, vector_k, offsets_j, offsets_k)
    print(projections)
    assert np.allclose(projections, out)


@pytest.mark.parametrize('field,out', [t for t in zip(fields, outs90)])
def test_john_transform_cuda90(field, out):
    vector_p = np.array([[1., 0., 0.]])
    vector_j = np.array([[0., 1., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    projections = np.zeros_like(out).astype(np.float32)
    john_transform_cuda(field, projections, vector_p, vector_j, vector_k, offsets_j, offsets_k)
    print(projections)
    assert np.allclose(projections, out)


@pytest.mark.parametrize('proj,out', [t for t in zip(projs, out_fields)])
def test_john_transform_adjoint_cuda(proj, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    field = np.zeros((4, 4, 4, 3,), dtype=np.float32)
    john_transform_adjoint_cuda(field, proj, vector_p, vector_j, vector_k, offsets_j, offsets_k)
    print(field)
    assert np.allclose(field[:, 0].ravel(), out)


@pytest.mark.parametrize('field,out', [t for t in zip(fields, outs)])
def test_device_john_transform_cuda(field, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    projections = cuda.to_device(np.zeros_like(out).astype(np.float32))
    john_transform_cuda(cuda.to_device(field), projections,
                        vector_p, vector_j, vector_k, offsets_j, offsets_k)
    assert np.allclose(projections.copy_to_host(), out)


@pytest.mark.parametrize('proj,out', [t for t in zip(projs, out_fields)])
def test_device_john_transform_adjoint_cuda(proj, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    field = cuda.to_device(np.zeros((4, 4, 4, 3,), dtype=np.float32))
    john_transform_adjoint_cuda(field, cuda.to_device(proj),
                                vector_p, vector_j, vector_k, offsets_j, offsets_k)
    assert np.allclose(field.copy_to_host()[:, 0].ravel(), out)
