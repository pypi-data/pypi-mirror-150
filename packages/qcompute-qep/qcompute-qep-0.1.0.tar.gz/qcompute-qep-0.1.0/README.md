*Copyright (c) 2022 Institute for Quantum Computing, Baidu Inc. All Rights Reserved.*

[![](https://img.shields.io/badge/license-Apache%202.0-green)](./LICENSE) [![](https://img.shields.io/badge/build-passing-green)]() ![](https://img.shields.io/badge/Python-3.8--3.9-blue) ![](https://img.shields.io/badge/release-v0.1.0-blue)

## About QEP

**QEP (量噪)** is a **Q**uantum **E**rror **P**rocessing toolkit developed by the [Institute for Quantum Computing](https://quantum.baidu.com) at [Baidu Research](http://research.baidu.com). It aims to deal with quantum errors inherent in quantum devices using software solutions. Currently, it offers three powerful quantum error processing functions: randomized benchmarking, quantum error characterization, and quantum error mitigation:

+ **Randomized benchmarking** is used for assessing the capabilities and extendibilities of quantum computing hardware platforms, through estimating the average error rates that are measured with long sequences of random quantum circuits. It provides standard randomized benchmarking, cross-entropy benchmarking, the unitarity randomized benchmarking.

+ **Quantum error characterization** is used for reconstructing the comprehensive information in quantum computing hardware platforms, through many partial and limited experimental results. It provides quantum state tomography, quantum process tomography, and spectral quantum tomography.

+ **Quantum error mitigation** is used for improving the accuracy of quantum computational results, through post-processing the experiment data obtained by varying noisy experiments, extending the computational reach of a noisy superconducting quantum processor. It provides zero-noise extrapolation technique to mitigate quantum gate noise, and a collection of methods such as inverse, least-square, iterative Bayesian unfolding, Neumann series to mitigate quantum measurement noise.

QEP is based on [QCompute](https://quantum-hub.baidu.com/opensource), a Python-based open-source quantum computing platform SDK also developed by [Institute for Quantum Computing](https://quantum.baidu.com). It provides a full-stack programming experience for senior users via hybrid quantum programming language features and high-performance simulators. You can install QCompute via [pypi](https://pypi.org/project/qcompute/). When you install QEP, the dependency QCompute will be automatically installed. Please refer to QCompute's official [Open Source](https://quantum-hub.baidu.com/opensource) page for more details.

## Installation

The package QEP is compatible with 64-bit Python 3.8 and 3.9, on Linux, MacOS (10.14 or later) and Windows. We highly recommend the users to install QEP via `pip`. Open the Terminal and run

```bash
pip install qcompute-qep
```

This will install the QEP binaries as well as the QEP package. For those using an older version of QEP, keep up to date by installing with the `--upgrade` flag for additional features and bug fixes.

After successfully installing QEP, you can run the test example within the `qcompute_qep` Source Distribution to check out whether the installation is successful

```bash
cd qcompute_qep/tests/
python example-qcompute-qep.py
```

## Tutorials

QEP provides detailed and comprehensive tutorials for randomized benchmarking, quantum error characterization, and quantum error mitigation, from theoretical analysis to practical application. We recommend the interested researchers or deverlopers to download the Jupyter Notebooks and try it. The tutorials are listed as follows:

+ **Randomized Benchmarking**
  
  + [Standard Randomized Benchmarking](https://quantum-hub.baidu.com/qep/tutorial-standardrb)
  + [Cross-Entropy Benchmarking](https://quantum-hub.baidu.com/qep/tutorial-xeb)
  + [Unitarity Randomized Benchmarking](https://quantum-hub.baidu.com/qep/tutorial-unitarityrb)

+ **Quantum Error Characterization**
  
  + [Quantum State Tomography](https://quantum-hub.baidu.com/qep/tutorial-qst)
  + [Quantum Process Tomography](https://quantum-hub.baidu.com/qep/tutorial-qpt)
  + [Spectral Quantum Tomography](https://quantum-hub.baidu.com/qep/tutorial-sqt)

+ **Quantum Error Mitigation**
  
  + [Zero-Noise Extrapolation](https://quantum-hub.baidu.com/qep/tutorial-zne)
  + [Measurement Error Mitigation](https://quantum-hub.baidu.com/qep/tutorial-mem)
  + [Applications of Measurement Error Mitigation](https://quantum-hub.baidu.com/qep/tutorial-mem-applications)

## Contribution Guidelines

Comments, suggestions, and code contributions are warmly welcome. Please contact us via Email: quantum@baidu.com .
