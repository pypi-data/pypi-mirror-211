.. _data_handling:

Data handling
=============

The :mod:`data_handling` module provides functionality for loading and inspecting data.
:class:`DataContainer <mumott.data_handling.DataContainer>` is the central class of this module.
Instances (objects) of this class are created by loading data from file.
Afterwards one can access, e.g., the geometry via the :attr:`DataContainer.geometry <mumott.data_handling.DataContainer.geometry>` property, which is a :class:`Geometry <mumott.data_handling.Geometry>` object.
The series of measurements (if available) is accessible via the :attr:`DataContainer.stack <mumott.data_handling.DataContainer.stack>` property, which is a :class:`Stack <mumott.data_handling.stack.Stack>` object.
The latter acts as a list of individual measurements, which are provided as :class:`Frame <mumott.data_handling.stack.Frame>` objects.

.. autoclass:: mumott.data_handling.DataContainer
   :members:

.. autoclass:: mumott.data_handling.stack.Stack
   :members:

.. autoclass:: mumott.data_handling.stack.Frame
   :members:

.. autoclass:: mumott.data_handling.Geometry
   :members:

Utilities
---------
.. automodule:: mumott.data_handling.utilities
   :members:
