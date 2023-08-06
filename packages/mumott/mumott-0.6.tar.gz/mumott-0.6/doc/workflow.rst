.. _workflow:
.. index:: Workflow

.. raw:: html

    <style> .orange {color:orange} </style>
    <style> .blue {color:CornflowerBlue} </style>
    <style> .green {color:darkgreen} </style>

.. role:: orange
.. role:: blue
.. role:: green


Workflow
********

The following figure illustrates the :program:`mumott` workflow.
Here, classes are shown in :blue:`blue`, input parameters and data in :orange:`orange`, and output data in :green:`green`.

.. graphviz:: _static/workflow.dot

A typical workflow involves the following steps:

#. First the :orange:`measured data along with its metadata` is loaded into a :class:`DataContainer <mumott.data_handling.DataContainer>` object.
   The latter allows one to access, inspect, and modify the data in various ways as shown in the
   `tutorial on loading and inspecting data tutorial <tutorials/inspect_data.html>`_.
   Note that it is possible to skip the full data when instantiating a :class:`DataContainer <mumott.data_handling.DataContainer>` object.
   In that case only geometry and diode data are read, which is much faster and sufficient for alignment.

#. The :class:`DataContainer <mumott.data_handling.DataContainer>` object holds the information pertaining to the geometry of the data.
   The latter is stored in the :attr:`geometry <mumott.data_handling.DataContainer.geometry>` property of the
   :class:`DataContainer <mumott.data_handling.DataContainer>` object in the form of a :class:`Geometry <mumott.data_handling.Geometry>` object.

#. The geometry information is then used to set up a :ref:`projector object <projectors>`,
   e.g., :attr:`SAXSProjectorNumba <mumott.methods.projectors.SAXSProjectorNumba>`.
   Projector objects allow one to transform tensor fields from three-dimensional space to projection space.

#. Next a :ref:`basis set object <basis_sets>` such as, e.g., :class:`SphericalHarmonics <mumott.methods.basis_sets.SphericalHarmonics>`, is set up.

#. One can then combine the :ref:`projector object <projectors>`, the :ref:`basis set <basis_sets>`, and the data from
   the :class:`DataContainer <mumott.data_handling.DataContainer>` object to set up a :ref:`functional object <functionals>`.
   :ref:`Functional obejcts <functionals>` hold the coefficients that need to be optimized and allow one to compute the residuals of the current representation.

#. To find the optimal coefficients a :ref:`loss function object <loss_functions>` is set up, using, e.g., the :class:`SquaredLoss <mumott.optimization.loss_functions.SquaredLoss>` or :class:`HuberLoss <mumott.optimization.loss_functions.HuberLoss>` classes.
   The :ref:`loss function <loss_functions>` can include one or several regularization terms, which are defined by :ref:`regularizer objects <regularizers>` such as :class:`L1Norm <mumott.optimization.regularizers.L1Norm>`, :class:`L2Norm <mumott.optimization.regularizers.L2Norm>` or :class:`TotalVariation <mumott.optimization.regularizers.TotalVariation>`.

#. The :ref:`loss function object <loss_functions>` is then handed over to an :ref:`optimizer object <optimizers>`,
   such as :class:`LBFGS <mumott.optimization.optimizers.LBFGS>` or :class:`GradientDescent <mumott.optimization.optimizers.GradientDescent>`,
   which updates the coefficients of the :ref:`functional object <functionals>`.

#. The optimized coefficients can then be processed via the :ref:`basis set object <basis_sets>`
   to generate :green:`tensor field properties` such as the anisotropy or the orientation distribution.
