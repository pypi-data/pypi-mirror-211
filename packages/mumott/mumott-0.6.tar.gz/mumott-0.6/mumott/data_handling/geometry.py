from __future__ import annotations
import logging
import tarfile
import tempfile
import json
import os
import codecs
import numpy as np
from typing import List, NamedTuple, Union
from numpy.typing import NDArray
from ..core.hashing import list_to_hash

logger = logging.getLogger(__name__)


class GeometryTuple(NamedTuple):
    """Tuple for passing and returning frame-wise geometry information.
    This is a helper class used by :class:`Geometry`.

    Attributes
    ----------
    rotation
        Rotation matrix.
    j_offset
        Offset to align projection in the direction j.
    k_offset
        Offset to align projection in the direction k.
    """
    rotation: NDArray[np.float64] = np.eye(3, dtype=np.float64)
    j_offset: np.float64 = np.float64(0)
    k_offset: np.float64 = np.float64(0)

    def __hash__(self) -> int:
        to_hash = [self.rotation.ravel(), self.j_offset, self.k_offset]
        return int(list_to_hash(to_hash), 16)

    def __str__(self) -> str:
        wdt = 74
        s = []
        s += ['-' * wdt]
        s += ['GeometryTuple'.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=4, precision=5, linewidth=60, edgeitems=1):
            ss = ', '.join([f'{r}' for r in self.rotation])
            s += ['{:18} : {}'.format('rotation', ss)]
            s += ['{:18} : {}'.format('j_offset', self.j_offset)]
            s += ['{:18} : {}'.format('k_offset', self.k_offset)]
        s += ['-' * wdt]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += ['<h3>GeometryTuple</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th><th>Data</th></tr></thead>']
        s += ['<tbody>']
        with np.printoptions(threshold=4, edgeitems=2, precision=2, linewidth=40):
            s += ['<tr><td style="text-align: left;">Rotation</td>']
            s += [f'<td>{self.rotation.shape}</td><td>{self.rotation}</td></tr>']
            s += ['<tr><td style="text-align: left;">j_offset</td>']
            s += [f'<td>{1}</td><td>{self.j_offset}</td></tr>']
            s += ['<tr><td style="text-align: left;">k_offset</td>']
            s += [f'<td>{1}</td><td>{self.k_offset}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return '\n'.join(s)


class Geometry:
    """ Stores information about the system geometry.
    Instances of this class are used by :class:`DataContainer`
    and :class:`Stack <mumott.data_handling.stack.Stack>` to maintain geometry information.
    They can be stored as a file using the :meth:`write` method.
    This allows one to (re)create a :class:`Geometry` instance from an earlier
    and overwrite the geometry information read by :class:`DataContainer`.
    This is useful, for example, in the context of alignment.

    Parameters
    ----------
    filename
        Name of file from which to read geometry information.
        Defaults to ``None``, in which case the instance is created with
        default parameters.
    """
    def __init__(self, filename: str = None):
        self._rotations = []
        self._j_offsets = []
        self._k_offsets = []
        self.p_direction_0 = np.array([0, 1, 0]).astype(np.float64)
        self.j_direction_0 = np.array([1, 0, 0]).astype(np.float64)
        self.k_direction_0 = np.array([0, 0, 1]).astype(np.float64)
        self.detector_direction_origin = np.array([1, 0, 0]).astype(np.float64)
        self.detector_direction_positive_90 = np.array([0, 0, 1]).astype(np.float64)
        self.projection_shape = np.array([0, 0]).astype(np.int32)
        self.volume_shape = np.array([0, 0, 0]).astype(np.int32)
        self.detector_angles = np.array([]).astype(np.float64)
        if filename is not None:
            self.read(filename)

    def write(self, filename: str) -> None:
        """Method for writing the current state of a :class:`Geometry` instance to file.

        Parameters
        ----------
        filename
            Name of output file.
        """
        to_write = dict(_rotations=self.rotations_as_array.tolist(),
                        _j_offsets=self._j_offsets,
                        _k_offsets=self._k_offsets,
                        p_direction_0=self.p_direction_0.tolist(),
                        j_direction_0=self.j_direction_0.tolist(),
                        k_direction_0=self.k_direction_0.tolist(),
                        detector_direction_origin=self.detector_direction_origin.tolist(),
                        detector_direction_positive_90=self.detector_direction_positive_90.tolist(),
                        projection_shape=self.projection_shape.tolist(),
                        volume_shape=self.volume_shape.tolist(),
                        detector_angles=self.detector_angles.tolist(),
                        checksum=[hash(self)])
        with tarfile.open(name=filename, mode='w') as tar_file:
            for key, item in to_write.items():
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.close()
                with codecs.open(temp_file.name, 'w', encoding='utf-8') as tf:
                    json.dump(item, tf)
                    tf.flush()
                with open(temp_file.name, 'rb') as tt:
                    tar_info = tar_file.gettarinfo(arcname=key, fileobj=tt)
                    tar_file.addfile(tar_info, tt)
                os.remove(temp_file.name)

    def read(self, filename: str) -> None:
        """Method for reading the current state of a :class:`Geometry` instance from file.

        Parameters
        ----------
        filename
            Name of input file.
        """
        to_read = ['_rotations',
                   '_j_offsets',
                   '_k_offsets',
                   'p_direction_0',
                   'j_direction_0',
                   'k_direction_0',
                   'detector_direction_origin',
                   'detector_direction_positive_90',
                   'projection_shape',
                   'volume_shape',
                   'detector_angles',
                   'checksum']
        with tarfile.open(name=filename, mode='r') as tar_file:
            for key in to_read:
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(tar_file.extractfile(key).read())
                temp_file.close()
                with codecs.open(temp_file.name, 'r', encoding='utf-8') as file:
                    text = file.read()
                data_as_list = json.loads(text)
                if key == 'checksum':
                    checksum = data_as_list[0]
                elif key == 'rotations':
                    self._rotations = []
                    for entry in data_as_list:
                        self._rotations.append(entry)
                elif key in ('_j_offsets', '_k_offsets'):
                    setattr(self, key, data_as_list)
                else:
                    setattr(self, key, np.array(data_as_list))
        if checksum != hash(self):
            logger.warning(f'Checksum does not match! Checksum is {checksum},'
                           f' but hash(self) is {hash(self)}. This may be due to'
                           ' version differences, but please proceed with caution!')

    def append(self, value: GeometryTuple) -> None:
        """ Appends frame-wise data handed via a
        :class:`GeometryTuple <mumott.data_handling.geometry.GeometryTuple>`. """
        self._rotations.append(value.rotation)
        self._j_offsets.append(value.j_offset)
        self._k_offsets.append(value.k_offset)

    def insert(self, key: int, value: GeometryTuple) -> None:
        """ Inserts frame-wise data handed via a
        :class:`GeometryTuple <mumott.data_handling.geometry.GeometryTuple>`. """
        self._rotations.insert(key, value.rotation)
        self._j_offsets.insert(key, value.j_offset)
        self._k_offsets.insert(key, value.k_offset)

    def __setitem__(self, key: int, value: GeometryTuple) -> None:
        """ Sets frame-wise data handed via a :class:`GeometryTuple`."""
        self._rotations[key] = value.rotation
        self._j_offsets[key] = value.j_offset
        self._k_offsets[key] = value.k_offset

    def __getitem__(self, key: int) -> GeometryTuple:
        """ Returns frame-wise data handed via a :class:`GeometryTuple`."""
        return GeometryTuple(rotation=self._rotations[key],
                             j_offset=self._j_offsets[key],
                             k_offset=self._k_offsets[key])

    def __delitem__(self, key: int) -> None:
        del self._rotations[key]
        del self._j_offsets[key]
        del self._k_offsets[key]

    @property
    def rotations_as_array(self) -> NDArray:
        """ Rotation matrices corresponding to each frame of data as an array."""
        if len(self) == 0:
            return np.array([])
        return np.stack([r for r in self._rotations], axis=0)

    @property
    def rotations(self) -> List[NDArray[np.float64]]:
        """ Rotation matrices corresponding to each frame of data."""
        return self._rotations

    @rotations.setter
    def rotations(self, value: Union[list, NDArray]) -> None:
        self._rotations = [r for r in value]

    @property
    def j_offsets(self) -> List[np.float64]:
        """Offsets to align projection in the direction j as an array."""
        return self._j_offsets

    @property
    def j_offsets_as_array(self) -> NDArray:
        """Offsets to align projection in the direction j as an array."""
        if len(self._j_offsets) == 0:
            return np.array([])
        return np.stack([j for j in self._j_offsets], axis=0)

    @j_offsets.setter
    def j_offsets(self, value: Union[List[np.float64], NDArray]) -> None:
        self._j_offsets = [j for j in value]

    @property
    def k_offsets(self) -> List[np.float64]:
        """Offsets to align projection in the direction k."""
        return self._k_offsets

    @property
    def k_offsets_as_array(self) -> NDArray:
        """Offsets to align projection in the direction k as an array."""
        if len(self._k_offsets) == 0:
            return np.array([])
        return np.stack([k for k in self._k_offsets], axis=0)

    @property
    def hash_rotations(self) -> str:
        """ A sha1 hash of :attr:`rotations_as_array`. """
        return list_to_hash([self.rotations_as_array])

    @property
    def hash_j_offsets(self) -> str:
        """ A sha1 hash of :attr:`j_offsets_as_array`. """
        return list_to_hash([self.j_offsets_as_array])

    @property
    def hash_k_offsets(self) -> str:
        """ A sha1 hash of :attr:`k_offsets_as_array`. """
        return list_to_hash([self.k_offsets_as_array])

    @k_offsets.setter
    def k_offsets(self, value: Union[List[np.float64], NDArray]) -> None:
        self._k_offsets = [k for k in value]

    def __hash__(self) -> int:
        to_hash = [self.rotations_as_array,
                   self.j_offsets_as_array,
                   self.k_offsets_as_array,
                   self.p_direction_0, self.j_direction_0, self.k_direction_0,
                   self.detector_direction_origin, self.detector_direction_positive_90,
                   self.projection_shape, self.volume_shape, self.detector_angles]
        return int(list_to_hash(to_hash), 16)

    def __len__(self) -> int:
        return len(self._rotations)

    def _get_str_representation(self, max_lines: int = 25) -> str:
        """ Retrieves a string representation of the object with specified
        maximum number of lines.

        Parameters
        ----------
        max_lines
            The maximum number of lines to return.
        """
        wdt = 74
        s = []
        s += ['-' * wdt]
        s += ['Geometry'.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=3, edgeitems=1, precision=3, linewidth=60):
            s += ['{:18} : {}'.format('hash_rotations',
                  self.hash_rotations[:6])]
            s += ['{:18} : {}'.format('hash_j_offsets',
                  self.hash_j_offsets[:6])]
            s += ['{:18} : {}'.format('hash_k_offsets',
                  self.hash_k_offsets[:6])]
            s += ['{:18} : {}'.format('p_direction_0', self.p_direction_0)]
            s += ['{:18} : {}'.format('j_direction_0', self.j_direction_0)]
            s += ['{:18} : {}'.format('k_direction_0', self.k_direction_0)]
            s += ['{:18} : {}'.format('detector_direction_origin', self.detector_direction_origin)]
            s += ['{:18} : {}'.format('detector_direction_positive_90', self.detector_direction_positive_90)]
            s += ['{:18} : {}'.format('projection_shape', self.projection_shape)]
            s += ['{:18} : {}'.format('volume_shape', self.volume_shape)]
            s += ['{:18} : {}'.format('detector_angles', self.detector_angles)]
        s += ['-' * wdt]
        truncated_s = []
        leave_loop = False
        while not leave_loop:
            line = s.pop(0).split('\n')
            for split_line in line:
                if split_line != '':
                    truncated_s += [split_line]
                if len(truncated_s) > max_lines - 2:
                    if split_line != '...':
                        truncated_s += ['...']
                    if split_line != ('=' * wdt):
                        truncated_s += ['=' * wdt]
                    leave_loop = True
                    break
            if len(s) == 0:
                leave_loop = True
        return '\n'.join(truncated_s)

    def __str__(self) -> str:
        return self._get_str_representation()

    def _get_html_representation(self, max_lines: int = 25) -> str:
        """ Retrieves an html representation of the object with specified
        maximum number of lines.

        Parameters
        ----------
        max_lines
            The maximum number of lines to return.
        """
        s = []
        s += ['<h3>Geometry</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th><th>Data</th></tr></thead>']
        s += ['<tbody>']
        with np.printoptions(threshold=3, edgeitems=1, precision=2, linewidth=40):
            s += ['<tr><td style="text-align: left;">rotations</td>']
            s += [f'<td>{len(self.rotations)}</td>'
                  f'<td>{self.hash_rotations[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">j_offsets</td>']
            s += [f'<td>{len(self.j_offsets)}</td>'
                  f'<td>{self.hash_j_offsets[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">k_offsets</td>']
            s += [f'<td>{len(self.k_offsets)}</td>'
                  f'<td>{self.hash_k_offsets[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">p_direction_0</td>']
            s += [f'<td>{len(self.p_direction_0)}</td><td>{self.p_direction_0}</td></tr>']
            s += ['<tr><td style="text-align: left;">j_direction_0</td>']
            s += [f'<td>{len(self.j_direction_0)}</td><td>{self.j_direction_0}</td></tr>']
            s += ['<tr><td style="text-align: left;">k_direction_0</td>']
            s += [f'<td>{len(self.k_direction_0)}</td><td>{self.k_direction_0}</td></tr>']
            s += ['<tr><td style="text-align: left;">detector_direction_origin</td>']
            s += [f'<td>{len(self.detector_direction_origin)}</td>'
                  f'<td>{self.detector_direction_origin}</td></tr>']
            s += ['<tr><td style="text-align: left;">detector_direction_positive_90</td>']
            s += [f'<td>{len(self.detector_direction_positive_90)}</td>'
                  f'<td>{self.detector_direction_positive_90}</td></tr>']
            s += ['<tr><td style="text-align: left;">projection_shape</td>']
            s += [f'<td>{len(self.projection_shape)}</td><td>{self.projection_shape}</td></tr>']
            s += ['<tr><td style="text-align: left;">volume_shape</td>']
            s += [f'<td>{len(self.volume_shape)}</td><td>{self.volume_shape}</td></tr>']
            s += ['<tr><td style="text-align: left;">detector_angles</td>']
            s += [f'<td>{len(self.detector_angles)}</td><td>{self.detector_angles}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        truncated_s = []
        line_count = 0
        leave_loop = False
        while not leave_loop:
            line = s.pop(0).split('\n')
            for split_line in line:
                truncated_s += [split_line]
                if '</tr>' in split_line:
                    line_count += 1
                    # Catch if last line had ellipses
                    last_tr = split_line
                if line_count > max_lines - 1:
                    if last_tr != '<tr><td style="text-align: left;">...</td></tr>':
                        truncated_s += ['<tr><td style="text-align: left;">...</td></tr>']
                    truncated_s += ['</tbody>']
                    truncated_s += ['</table>']
                    leave_loop = True
                    break
            if len(s) == 0:
                leave_loop = True
        return '\n'.join(truncated_s)

    def _repr_html_(self) -> str:
        return self._get_html_representation()
