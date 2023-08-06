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
This file aims to collect functions related to the Quantum state tomography.

"""

from qcompute_qep.utils.circuit import execute
from typing import List, Union
import scipy.linalg as la
import numpy as np

from qcompute_qep.exceptions.QEPError import ArgumentError
from qcompute_qep.tomography import Tomography, MeasurementBasis, init_measurement_basis
from qcompute_qep.utils.types import QComputer, QProgram, number_of_qubits
from qcompute_qep.utils.linalg import dagger
from qcompute_qep.quantum.pauli import ptm_to_operator
from qcompute_qep.utils.utils import expval_from_counts


class StateTomography(Tomography):
    """The Quantum State Tomography class.

    Quantum state tomography is the process by which a quantum state is reconstructed using measurements on an ensemble
    of identical quantum states.
    """
    def __init__(self, qp: QProgram = None, qc: QComputer = None, **kwargs):
        r"""
        The init function of the Quantum State Tomography class.

        Optional keywords list are:

            + `method`: default to ``inverse``, specify the state tomography method
            + `shots`: default to :math:`8192`, the number of shots each measurement should carry out
            + `basis`: default to ``PauliMeasBasis``, the measurement basis
            + `ptm`: default to ``False``, if the quantum state should be returned to the Pauli transfer matrix form

        :param qp: QProgram, quantum program for creating the target quantum state
        :param qc: QComputer, the quantum computer

        """
        super().__init__(qp, qc, **kwargs)
        self._qp: QProgram = qp
        self._qc: QComputer = qc
        self._method: str = kwargs.get('method', 'inverse')
        self._shots: int = kwargs.get('shots', 8192)
        self._ptm: bool = kwargs.get('ptm', False)
        # Setup the the measurement basis for quantum state tomography
        self._basis: Union[str, MeasurementBasis] = init_measurement_basis(kwargs.get('basis', None))

    def fit(self, qp: QProgram = None, qc: QComputer = None, **kwargs) -> np.ndarray:
        r"""
        Execute the quantum state procedure for the quantum state specified by @qp on the quantum computer @qc.

        Optional keywords list are:

            + `method`: default to ``inverse``, specify the state tomography method. Current support:

                + ``inverse``: the inverse method;
                + ``lstsq``: the least square method;
                + ``mle``: the maximum likelihood estimation method.

            + `shots`: default to :math:`8192`, the number of shots each measurement should carry out

            + `basis`: default to ``PauliMeasBasis``, the measurement basis

            + `ptm`: default to ``False``, if the quantum state should be returned to the Pauli transfer matrix form

        :param qp: QProgram, quantum program for creating the target quantum state
        :param qc: QComputer, the quantum computer instance
        :return: np.ndarray, the estimated quantum state

        Usage:

        .. code-block:: python
            :linenos:

            rho = StateTomography.fit(qp=qp, qc=qc)
            rho = StateTomography.fit(qp=qp, qc=qc, method='inverse')
            rho = StateTomography.fit(qp=qp, qc=qc, method='lstsq', shots=8192)

        **Examples**

            >>> from qcompute_qep.quantum.pauli import operator_to_ptm, complete_pauli_basis
            >>> from qcompute_qep.utils.circuit import circuit_to_state
            >>> from qcompute_qep.quantum.metrics import state_fidelity
            >>> qp = QCompute.QEnv()
            >>> qp.Q.createList(2)
            >>> QCompute.H(qp.Q[0])
            >>> QCompute.CX(qp.Q[0], qp.Q[1])
            >>> ideal_state = circuit_to_state(qp, vector=False)
            >>> qc = QCompute.BackendName.LocalBaiduSim2
            >>> st = StateTomography()
            >>> noisy_state = st.fit(qp, qc, method='inverse', shots=8192)
            >>> ideal_ptm = operator_to_ptm(ideal_state)
            >>> noisy_ptm = operator_to_ptm(noisy_state)
            >>> fid = state_fidelity(ideal_state, noisy_state.data)
            >>> print('Fidelity between the ideal and noisy states: F = {:.5f}'.format(fid))
            Fidelity between the ideal and noisy states: F = 1.00000

            Fidelity between the ideal and noisy states: F = 1.00000

        """
        # Parse the arguments. If not set, use the default arguments set by the init function
        self._qp = qp if qp is not None else self._qsp
        self._qc = qc if qc is not None else self._qc
        self._method = kwargs.get('method', self._method)
        self._shots = kwargs.get('shots', self._shots)
        self._ptm = kwargs.get('ptm', self._ptm)
        # Setup the the measurement basis for state tomography
        self._basis = init_measurement_basis(kwargs.get('basis', self._basis))

        # If the quantum program or the quantum computer is not set, the state tomography cannot be executed
        if self._qp is None:
            raise ArgumentError("in StateTomography.fit(): the quantum program is not set!")
        if self._qc is None:
            raise ArgumentError("in StateTomography.fit(): the quantum computer is not set!")

        # Number of qubits in the quantum program
        n = number_of_qubits(qp)

        # Step 1. construct a list of tomographic quantum circuits from the quantum program
        tomo_qps, tomo_obs = self._basis.meas_circuits(self._qp)

        # Step 2. run the tomographic quantum circuits on the quantum computer and estimate the expectation values
        ptm: List[float] = []
        for i in range(len(tomo_qps)):
            counts = execute(qp=tomo_qps[i], qc=self._qc, shots=self._shots)
            expval = expval_from_counts(A=tomo_obs[i], counts=counts)
            ptm.append(expval)

        # Step 3. perform the fitting procedure to estimate the quantum state
        # Obtain the transition matrix for the measurement basis
        M = self._basis.transition_matrix(n)
        if self._method.lower() == 'inverse':  # The naive inverse method
            # Compute the pseudoinverse of the transition matrix
            M_inv = la.pinv(M)
            rho_ptm = np.dot(M_inv, np.asarray(ptm))
        elif self._method.lower() == 'lstsq':  # the ordinary least square method
            rho_ptm = la.pinv(dagger(M) @ M) @ dagger(M) @ np.asarray(ptm)
        elif self._method.lower() == 'mle':  # the maximum likelihood estimation
            rho_ptm = None
            pass
        else:
            raise ArgumentError("In StateTomography.fit(), unsupported tomography method '{}'".format(self._method))

        if self._ptm:
            return rho_ptm
        else:
            return ptm_to_operator(rho_ptm)
