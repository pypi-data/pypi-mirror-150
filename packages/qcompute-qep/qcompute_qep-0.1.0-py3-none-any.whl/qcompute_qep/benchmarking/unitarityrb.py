#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unitarity Randomized Benchmarking.
A scalable and robust algorithm for benchmarking the unitarity of the Clifford gates
by a single parameter called UPC (unitarity per Clifford) using randomization techniques.
"""
import itertools
import qiskit
import qiskit.quantum_info as qi
from typing import List, Tuple, Union, Optional
import functools

import numpy as np
import QCompute
from qcompute_qep.utils.linalg import tensor
from qcompute_qep.utils import expval_from_counts, execute, circuit, expval_z_from_counts
from qcompute_qep.quantum import clifford
from qiskit.providers.aer.noise import NoiseModel
import qcompute_qep.exceptions.QEPError as QEPError
import qcompute_qep.benchmarking as rb
from qcompute_qep.utils.types import QComputer, get_qc_name, QProgram
from scipy.optimize import curve_fit
from copy import deepcopy

try:
    from matplotlib import pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import pylab

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class UnitarityRB(rb.RandomizedBenchmarking):
    """
    The Unitarity Randomized Benchmarking class.
    Aim to benchmark the coherence(unitarity) noise of a complete set of Cliffords.
    """

    def __init__(self, qc: QComputer = None, qubits: List[int] = None, **kwargs):
        r"""init function of the Unitarity Randomized Benchmarking class.

        Optional keywords list are:

        + ``seq_lengths``: List[int], default to :math:`[1, 10, 20, 50, 75, 100]`, a list of sequence lengths
        + ``repeats``: int, default to :math:`6`, the number of repetitions of each sequence length
        + ``shots``: int, default to :math:`8192`, the number of shots each measurement carries out to estimate the value
        + ``prep_circuit``: default to `default_prep_circuit`, prepares the initial quantum state :math:`\vert 0\cdots 0`
        + ``meas_circuit``: default to `default_meas_circuit`, add the Z basis measurement to the end of the
                RB circuits and set the quantum observable to :math:`\vert 0\cdots 0\rangle\!\langle 0\cdots 0\vert`

        :param qc: QComputer, the quantum computer on which the RB carries out
        :param qubits: List[int], the qubits who will be benchmarked
        """
        # Initialize the URB parameters. If not set, use the default parameters
        super().__init__(**kwargs)
        self._qc = qc
        self._qubits = qubits
        self._seq_lengths = kwargs.get('seq_lengths', [1, 10, 20, 50, 75, 100])
        self._repeats = kwargs.get('repeats', 6)
        self._shots = kwargs.get('shots', 8192)
        self._prep_circuit = kwargs.get('prep_circuit', rb.default_prep_circuit)
        self._meas_circuit = kwargs.get('meas_circuit', rb.default_meas_circuit)

        # Store the URB results. Initialize to an empty dictionary
        self._results = dict()

        # Store the URB parameters. Initialize to an empty dictionary
        self._params = dict()

    @property
    def params(self) -> dict:
        r"""
        Return the used parameters in unitarity randomized benchmarking in a dictionary
        """
        if not self._params:
            urb_params = dict()
            urb_params['qc'] = get_qc_name(self._qc)
            urb_params['qubits'] = self._qubits
            urb_params['seq_lengths'] = self._seq_lengths
            urb_params['repeats'] = self._repeats
            urb_params['shots'] = self._shots
            urb_params['prep_circuit'] = self._prep_circuit
            urb_params['meas_circuit'] = self._meas_circuit
            self._params = urb_params

        return self._params

    @property
    def results(self) -> dict:
        """
        Return the unitarity randomized benchmarking results in a dictionary.
        """
        # If the randomized benchmarking results have not been generated yet,
        # call the benchmark function to generate the results using the default parameters
        if (self._results is None) or (bool(self._results) is False):
            self.benchmark(self._qc, self._qubits)

        return self._results

    def _fit_func(self, m: int, u: float, A: float, B: float) -> np.ndarray:
        r"""The fit function used in the unitarity randomized benchmarking.

        The used fit function is an exponential function in the input and is defined as follows:

        .. math:: p(x) = A u^{m-1} + B

        where

        + :math:`m` is the sequence length, i.e., the number of Cliffords in the sequence,
        + :math:`u` is the unitarity of the Cliffords
        + :math:`A` and :math:`B` absorb the state preparation and measurement errors (SPAM).

        :param m: int, corresponds to the sequence length
        :param u: float, the unitarity of the noise
        :param A: float, a parameter that absorbs the state preparation and measurement errors
        :param B: float, another parameter that absorbs the state preparation and measurement errors
        :return: np.ndarray, the estimated expectation value
        """
        return A * u ** (m - 1) + B

    def benchmark(self, qc: QComputer, qubits: List[int], **kwargs) -> dict:
        r"""Execute the unitarity randomized benchmarking procedure on the quantum computer.

        The parameters `qc` and `qubits` must be set either by the init() function or here,
        otherwise the unitarity randomized benchmarking procedure will not carry out.

        Optional keywords list are:

        + ``seq_lengths``: List[int], default to :math:`[1, 10, 20, 50, 75, 100]`, the list of sequence lengths
        + ``repeats``: int, default to :math:`6`, the number of repetitions of each sequence length
        + ``shots``: int, default to :math:`8192`, the number of shots each measurement should carry out
        + ``prep_circuit``: default to `default_prep_circuit`, prepares the initial quantum state :math:`\vert 0\cdots 0\rangle`
        + ``meas_circuit``: default to `default_meas_circuit`, add the Z basis measurement and set the quantum observable to :math:`\vert 0\cdots 0\rangle\!\langle 0\cdots 0\vert`

        **Usage**

        .. code-block:: python
            :linenos:

            urb_results = urb.benchmark(qubits=[1], qc=qc)
            urb_results = urb.benchmark(qubits=[1], qc=qc, seq_lengths=[1,10,50,100])
            urb_results = urb.benchmark(qubits=[1], qc=qc, seq_lengths=[1,10,50,100], repeats=10, shots=1024)

            u = urb_results['u']  # the estimated unitarity
            u_err = urb_results['u_err']  # the standard deviation error of the estimation

        :return: dict, the randomized benchmarking results

        **Examples**

            >>> import qiskit
            >>> from qiskit.test import mock
            >>> from qcompute_qep.benchmarking.unitarityrb import UnitarityRB
            >>> qc = qiskit.providers.aer.AerSimulator.from_backend(mock.FakeSantiago())
            >>> urb = UnitarityRB(qubits=[0], qc=qc)
            >>> urb_results = urb.benchmark()
            >>> urb.plot_results()
        """
        # Parse the arguments from the key list. If not set, use default arguments from the init function
        self._qc = qc if qc is not None else self._qc
        self._qubits = qubits if qubits is not None else self._qubits
        self._seq_lengths = kwargs.get('seq_lengths', self._seq_lengths)
        self._repeats = kwargs.get('repeats', self._repeats)
        self._shots = kwargs.get('shots', self._shots)
        self._prep_circuit = kwargs.get('prep_circuit', self._prep_circuit)
        self._meas_circuit = kwargs.get('meas_circuit', self._meas_circuit)

        if self._qc is None:
            raise QEPError.ArgumentError("URB: the quantum computer for benchmarking is not specified!")
        if self._qubits is None:
            raise QEPError.ArgumentError("URB: the qubits for benchmarking are not specified!")

        ###############################################################################################################
        # Step 1. Data Collection Phase.
        #   First construct the list of benchmarking quantum circuits.
        #   Then for each RB quantum circuit, evaluate its expectation value.
        ###############################################################################################################
        # Store the estimated expectation values, which is a :math:`R \times M` array,
        # where :math:`R` is the number of repeats and :math:`M` is the number of sequences
        expvals = np.empty([self._repeats, len(self._seq_lengths)], dtype=float)

        n = len(self._qubits)  # number of qubits
        for m, seq_m in enumerate(self._seq_lengths):
            for r in range(self._repeats):
                cliffords = clifford.random_clifford(n, seq_m)
                rb_qp = QCompute.QEnv()
                q = rb_qp.Q.createList(n)
                for c in cliffords:
                    c(q, self._qubits)

                # The same state measuring in complete Pauli basis,
                # For n qubits, there are totally 4^n-1 Pauli basis
                # subtracted off the identity Pauli basis
                expval = 0
                for pauli_str in itertools.product(['I', 'X', 'Y', 'Z'], repeat=n):
                    p = list(pauli_str)
                    if all(x == 'I' for x in p):
                        continue
                    meas_qp, meas_ob = _meas_circuit(p, rb_qp, self._qubits)
                    counts = execute(qp=meas_qp, qc=self._qc, shots=self._shots, optimization_level=0)
                    expval += expval_from_counts(meas_ob, counts) ** 2
                expvals[r, m] = expval*2**n / (2 ** n - 1)

        ###############################################################################################################
        # Step 2. Data Processing Phase.
        #   Fit the list of averaged expectation values to the exponential model and extract the fitting results.
        ###############################################################################################################
        # Set the bounds for the parameters tuple: :math:`(u, A, B)`
        # bounds = ([0, min_eig - max_eig, min_eig], [1, max_eig - min_eig, max_eig])
        bounds = ([0, 0, 0], [1, 1, 1])
        # Use scipy's non-linear least squares to fit the data
        xdata = self._seq_lengths
        ydata = np.mean(expvals, axis=0)
        sigma = np.std(expvals, axis=0)
        if len(sigma) - np.count_nonzero(sigma) > 0:
            sigma = None

        p0 = [1, 0.5, 0.5]
        # Use the first two points to guess the decay param (qiskit method)
        # p0 = [0.99, 0.95, 1 / 2 ** n]
        # dx = (xdata[1] - xdata[0])
        # dy = ((ydata[1] - p0[2]) / (ydata[0] - p0[2]))
        # alpha_guess = dy ** (1 / dx)
        # if alpha_guess < 1.0:
        # p0[0] = alpha_guess
        # if ydata[0] > p0[2]:
        # p0[1] = ((ydata[0] - p0[2]) / p0[0] ** xdata[0])

        popt, pcov = curve_fit(self._fit_func, xdata, ydata, p0=p0, sigma=sigma, bounds=bounds,
                               method='trf')
        # Store the randomized benchmarking results
        params_err = np.sqrt(np.diag(pcov))
        self._results['expvals'] = expvals
        self._results['u'] = popt[0]
        self._results['A'] = popt[1]
        self._results['B'] = popt[2]
        self._results['u_err'] = params_err[0]

        return self._results

    def plot_results(self, show: bool = True, fname: str = None):
        r"""Plot unitarity randomized benchmarking results.

        Commonly, we visualize the sampled and averaged expectation values for each given length,
        the fitted function, and the estimated unitarity.

        :param show: bool, default to True, show the plot figure or not
        :param fname: figure name for saving. If fname is None, do not save the figure
        """

        if not HAS_MATPLOTLIB:
            raise ImportError('Function "plot_results" requires matplotlib. Run "pip install matplotlib" first.')

        fig, ax = plt.subplots(figsize=(12, 8))

        xdata = self._seq_lengths
        expvals = self.results['expvals']

        # Plot the repeated estimates for each sequence
        for r in range(self._repeats):
            ax.plot(xdata, expvals[r, :], color='gray', linestyle='none', marker='x')

        # Plot the mean of the estimated expectation values with error bars
        ax.errorbar(xdata, np.mean(expvals, axis=0), yerr=np.std(expvals, axis=0),
                    color='r', linestyle='--', linewidth=2)

        # Plot the fitting function
        ydata = [self._fit_func(x, self.results['u'], self.results['A'], self.results['B']) for x in xdata]
        ax.plot(xdata, ydata, color='blue', linestyle='-', linewidth=2)
        ax.tick_params(labelsize='medium')

        # Set the labels
        ax.set_xlabel('Clifford Length', fontsize='large')
        ax.set_ylabel('Expectation Value', fontsize='large')
        ax.grid(True)

        # Fix the y limit
        ax.set_ylim([0, 1])

        # Add the estimated fidelity and EPC parameters
        bbox_props = dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5)
        ax.text(0.85, 0.9,
                "u: {:.3f}({:.1e}) \n".format(self.results['u'],
                                              self.results['u_err']),
                ha="center", va="center", fontsize='medium', bbox=bbox_props, transform=ax.transAxes)

        # Save the figure if `fname` is set
        if fname is not None:
            plt.savefig(fname, format='png', dpi=600, bbox_inches='tight', pad_inches=0.1)
        # Show the figure if `show==True`
        if show:
            plt.show()


def _prep_circuit(pauli, qp1: QProgram, qp2: QProgram, qubits) -> Tuple[QProgram, QProgram]:
    """
    The function is testing for class UnitarityRB. Will be deprecated in the future.
    """
    n = circuit.number_of_qubits(qp1)
    q1 = qp1.Q.toListPair()[0]
    q2 = qp2.Q.toListPair()[0]
    if pauli == 'X':
        for i in range(n):
            QCompute.H(q1[qubits[i]])
        for i in range(n):
            QCompute.X(q2[qubits[i]])
            QCompute.H(q2[qubits[i]])
    elif pauli == 'Z':
        for i in range(n):
            QCompute.X(q2[qubits[i]])
    elif pauli == 'Y':
        for i in range(n):
            QCompute.H(q1[qubits[i]])
            QCompute.S(q1[qubits[i]])
        for i in range(n):
            QCompute.X(q2[qubits[i]])
            QCompute.H(q2[qubits[i]])
            QCompute.S(q2[qubits[i]])

    return qp1, qp2


def _meas_circuit(pauli, qp, qubits):
    """
    This function is only used in class UnitarityRB. For qiskit.QuantumCircuit only
    Will be updated in the future.
    """
    if isinstance(qp, QCompute.QEnv):
        eigs = []
        n = circuit.number_of_qubits(qp)
        meas_qp = deepcopy(qp)
        q = meas_qp.Q
        for idx in range(len(pauli)):
            i = n - idx - 1
            P = pauli[i]
            if P == 'X':
                QCompute.H(q[qubits[i]])
            elif P == 'Y':
                QCompute.H(q[qubits[i]])
                QCompute.S(q[qubits[i]])
            else:
                pass
            eigs.append(np.diag([1, 1]) / np.sqrt(2) if P == 'I' else np.diag([1, -1]) / np.sqrt(2))

            # If the given quantum program does not contain a measurement, measure it in the Z basis
        QCompute.MeasureZ(*meas_qp.Q.toListPair())
        meas_ob = tensor(eigs)
        return meas_qp, meas_ob
    else:
        n = qp.qubits
        meas = qiskit.QuantumCircuit(n)
        for i in range(len(pauli)):
            P = pauli[i]
            if P == 'X':
                meas.h(qubits[i])
            elif P == 'Y':
                meas.h([qubits[i]])
                meas.s([qubits[i]])
            elif P == 'I':
                meas.id([qubits[i]])
            elif P == 'Z':
                pass

        return meas
