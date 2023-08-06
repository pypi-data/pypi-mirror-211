""" Container for class Stack. """
import numpy as np
from numpy.typing import NDArray
from .geometry import Geometry, GeometryTuple
from ..core.hashing import list_to_hash


class Frame:
    """Instances of this class contain data and metadata from a single measurement.
    Typically they are appended to a :class:`Stack <mumott.data_handling.stack.Stack>` object.

    Parameters
    ----------
    data
        Data from measurement, structured into 3 dimensions representing
        the two scanning directions and the detector angle.
    diode
        Diode or transmission data from measurement, structured into
        2 dimensions representing the two scanning directions.
    weights
        Weights or masking information, represented as a number
        between ``0`` and ``1``. ``0`` means mask, ``1`` means
        do not mask. Structured the same way as :attr:`data`.
    rotation
        3-by-3 rotation matrix, representing the rotation of the sample in the
        laboratory coordinate system.
    j_offset
        The offset needed to align the projection in the j-direction.
    k_offset
        The offset needed to align the projection in the k-direction.
    """
    def __init__(self,
                 data: NDArray[np.float64] = None,
                 diode: NDArray[np.float64] = None,
                 weights: NDArray[np.float64] = None,
                 rotation: NDArray[np.float64] = np.eye(3, dtype=np.float64),
                 j_offset: np.float64 = np.float64(0),
                 k_offset: np.float64 = np.float64(0)):
        self._key = None
        self._stack = None
        self.data = data
        self.diode = diode
        self.weights = weights
        self.j_offset = j_offset
        self.k_offset = k_offset
        self.rotation = rotation

    @property
    def j_offset(self) -> np.float64:
        """ The offset needed to align the projection in the j-direction."""
        if self._stack is None:
            return self._j_offset
        else:
            k = self._stack.index_by_key(self._key)
            return self._stack.geometry.j_offsets[k]

    @j_offset.setter
    def j_offset(self, value) -> None:
        self._j_offset = value
        if self._stack is not None:
            k = self._stack.index_by_key(self._key)
            self._stack.geometry.j_offsets[k] = value

    @property
    def k_offset(self) -> np.float64:
        """ The offset needed to align the projection in the k-direction."""
        if self._stack is None:
            return self._k_offset
        else:
            k = self._stack.index_by_key(self._key)
            return self._stack.geometry.k_offsets[k]

    @k_offset.setter
    def k_offset(self, value) -> None:
        self._k_offset = value
        if self._stack is not None:
            k = self._stack.index_by_key(self._key)
            self._stack.geometry.k_offsets[k] = value

    @property
    def rotation(self) -> NDArray[np.float64]:
        """ 3-by-3 rotation matrix, representing the rotation of the sample in the
        laboratory coordinate system. """
        if self._stack is None:
            return self._rotation
        else:
            k = self._stack.index_by_key(self._key)
            return self._stack.geometry.rotations[k]

    @rotation.setter
    def rotation(self, value) -> None:
        self._rotation = value
        if self._stack is not None:
            k = self._stack.index_by_key(self._key)
            self._stack.geometry.rotations[k] = value

    @property
    def data(self) -> NDArray:
        """ Scattering data, structured ``(j, k, w)``, where ``j`` is the pixel in the j-direction,
        ``k`` is the pixel in the k-direction, and ``w`` is the detector segment.
        Before the reconstruction, the data should be normalized by the diode.
        This may already have been done prior to loading the data.
        """
        return np.array([]).reshape(0, 0) if self._data is None else self._data

    @data.setter
    def data(self, val) -> None:
        self._data = val

    @property
    def diode(self) -> NDArray[np.float64]:
        """ The diode readout, used to normalize the data. Can be blank if data is already normalized.
        """
        return np.array([]).reshape(0, 0) if self._diode is None else self._diode

    @diode.setter
    def diode(self, val) -> None:
        self._diode = val

    @property
    def weights(self) -> NDArray:
        """ Weights to be applied multiplicatively during optimization. A value of ``0``
        means mask, a value of ``1`` means no weighting, and other values means weighting
        each data point either less (``weights < 1``) or more (``weights > 1``) than a weight of ``1``.
        """
        return np.array([]).reshape(0, 0) if self._weights is None else self._weights

    @weights.setter
    def weights(self, val) -> None:
        self._weights = val

    @property
    def attached(self):
        """ Returns true if frame is attached to a :class:`Stack <Stack>` object. """
        return self._stack is not None

    def attach_to_stack(self, stack, index):
        """ Used to attach the frame to a stack.
        *This method should not be called by users.*
        """
        if self.attached:
            raise ValueError('This frame is already attached to a stack')
        self._stack = stack
        self._key = index

    @property
    def geometry(self) -> GeometryTuple:
        """ Returns geometry information as a named tuple. """
        return GeometryTuple(rotation=self.rotation, j_offset=self.j_offset, k_offset=self.k_offset)

    @geometry.setter
    def geometry(self, value: GeometryTuple) -> None:
        self.rotation = value.rotation
        self.j_offset = value.j_offset
        self.k_offset = value.k_offset

    def detach_from_stack(self):
        """ Used to detach the frame from a stack.
        *This method should not be called by users.*
        """
        k = self._stack.index_by_key(self._key)
        g = self._stack.geometry[k]
        self._rotation = g.rotation
        self._j_offset = g.j_offset
        self._k_offset = g.k_offset
        self._stack = None
        self._key = None

    @property
    def hash_data(self) -> str:
        """ A hash of :attr:`data`."""
        # np.array wrapper in case data is None
        return list_to_hash([np.array(self.data)])

    @property
    def hash_diode(self) -> str:
        """ A sha1 hash of :attr:`diode`."""
        return list_to_hash([np.array(self.diode)])

    @property
    def hash_weights(self) -> str:
        """ A sha1 hash of :attr:`weights`."""
        return list_to_hash([np.array(self.weights)])

    def __str__(self) -> str:
        wdt = 74
        s = []
        s += ['-' * wdt]
        s += ['Frame'.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=4, precision=5, linewidth=60, edgeitems=2):
            s += ['{:18} : {}'.format('hash_data', self.hash_data[:6])]
            s += ['{:18} : {}'.format('hash_diode', self.hash_diode[:6])]
            s += ['{:18} : {}'.format('hash_weights', self.hash_weights[:6])]
            ss = ', '.join([f'{r}' for r in self.rotation])
            s += ['{:18} : {}'.format('rotation', ss)]
            s += ['{:18} : {}'.format('j_offset', self.j_offset)]
            s += ['{:18} : {}'.format('k_offset', self.k_offset)]
        s += ['-' * wdt]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += ['<h3>Frame</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th><th>Data</th></tr></thead>']
        s += ['<tbody>']
        with np.printoptions(threshold=4, precision=5, linewidth=40, edgeitems=2):
            s += ['<tr><td style="text-align: left;">data</td>']
            s += [f'<td>{self.data.shape}</td><td>{self.hash_data[:6]} (hash)</td></tr>']
            s += [f'<tr><td style="text-align: left;">diode</td>'
                  f'<td>{self.diode.shape}</td>']
            s += [f'<td>{self.hash_diode[:6]} (hash)</td></tr>']
            s += [f'<tr><td style="text-align: left;">weights</td>'
                  f'<td>{self.weights.shape}</td>']
            s += [f'<td>{self.hash_weights[:6]} (hash)</td></tr>']
            s += [f'<tr><td style="text-align: left;">rotation</td><td>{self.rotation.shape}</td>']
            s += [f'<td>{self.rotation}</td></tr>']
            s += ['<tr><td style="text-align: left;">j_offset</td><td>1</td>']
            s += [f'<td>{self.j_offset}</td></tr>']
            s += ['<tr><td style="text-align: left;">k_offset</td><td>1</td>']
            s += [f'<td>{self.k_offset}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return '\n'.join(s)


class Stack:
    """Instances of this class contain data, geometry and other pertinent information
    for a series of measurements.
    The individual measurements are stored as :class:`Frame <mumott.data_handling.stack.Frame>` objects.
    The latter are accessible via list-like operations, which enables, for example, iteration over
    measurements but also retrieval of individual measurements by index, in-place modification or deletion.

    The geometry information (i.e., rotations and offsets for each frame)
    is accessible via the :attr:`geometry` attribute.
    Data, diode readouts, and weights can be retrieved as contiguous arrays
    via the properties :attr:`data`, :attr:`diode`, and :attr:`weights`, respectively.

    Example
    -------
    The following code snippet illustrates how individual measurements can be accessed via list operations.
    For demonstration, here, we use default ("empty") frames.
    In practice the individual measurements are read from a data file via the
    :class:`DataContainer <mumott.data_handling.DataContainer>` class, which makes
    them available via the :attr:`DataContainer.stack <mumott.data_handling.DataContainer.stack>` attribute.

    First we create an empty stack

    >>> from mumott.data_handling.stack import Frame, Stack
    >>> stack = Stack()

    Next we create a frame and attach it to the stack.
    In order to be able to distinguish this frame during this example,
    we assign it a :attr:`Frame.j_offset` of ``0.5``.

    >>> frame = Frame(j_offset=0.5)
    >>> stack.append(frame)

    The geometry information can now be accessed via the stack in several different but equivalent ways,
    namely via the original frame object,

    >>> print(frame.j_offset)

    via indexing the stack

    >>> print(stack[0].geometry.j_offset)

    or by indexing the respective geometry property of the stack itself.

    >>> print(stack.geometry.j_offsets[0])

    We can modify the geometry parameters via any of these properties with identical outcome.
    For example,

    >>> stack[0].j_offset = -0.2
    >>> print(frame.j_offset, stack[0].geometry.j_offset, stack.geometry.j_offsets[0])
    -0.2 -0.2 -0.2

    Next consider a situation where several frames are included in the stack.

    >>> stack.append(Frame(j_offset=0.1))
    >>> stack.append(Frame(j_offset=-0.34))
    >>> stack.append(Frame(j_offset=0.23))
    >>> stack.append(Frame(j_offset=0.78))
    >>> print(stack.geometry.j_offsets)
    [-0.2, 0.1, -0.34, 0.23, 0.78]

    The summary of the stack includes hashes for the data, the diode readout, and the weights.
    This allows one to get a quick indication for whether the content of these fields changes.

    >>> print(stack)
    --------------------------------------------------------------------------
                                      Stack
    --------------------------------------------------------------------------
    hash_data          : ...

    We could, for example, decide to remove an invididual frames as we might
    have realized that the data from that measurement was corrupted.

    >>> del stack[1]
    >>> print(stack)
    --------------------------------------------------------------------------
                                      Stack
    --------------------------------------------------------------------------
    hash_data          : ...

    From the output it is readily apparent that the content of the data field
    has changed as a result of this operation.

    Finally, note that we can also loop over the stack, for example, to print the frames.

    >>> for frame in stack:
    >>>     print(frame)
    ...
    """

    def __init__(self) -> None:
        self._frames = []
        self._keys = []
        self._geometry = Geometry()

    def __delitem__(self, k: int) -> None:
        """ Removes a frame from the stack. """
        if abs(k) > len(self) - int(k >= 0):
            raise IndexError(f'Index {k} is out of bounds for Stack of length {len(self)}.')
        self._frames[k].detach_from_stack()
        del self._frames[k]
        del self._geometry[k]
        del self._keys[k]

    def append(self, frame: Frame) -> None:
        """
        Appends a measurement in the form of a :class:`Frame <mumott.data_handling.stack.Frame>` object.
        Once a frame is attached to a stack, the geometry information of the frame will be synchronized
        with the geometry information of the stack (see :attr:`geometry`).

        Parameters
        ----------
        frame
            :class:`Frame <mumott.data_handling.stack.Frame>` object to be appended.
        """
        if frame.attached:
            raise ValueError('The frame is already attached to a stack')
        assert len(self._frames) == len(self._geometry)
        if len(self) == 0:
            self._geometry.projection_shape = np.array(frame.diode.shape)
        elif not np.allclose(self.diode.shape[1:], frame.diode.shape):
            raise ValueError('Appended frame diode must have the same shape as other frames,'
                             f' but its shape is {frame.diode.shape} while other frames'
                             f' have shape {self.diode.shape[1:]}.')
        self._frames.append(frame)
        self._geometry.append(GeometryTuple(rotation=frame.rotation,
                                            j_offset=frame.j_offset,
                                            k_offset=frame.k_offset))

        frame_key = hash(frame)
        self._keys.append(frame_key)
        frame.attach_to_stack(self, frame_key)

    def __setitem__(self, k: int, frame: Frame) -> None:
        """
        This allows each frame of the stack to be safely modified.
        """
        assert len(self._frames) == len(self._geometry)
        if abs(k) > len(self) - int(k >= 0):
            raise IndexError(f'Index {k} is out of bounds for Stack of length {len(self)}.')

        if frame.attached:
            raise ValueError('The frame is already attached to a stack')
        if not np.allclose(self.diode.shape[1:], frame.diode.shape):
            raise ValueError('New frame diode must have the same shape as other frames,'
                             f' but its shape is {frame.diode.shape} while other frames'
                             f' have shape {self.diode.shape[1:]}.')

        # detach and delete previous frame
        del self[k]

        # attach new frame
        self._frames.insert(k, frame)
        self._geometry.insert(k, GeometryTuple(rotation=frame.rotation,
                                               j_offset=frame.j_offset,
                                               k_offset=frame.k_offset))

        frame_key = hash(frame)
        self._keys.insert(k, frame_key)
        frame.attach_to_stack(self, frame_key)

    def insert(self, k: int, frame: Frame) -> None:
        """ Inserts a frame at a particular index, increasing the indices
        of all subsequent frames by 1. """
        assert len(self._frames) == len(self._geometry)
        if abs(k) > len(self) - int(k >= 0):
            raise IndexError(f'Index {k} is out of bounds for stack of length {len(self)}.')

        if frame.attached:
            raise ValueError('The frame is already attached to a stack.')
        if not np.allclose(self.diode.shape[1:], frame.diode.shape):
            raise ValueError('Inserted frame diode must have the same shape as other frames,'
                             f' but its shape is {frame.diode.shape} while other frames'
                             f' have shape {self.diode.shape[1:]}.')

        self._frames.insert(k, frame)
        self._geometry.insert(k, GeometryTuple(rotation=frame.rotation,
                                               j_offset=frame.j_offset,
                                               k_offset=frame.k_offset))
        self._geometry.projection_shape = np.array(frame.diode.shape)
        frame_key = hash(frame)
        self._keys.insert(k, frame_key)
        frame.attach_to_stack(self, frame_key)

    def __getitem__(self, k: int) -> Frame:
        """
        This allows indexing of and iteration over the stack.
        """
        assert len(self._frames) == len(self._geometry)
        if abs(k) > len(self) - round(float(k >= 0)):
            raise IndexError(f'Index {k} is out of bounds for Stack of length {len(self)}.')
        return self._frames[k]

    def __len__(self) -> int:
        return len(self._frames)

    @property
    def data(self) -> NDArray:
        """ Scattering data, structured ``(n, j, k, w)``, where ``n`` is the projection number,
        ``j`` is the pixel in the j-direction, ``k`` is the pixel in the k-direction,
        and ``w`` is the detector segment. Before the reconstruction, this should
        be normalized by the diode. This may already have been done prior to loading the data.
        """
        if len(self) == 0:
            return np.array([]).reshape(0, 0, 0)
        return np.stack([f.data for f in self._frames], axis=0)

    @property
    def diode(self) -> NDArray:
        """ The diode readout, used to normalize the data. Can be blank if data is already normalized.
        The diode value should not be normalized per frame, i.e., it is distinct from the
        transmission value used in standard tomography."""
        if len(self) == 0:
            return np.array([]).reshape(0, 0, 0)
        return np.stack([f.diode for f in self._frames], axis=0)

    @diode.setter
    def diode(self, val) -> None:
        assert len(self) == len(val)
        for i, frame in enumerate(self._frames):
            frame.diode[...] = val[i]

    @property
    def weights(self) -> NDArray:
        """ Weights applied multiplicatively during optimization. A value of ``0``
        means mask, a value of ``1`` means no weighting, and other values means weighting
        each data point either less (``weights < 1``) or more (``weights > 1``) than a weight of ``1``.
        """
        if len(self) == 0:
            return np.array([]).reshape(0, 0, 0)
        return np.stack([f.weights for f in self._frames], axis=0)

    @weights.setter
    def weights(self, val) -> None:
        assert len(self) == len(val)
        for i, frame in enumerate(self._frames):
            frame.weights[...] = val[i]

    def _get_str_representation(self, max_lines: int = 25) -> str:
        """ Retrieves a string representation of the object with the specified
        maximum number of lines.

        Parameters
        ----------
        max_lines
            The maximum number of lines to return.
        """
        s = []
        wdt = 74
        s = []
        s += ['-' * wdt]
        s += ['Stack'.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=3, edgeitems=1, precision=3, linewidth=60):
            s += ['{:18} : {}'.format('hash_data', self.hash_data[:6])]
            s += ['{:18} : {}'.format('hash_diode', self.hash_diode[:6])]
            s += ['{:18} : {}'.format('hash_weights', self.hash_weights[:6])]
            s += ['{:18} : {}'.format('Number of frames', len(self))]
            s += ['{:18} : {}'.format('Number of pixels j', self.diode.shape[1])]
            s += ['{:18} : {}'.format('Number of pixels k', self.diode.shape[2])]
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
        truncated_s += ['-' * wdt]
        return '\n'.join(truncated_s)

    def __str__(self) -> str:
        return self._get_str_representation()

    @property
    def hash_data(self) -> str:
        """ A hash of :attr:`data`."""
        # np.array wrapper in case data is None
        return list_to_hash([np.array(self.data)])

    @property
    def hash_diode(self) -> str:
        """ A sha1 hash of :attr:`diode`."""
        return list_to_hash([np.array(self.diode)])

    @property
    def hash_weights(self) -> str:
        """ A sha1 hash of :attr:`weights`."""
        return list_to_hash([np.array(self.weights)])

    def _get_html_representation(self, max_lines: int = 25) -> str:
        """ Retrieves an html representation of the object with the specified
        maximum number of lines.

        Parameters
        ----------
        max_lines
            The maximum number of lines to return.
        """
        s = []
        s += ['<h3>Stack</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th><th>Data</th></tr></thead>']
        s += ['<tbody>']
        with np.printoptions(threshold=3, edgeitems=1, precision=2, linewidth=40):
            s += ['<tr><td style="text-align: left;">data</td>']
            s += [f'<td>{self.data.shape}</td><td>{self.hash_data[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">diode</td>']
            s += [f'<td>{self.diode.shape}</td><td>{self.hash_diode[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">weights</td>']
            s += [f'<td>{self.weights.shape}</td><td>{self.hash_weights[:6]} (hash)</td></tr>']
            s += ['<tr><td style="text-align: left;">Number of pixels j</td>']
            s += ['<td>1</td>']
            s += [f'<td>{self.diode.shape[1]}</td></tr>']
            s += ['<tr><td style="text-align: left;">Number of pixels k</td>']
            s += ['<td>1</td>']
            s += [f'<td>{self.diode.shape[2]}</td></tr>']
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

    @property
    def geometry(self) -> Geometry:
        """ Contains geometry information for each frame as well
        as information about the geometry of the whole system. """
        return self._geometry

    def index_by_key(self, key):
        """ Returns an index from a key. """
        return self._keys.index(key)
