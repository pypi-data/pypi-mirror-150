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
This file aims to collect functions related to the Quantum Spectral Tomography.

"""
import scipy.linalg as la
import numpy as np
from copy import deepcopy
from qcompute_qep.exceptions.QEPError import ArgumentError
from qcompute_qep.tomography import Tomography, ProcessTomography
from qcompute_qep.utils.types import QComputer, QProgram, number_of_qubits
from qcompute_qep.utils.circuit import execute
from qcompute_qep.quantum.pauli import complete_pauli_basis
from typing import List, Union, Tuple
from qcompute_qep.utils.utils import expval_from_counts


class SpectralTomography(Tomography):
    """The Quantum Spectral Tomography class.

    Quantum Spectral Tomography deals with identifying the eigenvalues of an unknown quantum dynamical process in PTM form.
    """
    def __init__(self, qp: QProgram = None, qc: QComputer = None, **kwargs):
        """
        The init function of the Quantum Spectral Tomography class.

        The init function of the Quantum Spectral Tomography class. Optional keywords list are:

            + `shots`: default to :math:`8192`, the number of shots each measurement should carry out
            + `k`: default to None, number of channel reuse
            + `l`: default to None, pencil parameter, determine the shape of matrix :math:`Y`
            + `N`: default to None, the number of eigenvalues
            + `a`: default to False, decide whether to calculate amplitude

        :param qp: QProgram, quantum program for creating the target quantum process
        :param qc: QComputer, the quantum computer

        """
        super().__init__(qp, qc, **kwargs)
        self._qp: QProgram = qp
        self._qc: QComputer = qc
        # self._method: str = kwargs.get('method', 'inverse')
        self._shots: int = kwargs.get('shots', 8192)
        self._K: int = kwargs.get('k', None)
        self._L: int = kwargs.get('l', None)
        self._N: int = kwargs.get('N', None)
        self._amp = kwargs.get('a', False)

    def _repeat_channel(self) -> List[QProgram]:
        """
        :return: a list of quantum circuit repeating k times quantum channel
        """
        # Construct g(0)
        start_qp = deepcopy(self._qp)
        start_qp.circuit.clear()

        k_qps: List[QProgram] = [start_qp]
        # Construct g(1) .... g(K)
        for _ in range(self._K):
            k_qp = deepcopy(k_qps[-1])
            k_qp.circuit = k_qp.circuit + self._qp.circuit
            k_qps.append(k_qp)

        return k_qps

    def fit(self, qp: QProgram = None, qc: QComputer = None, **kwargs) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Execute the quantum spectral procedure for the quantum process specified by @qp on the quantum computer @qc.

        Optional keywords list are:

            + `shots`: default to :math:`8192`, the number of shots each measurement should carry out
            + `k`: default to :math:`2 N-2`, number of channel reuse
            + `l`: default to :math:`K/2`, pencil parameter, determine the shape of matrix :math:`Y`
            + `N`: default to :math:`4^n - 1`, a variable to fit the signal (consider degenerate)
            + `a`: default to False, decide whether to calculate amplitude

        :param qp: QProgram, quantum program for creating the target quantum process
        :param qc: QComputer, the quantum computer instance
        :return: the estimated quantum process in the Pauli transfer matrix form

        Usage:

        .. code-block:: python
            :linenos:

            rho = SpectralTomography.fit(qp=qp, qc=qc)
            rho = SpectralTomography.fit(qp=qp, qc=qc, method='inverse')
            rho = SpectralTomography.fit(qp=qp, qc=qc, method='lstsq', shots=shots)

        **Examples**

            >>> import QCompute
            >>> import qcompute_qep.tomography as tomography
            >>> qp = QCompute.QEnv()
            >>> qp.Q.createList(2)
            >>> QCompute.H(qp.Q[0])
            >>> QCompute.CZ(qp.Q[1], qp.Q[0])
            >>> QCompute.H(qp.Q[0])
            >>> qc = QCompute.BackendName.LocalBaiduSim2
            >>> st = tomography.SpectralTomography()
            >>> noisy_ptm = st.fit(qp, qc, k=50, l=30, N=2)

        """
        # Parse the arguments. If not set, use the default arguments set by the init function
        self._qp = qp if qp is not None else self._qp
        self._qc = qc if qc is not None else self._qc
        self._shots = kwargs.get('shots', self._shots)
        self._K = kwargs.get('k', self._K)
        self._L = kwargs.get('l', self._L)
        self._amp = kwargs.get('a', self._amp)

        # If the quantum program or the quantum computer is not set, the process tomography cannot be executed
        if self._qp is None:
            raise ArgumentError("in SpectralTomography.fit(): the quantum program is not set!")
        if self._qc is None:
            raise ArgumentError("in SpectralTomography.fit(): the quantum computer is not set!")

        # Number of qubits in the quantum program representing the quantum process
        n = number_of_qubits(qp)
        # Consider the :math:`N` as a variable, default to :math:`4^n-1`
        N = kwargs.get('N', 4**n-1) if self._N is None else kwargs.get('N', self._N)
        # Set the default parameter K and L
        self._K = 2 * N - 2 if self._K is None else self._K
        self._L = int(self._K / 2) if self._L is None else self._L
        meas_paulis = complete_pauli_basis(n)[1:]  # a list of string, Pauli basis
        # Applying the gate k times
        k_qps = self._repeat_channel()

        g = np.zeros(self._K+1, dtype=float)

        # Gather the data to estimate g(k)
        for k, k_qp in enumerate(k_qps):
            # Construct the measurement circuit for k-th circuit
            for i, meas_pauli in enumerate(meas_paulis):
                meas_qp, meas_ob = meas_pauli.meas_circuit(k_qp)
                qps, eig_vals = meas_pauli.preps_circuits(meas_qp)
                for j, qp in enumerate(qps):
                    counts = execute(qp=qp, qc=self._qc, shots=self._shots)
                    expval = expval_from_counts(A=meas_ob, counts=counts)
                    g[k] = g[k] + expval * eig_vals[j]

            g[k] = g[k] / (2**n)

        # print("the g(k) sequence is \n", g)

        # Construct a (K-L+1) \times (L+1) dimensional data matrix Y
        Y = np.zeros((self._K-self._L+1, self._L+1), dtype=float)
        for i in range(self._L+1):
            Y[:, i] = np.asarray(g[i:i+self._K-self._L+1].T)

        # Construct a singular-value decomposition of the matrix Y
        _, sigma, vt = np.linalg.svd(Y)
        if len(sigma) > N:
            sigma = sigma[:N]
            vt = vt[:N, :]
        vt0 = vt[:, :-1]
        vt1 = vt[:, 1:]
        eig_vals, _ = np.linalg.eig(vt0 @ la.pinv(vt1))

        # Only calculate eigenvalues we estimate
        if self._amp is False:
            return eig_vals
        
        # TODO: use least-squares minimization to calculate the amplitude of noisy signal
        amplitudes = np.zeros((N, 1), dtype=complex)

        return eig_vals, amplitudes
