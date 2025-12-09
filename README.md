# Decoherence-Triggered Collapse (DTC) 
A Deterministic Effective Theory of the Quantum-to-Classical Transition


[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

This repository contains the reference implementation, simulation tools, and validation suite for the **Decoherence-Triggered Collapse (DTC) model**: a deterministic, threshold-based objective collapse mechanism that links state reduction directly to environmental decoherence.

DTC introduces no stochastic noise, preserves exact unitarity for isolated systems, and provides a physically motivated collapse threshold derived from environmental scattering rates. The model yields sharp, tail-free macroscopic localization while remaining fully consistent with all experimental constraints as of 2025.

This repository accompanies the research preprint:

**R. Chung (2025).** *Decoherence-Triggered Collapse: A Deterministic Effective Theory of the Quantum-to-Classical Transition.*

---

## Overview

Standard quantum mechanics suppresses interference through environmental decoherence but offers no mechanism for actual state selection. Stochastic collapse theories (e.g., GRW, CSL) introduce ad hoc noise fields that generate spontaneous heating.

**DTC is a deterministic alternative.** Collapse occurs only when environmental decoherence suppresses total coherence below a universal **irreversibility threshold** $\( C_{\mathrm{irr}} \approx 10^{-20} \)$. Beyond this threshold, non-actualized branches are eliminated via a non-local geometric projection in the pointer basis.

For all isolated microscopic systems $\( C(\rho) \gg C_{\mathrm{irr}} \)$, the trigger is inactive, ensuring:

* strictly unitary evolution
* zero spontaneous heating
* no additional free parameters

Macroscopic collapse emerges naturally from environmental scattering.



## Key Features

* **Deterministic Collapse:** Triggered solely by decoherence crossing a physical threshold.
* **Exact Unitarity for Microscopic Systems:** Identical to standard quantum mechanics when isolated.
* **Tail-Free Macroscopic Localization:** Sharp, rapid collapse with no residual amplitudes.
* **No Stochastic Noise:** Distinct from GRW/CSL; avoids vacuum heating.
* **Born Rule Emergence:** Outcome frequencies arise from environmental phase dynamics.
* **Experimentally Testable Predictions:** Distinct signatures in interferometry and echo experiments.



## Mathematical Formulation

The DTC dynamics follow the modified master equation:

\$[\frac{d\rho}{dt}= -i[H,\rho] + \sum_k \gamma_k D[L_k]\rho + \Gamma_{\text{trigger}}(\rho)\sum_n D[P_n]\rho\]$

The collapse trigger activates when coherence drops below the threshold:

$\[\Gamma_{\text{trigger}}(\rho)= \Gamma_0 \, \Theta(C_{\mathrm{irr}} - C(\rho))\]$

Coherence is quantified by:

$\[C(\rho) = \sqrt{1 - \mathrm{Tr}(\rho^2)}\]$

Pointer states $\( P_n \)$ correspond to a spatial grid, selected by environmental scattering physics.




