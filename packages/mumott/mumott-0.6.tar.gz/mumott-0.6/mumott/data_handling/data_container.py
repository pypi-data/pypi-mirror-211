import h5py as h5
import logging
import numpy as np
from numpy.typing import NDArray
from scipy.io import loadmat
from scipy.spatial.transform import Rotation
from .geometry import Geometry
from .stack import Stack, Frame

logger = logging.getLogger(__name__)


class DataContainer:

    """
    Instances of this class represent data read from an input file in a format suitable for further analysis.
    The two core components are the :attr:`geometry` and the :attr:`stack`.
    The latter comprises a list of :class:`Frame <mumott.data_handling.stack.Frame>` instances,
    each of which corresponds to a single measurement.

    By default all data is read, which can be rather time consuming and unnecessary in some cases,
    e.g., when aligning data.
    In those cases, one can skip loading the actual measurements by setting :attr:`skip_data` to ``True``.
    The geometry information and supplementary information such as the diode data will still be read.

    Example
    -------
    The following code snippet illustrates the basic use of the :class:`DataContainer` class.

    First we create a :class:`DataContainer` instance, providing the path to the data file to be read.

    >>> from mumott.data_handling import DataContainer
    >>> dc = DataContainer('tests/test_full_circle.h5')

    One can then print a short summary of the content of the :class:`DataContainer` instance.

    >>> print(dc)
    ==========================================================================
                                  DataContainer
    --------------------------------------------------------------------------
    Corrected for transmission : False
    ...

    To access individual measurements we can use the :attr:`stack` attribute.
    The latter behaves like a list, where the elements of the list are
    :class:`Frame <mumott.data_handling.stack.Frame>` objects,
    each of which represents an individual measurement.
    We can print a summary of the content of the first frame.

    >>> print(dc.stack[0])
    --------------------------------------------------------------------------
                                      Frame
    --------------------------------------------------------------------------
    hash_data          : 475981
    hash_diode         : 40a75d
    hash_weights       : a213c4
    rotation           : [1. 0. 0.], [0. 1. 0.], [0. 0. 1.]
    j_offset           : -0.01
    k_offset           : 5.0
    --------------------------------------------------------------------------

    Parameters
    ----------
    data_path : str
        Path of the data file relative to the directory of execution.
    data_type : str, optional
        The type (or format) of the data file. Supported values are
        ``h5`` (default) for hdf5 format and ``mat`` for cSAXS Matlab format.
    skip_data : bool, optional
        If ``True``, will skip data from individual measurements when loading the file.
        This will result in a functioning :attr:`geometry` instance as well as
        :attr:`diode` and :attr:`weights` entries in the data stack, but
        :attr:`data` will be empty.
    """
    def __init__(self,
                 data_path: str,
                 data_type: str = 'h5',
                 skip_data: bool = False):
        self._correct_for_transmission_called = False
        self._stack = Stack()
        self._geometry_dictionary = dict()
        self._skip_data = skip_data
        if data_type == 'mat':
            self._matlab_to_stack(data_path)
        elif data_type == 'h5':
            self._h5_to_stack(data_path)
        else:
            raise ValueError(f'Unknown data_type: {data_type} for'
                             ' load_only_geometry=False.')

    def _h5_to_stack(self, file_path: str):
        """
        Internal method for loading data from hdf5 file.
        """
        h5_data = h5.File(file_path, 'r')
        projections = h5_data['projections']
        number_of_projections = len(projections)
        max_shape = (0, 0)
        for i in range(number_of_projections):
            p = projections[f'{i}']
            if 'diode' in p:
                max_shape = np.max((max_shape, p['diode'].shape), axis=0)
        for i in range(number_of_projections):
            p = projections[f'{i}']
            if 'diode' in p:
                diode = np.ascontiguousarray(np.copy(p['diode']).astype(np.float64))
                pad_sequence = np.array(((0, max_shape[0] - diode.shape[0]),
                                         (0, max_shape[1] - diode.shape[1]),
                                         (0, 0)))
                diode = np.pad(diode, pad_sequence[:-1])
            elif 'data' in p:
                diode = None
                pad_sequence = np.array(((0, max_shape[0] - p['data'].shape[0]),
                                         (0, max_shape[1] - p['data'].shape[1]),
                                         (0, 0)))
            else:
                pad_sequence = np.zeros((3, 2))
            if not self._skip_data:
                data = np.ascontiguousarray(np.copy(p['data']).astype(np.float64))
                data = np.pad(data, pad_sequence)
                if 'weights' in p:
                    weights = np.ascontiguousarray(
                        np.copy(p['weights']).astype(np.float64))[:, :, np.newaxis] * \
                        np.ones((1, 1, data.shape[-1])).astype(np.float64)
                else:
                    weights = np.ones_like(data)
            else:
                data = None
                if 'weights' in p:
                    weights = np.ascontiguousarray(np.copy(p['weights']).astype(np.float64))
                    weights = np.pad(weights, pad_sequence[:weights.ndim])
                else:
                    if diode is None:
                        weights = None
                    else:
                        weights = np.ones_like(diode)
                        weights = np.pad(weights, pad_sequence[:weights.ndim])
            # Look for rotation information and load if available
            if 'rot_mat' in p:
                rotation = p['rot_mat'][...]
                if i == 0:
                    logger.info('Rotation matrices were loaded from the input file.')
            elif 'rotations' in p and 'tilts' in p:
                if 'inner_axis' in p and 'outer_axis' in p:
                    R_rot = Rotation.from_vector(p['rotations'] * p['inner_axis']).as_matrix()
                    R_tilt = Rotation.from_vector(p['tilts'] * p['outer_axis']).as_matrix()
                    if i == 0:
                        logger.info('Rotation matrices were generated from rotation and tilt angles,'
                                    ' along with inner and outer rotation axis vectors.'
                                    ' Rotation and tilt angles assumed to be in radians.')
                else:
                    R_rot = self._Rz(-p['rotations'][0])
                    R_tilt = self._Rx(p['tilts'][0])
                    if i == 0:
                        logger.info('Rotation matrices were generated from rotation and tilt angles.'
                                    ' Rotations were assumed to be about the z-axis and tilts about x-axis'
                                    ' with angles assumed to be in radians.')
                rotation = R_tilt @ R_rot
            else:
                rotation = np.eye(3)
                if i == 0:
                    logger.info('No rotation information found.')
            j_offset = p['offset_j'][0]
            k_offset = p['offset_k'][0]
            j_offset -= pad_sequence[0, 1] * 0.5
            k_offset -= pad_sequence[1, 1] * 0.5
            frame = Frame(data=data,
                          diode=diode,
                          weights=weights,
                          rotation=rotation,
                          j_offset=j_offset,
                          k_offset=k_offset)
            self._stack.append(frame)
        if not self._skip_data:
            self._stack.geometry.detector_angles = np.copy(h5_data['detector_angles'])
        if 'volume_shape' in h5_data.keys():
            self._stack.geometry.volume_shape = np.copy(h5_data['volume_shape'])
        else:
            self._stack.geometry.volume_shape = np.array(max_shape)[[0, 0, 1]]
        # Load sample geometry information
        if 'p_direction_0' in h5_data.keys():  # TODO check for orthogonality, normality
            self._stack.geometry.p_direction_0 = np.copy(h5_data['p_direction_0'][...])
            self._stack.geometry.j_direction_0 = np.copy(h5_data['j_direction_0'][...])
            self._stack.geometry.k_direction_0 = np.copy(h5_data['k_direction_0'][...])
            logger.info('Sample geometry loaded from file.')
        else:
            logger.info('No sample geometry information was found. Default mumott geometry assumed.')

        # Load detector geometry information
        if 'detector_direction_origin' in h5_data.keys():  # TODO check for orthogonality, normality
            self._stack.geometry.detector_direction_origin = np.copy(
                h5_data['detector_direction_origin'][...])
            self._stack.geometry.detector_direction_positive_90 = np.copy(
                h5_data['detector_direction_positive_90'][...])
            logger.info('Detector geometry loaded from file.')
        else:
            logger.info('No detector geometry information was found. Default mumott geometry assumed.')

    def _matlab_to_stack(self, file_path: str):
        """
        Internal method for loading data from Matlab file.
        """
        try:
            matlab_data = loadmat(file_path)
            is_v73 = False
        except Exception as e:
            if 'v7.3' in str(e):
                logger.info('Matlab file version is v7.3, using h5py to load.')
                matlab_data = h5.File(file_path)
                is_v73 = True
            else:
                logger.warning('scipy.io.loadmat failed for unidentified reasons.'
                               ' Trying h5py.')
                matlab_data = h5.File(file_path)
                is_v73 = True
                logger.warning(
                    'The following exception was raised during execution of scipy.io.loadmat:\n' + str(e) +
                    '\nPlease proceed with caution.')
        number_of_projections = matlab_data['projection']['data'].size
        any_tomo_axis_x = False

        def load_one_frame(i: int) -> tuple:
            if is_v73:
                if not self._skip_data:
                    data = np.array(matlab_data[matlab_data['projection']['data'][i, 0]],
                                    copy=True).squeeze().astype(np.float64).T
                else:
                    data = None
                diode = np.array(matlab_data[matlab_data['projection']['diode'][i, 0]],
                                 copy=True).squeeze().astype(np.float64).T
                temp_rot_x = np.array(matlab_data[matlab_data['projection']['rot_x'][i, 0]],
                                      copy=True).squeeze().astype(np.float64)
                temp_rot_y = np.array(matlab_data[matlab_data['projection']['rot_y'][i, 0]],
                                      copy=True).squeeze().astype(np.float64)
                temp_dx = np.array(matlab_data[matlab_data['projection']['dx'][i, 0]],
                                   copy=True).squeeze().astype(np.float64)
                temp_dy = np.array(matlab_data[matlab_data['projection']['dy'][i, 0]],
                                   copy=True).squeeze().astype(np.float64)
                window_mask = np.array(matlab_data[matlab_data['projection']['window_mask'][i, 0]],
                                       copy=True).squeeze().astype(np.float64).T
                tomo_axis_x = round(matlab_data[matlab_data['projection']['par'][0, 0]]['tomo_axis_x'][0, 0])
            else:
                if not self._skip_data:
                    data = np.copy(matlab_data['projection']['data'][0, i]).astype(np.float64)
                else:
                    data = None
                diode = np.copy(matlab_data['projection']['diode'][0, i]).astype(np.float64)
                temp_rot_x = np.copy(matlab_data['projection']['rot_x'][0, i].squeeze()).astype(np.float64)
                temp_rot_y = np.copy(matlab_data['projection']['rot_y'][0, i].squeeze()).astype(np.float64)
                temp_dx = np.copy(matlab_data['projection']['dx'][0, i].squeeze()).astype(np.float64)
                temp_dy = np.copy(matlab_data['projection']['dy'][0, i].squeeze()).astype(np.float64)
                window_mask = np.copy(matlab_data['projection']['window_mask'][0, i]).astype(np.float64)
                tomo_axis_x = round(matlab_data['projection']['par'][0, 0]['tomo_axis_x'][0, 0][0, 0])
            return (np.ascontiguousarray(data), np.ascontiguousarray(diode),
                    temp_rot_x, temp_rot_y, temp_dx, temp_dy,
                    np.ascontiguousarray(window_mask), tomo_axis_x)
        max_shape = (0, 0)
        for i in range(number_of_projections):
            diode = load_one_frame(i)[1]
            max_shape = np.max((max_shape, diode.shape[:2]), axis=0)

        for i in range(number_of_projections):
            data, diode, temp_rot_x, temp_rot_y, temp_dx, temp_dy, window_mask, tomo_axis_x = \
                load_one_frame(i)
            if not self._skip_data:
                weights = window_mask[..., np.newaxis] * \
                    np.ones((1, 1, data.shape[-1]))
            else:
                weights = window_mask
            # Pad to make all frames the same shape.
            pad_sequence = np.array(((0, max_shape[0] - diode.shape[0]),
                                    (0, max_shape[1] - diode.shape[1]),
                                    (0, 0)))
            if not self._skip_data:
                data = np.pad(data, pad_sequence)
            diode = np.pad(diode, pad_sequence[:-1])
            weights = np.pad(weights, pad_sequence[:weights.ndim])
            if tomo_axis_x:
                any_tomo_axis_x = True
                rotation = \
                    self._Ry(-temp_rot_y * np.pi / 180) @ self._Rx(-temp_rot_x * np.pi / 180)
            else:
                rotation = \
                    self._Rx(temp_rot_x * np.pi / 180) @ self._Ry(temp_rot_y * np.pi / 180)
            # Append frame to stack
            j_offset = temp_dy - pad_sequence[0, 1] * 0.5
            k_offset = temp_dx - pad_sequence[1, 1] * 0.5
            frame = Frame(data=data,
                          diode=diode,
                          weights=weights,
                          rotation=rotation,
                          j_offset=j_offset,
                          k_offset=k_offset)
            self._stack.append(frame)
        number_of_segments = self._stack.data.shape[-1]
        if not self._skip_data:
            if is_v73:
                self._stack.geometry.detector_angles = np.array(matlab_data[matlab_data['projection']
                                                                ['integ'][0, 0]]
                                                                ['phi_det'][:number_of_segments, 0],
                                                                copy=True) * np.pi / 180
                matlab_data.close()
            else:
                self._stack.geometry.detector_angles = np.copy(
                    matlab_data['projection']['integ'][0, 0]
                    ['phi_det'][0, 0][0, :number_of_segments]) * np.pi / 180
        self._stack.geometry.p_direction_0 = np.array([0., 0., 1.0])
        self._stack.geometry.j_direction_0 = np.array([0., 1.0, 0.])
        self._stack.geometry.k_direction_0 = np.array([1.0, 0., 0.])
        self._stack.geometry.detector_direction_origin = np.array([1.0, 0, 0.0])
        self._stack.geometry.detector_direction_positive_90 = np.array([0, 1.0, 0])
        if any_tomo_axis_x:
            self._stack.geometry.volume_shape = np.array(max_shape)[[1, 0, 0]]
        else:
            self._stack.geometry.volume_shape = np.array(max_shape)[[1, 0, 1]]

    def __len__(self) -> int:
        """
        Length of the :attr:`stack <mumott.data_handling.stack.Stack>`
        attached to this :class:`DataContainer` instance.
        """
        return len(self._stack)

    def append(self, f: Frame) -> None:
        """
        Appends a :class:`Frame <mumott.data_handling.stack.Frame>` to the :attr:`stack`
        attached to this :class:`DataContainer` instance.
        """
        self._stack.append(f)

    @property
    def stack(self) -> Stack:
        """ The stack, containing data and geometry. """
        return self._stack

    @stack.setter
    def stack(self, val) -> None:
        self._stack = val

    @property
    def geometry(self) -> Geometry:
        """ Container of geometry information. """
        return self._stack.geometry

    @property
    def data(self) -> NDArray[np.float64]:
        """
        The data in the :attr:`stack` object
        attached to this :class:`DataContainer` instance.
        """
        return self._stack.data

    @property
    def diode(self) -> NDArray[np.float64]:
        """
        The diode data in the :attr:`stack` object
        attached to this :class:`DataContainer` instance.
        """
        return self._stack.diode

    @property
    def weights(self) -> NDArray[np.float64]:
        """
        The weights in the :attr:`stack` object
        attached to this :class:`DataContainer` instance.
        """
        return self._stack.weights

    def correct_for_transmission(self) -> None:
        """
        Applies correction from the input provided in the :attr:`diode
        <mumott.data_handling.stack.Frame>` field.  Should
        only be used if this correction has not already been applied.
        """
        if self._correct_for_transmission_called:
            logger.info(
                'DataContainer.correct_for_transmission() has been called already.'
                ' The correction has been applied previously, and the repeat call is ignored.')
            return

        data = self._stack.data / self._stack.diode[..., np.newaxis]

        for i, f in enumerate(self._stack):
            f.data = data[i]
        self._correct_for_transmission_called = True

    def _Rx(self, angle: float) -> NDArray[float]:
        """ Generate a rotation matrix for rotations around
        the x-axis, following the convention that vectors
        have components ordered ``(x, y, z)``.

        Parameters
        ----------
        angle
            The angle of the rotation.

        Returns
        -------
        R
            The rotation matrix.

        Notes
        -----
        For a vector ``v`` with shape ``(..., 3)`` and a rotation angle :attr:`angle`,
        ``np.einsum('ji, ...i', _Rx(angle), v)`` rotates the vector around the
        ``x``-axis by :attr:`angle`. If the
        coordinate system is being rotated, then
        ``np.einsum('ij, ...i', _Rx(angle), v)`` gives the vector in the
        new coordinate system.
        """
        return Rotation.from_euler('X', angle).as_matrix()

    def _Ry(self, angle: float) -> NDArray[float]:
        """ Generate a rotation matrix for rotations around
        the y-axis, following the convention that vectors
        have components ordered ``(x, y, z)``.

        Parameters
        ----------
        angle
            The angle of the rotation.

        Returns
        -------
        R
            The rotation matrix.

        Notes
        -----
        For a vector ``v`` with shape ``(..., 3)`` and a rotation angle ``angle``,
        ``np.einsum('ji, ...i', _Ry(angle), v)`` rotates the vector around the
        For a vector ``v`` with shape ``(..., 3)`` and a rotation angle :attr:`angle`,
        ``np.einsum('ji, ...i', _Ry(angle), v)`` rotates the vector around the
        ``y``-axis by :attr:`angle`. If the
        coordinate system is being rotated, then
        ``np.einsum('ij, ...i', _Ry(angle), v)`` gives the vector in the
        new coordinate system.
        """
        return Rotation.from_euler('Y', angle).as_matrix()

    def _Rz(self, angle: float) -> NDArray[float]:
        """ Generate a rotation matrix for rotations around
        the z-axis, following the convention that vectors
        have components ordered ``(x, y, z)``.

        Parameters
        ----------
        angle
            The angle of the rotation.

        Returns
        -------
        R
            The rotation matrix.

        Notes
        -----
        For a vector ``v`` with shape ``(..., 3)`` and a rotation angle :attr:`angle`,
        ``np.einsum('ji, ...i', _Rz(angle), v)`` rotates the vector around the
        ``z``-axis by :attr:`angle`. If the
        coordinate system is being rotated, then
        ``np.einsum('ij, ...i', _Rz(angle), v)`` gives the vector in the
        new coordinate system.
        """
        return Rotation.from_euler('Z', angle).as_matrix()

    def _get_str_representation(self, max_lines=50) -> str:
        """ Retrieves a string representation of the object with specified
        maximum number of lines.

        Parameters
        ----------
        max_lines
            The maximum number of lines to return.
        """
        wdt = 74
        s = []
        s += ['=' * wdt]
        s += ['DataContainer'.center(wdt)]
        s += ['-' * wdt]
        s += ['{:26} : {}'.format('Corrected for transmission', self._correct_for_transmission_called)]
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
        truncated_s += ['=' * wdt]
        return '\n'.join(truncated_s)

    def __str__(self) -> str:
        return self._get_str_representation()

    def _get_html_representation(self, max_lines=25) -> str:
        """ Retrieves an html representation of the object with specified
        maximum number of lines.

        Parameters
        ----------
        max_lines
            The maximum number of lines to return.
        """
        s = []
        s += ['<h3>DataContainer</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th></tr></thead>']
        s += ['<tbody>']
        s += ['<tr><td style="text-align: left;">Number of projections</td>']
        s += [f'<td>{len(self._stack)}</td></tr>']
        s += ['<tr><td style="text-align: left;">Corrected for transmission</td>']
        s += [f'<td>{self._correct_for_transmission_called}</td></tr>']
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
