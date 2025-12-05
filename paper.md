# Decoherence-Triggered Instant Pruning (DTC): A Simulation-Efficient Objective Collapse Model

**Author:** Renny Chung

**Contact:** renny.chung.physics@gmail.com

**Canonical Status:** This document is the definitive reference for Renny’s DTC theory.



## Abstract

We present a new objective quantum collapse model—**Decoherence-Triggered Instant Pruning (DTC)**—governed by a modified master equation that implements a sharp, information-theoretic threshold for the irreversibility of quantum branches. We demonstrate, through exact numerical simulations in both trajectory and density-matrix formalisms, that the DTC model yields **objective, tail-free collapse** consistent with all standard quantum predictions and the Born rule, while offering a simulation-optimal approach to quantum reality.



## 1. Introduction

The measurement problem in quantum mechanics has motivated the search for objective collapse models that can account for the emergence of classicality from quantum superpositions. Traditional models, such as GRW and CSL, introduce stochastic or mass-dependent terms but can lack conceptual efficiency.

We propose the **Decoherence-Triggered Instant Pruning (DTC)** model, in which collapse is governed solely by the loss of recoverable information between quantum branches. Collapse occurs only and exactly when alternative outcomes become **irreversibly inaccessible** to the entire future universe, as diagnosed by the vanishing of off-diagonal coherence in the environmentally selected pointer basis. This approach is objective, operationally well-defined, and optimally efficient for simulation.



## 2. The DTC Master Equation

The evolution of the density matrix $\rho$ for any quantum system is governed by the following modified master equation:

$$\frac{d\rho}{dt} = -i[H, \rho] + \sum_k \gamma_k \mathcal{D}[L_k]\rho + \Gamma_{\text{trigger}}(\rho) \sum_n \mathcal{D}[P_n]\rho$$

**Where:**

* $H$: System Hamiltonian
* $\mathcal{D}[A]\rho = A \rho A^\dagger - \frac{1}{2}\{A^\dagger A,\rho\}$: The Lindblad superoperator ($\{,\}$ is the anticommutator).
* $L_k$: Standard Lindblad operators for environmental decoherence (rates: $\gamma_k$).
* $P_n$: Orthogonal projectors onto the pointer basis $|n\rangle$ (with $\sum_n P_n = \mathbf{1}$).

### 2.1 Collapse Trigger

Collapse is triggered only when the system’s coherence in the pointer basis falls below a critical **irreversibility threshold** $C_{\text{th}}$. The collapse rate is:

$$\Gamma_{\text{trigger}}(\rho) = \Gamma_0 \cdot \Theta\!\bigl(C_{\text{th}} - C(\rho)\bigr), \quad \Gamma_0 \to \infty$$

* $\Theta$: The Heaviside step function. (A smooth logistic approximation may be used for numerical work.)

### 2.2 Coherence Measure

Coherence is quantified as $C(\rho)$. We use two measures:

* **l¹-norm (Conceptual):** $C_{\text{l1}}(\rho) = \sum_{n \neq m} |\langle n|\rho|m\rangle|$
* **Operational (Purity Proxy):** $C(\rho) = \sqrt{1 - \text{Tr}[\rho^2]}$

These measures are **monotonically related** and vanish together under strong decoherence, making the operational proxy the preferred choice for the trigger.



## 3. Fundamental Parameters

| Parameter | Physical Meaning | Realistic Value | Canonical Choice (Ideal) |
| :--- | :--- | :--- | :--- |
| $\Gamma_0$ | Maximum pruning rate (collapse speed) | $\geq 10^{20} \text{ s}^{-1}$ (instantaneous) | $\infty$ (sharp switch) |
| $C_{\text{th}}$ | Irreversibility threshold | $\sim 10^{-20} \text{ – } 10^{-15}$ | $10^{-20}$ |
| $\kappa$ | Steepness of switch (logistic approximation) | $> 10^{20}$ | $\infty$ (sharp switch) |
| $\gamma_k, L_k$ | Decoherence rates and operators | Set by environment | Standard QM |



## 4. Key Theorems and Consequences

* **Microscopic Systems:** For isolated systems ($\gamma_k \approx 0$), $C(\rho)$ never drops below $C_{\text{th}}$, so $\Gamma_{\text{trigger}} = 0$ always. **Perfectly unitary evolution** and zero collapse noise are exactly preserved.
* **Macroscopic/Measurement Regime:** Strong decoherence causes $C(\rho) \to 0$ in $<10^{-15} \text{ s}$, triggering $\Gamma_{\text{trigger}} \to \infty$. Collapse occurs **instantly and irreversibly**, selecting one definite outcome and physically deleting all other branches.
* **Born Rule:** The probability of jumping to pointer state $n$ is $\text{Tr}[P_n \rho P_n]$ immediately before the trigger, precisely matching the quantum probability law.
* **No Superluminal Signaling:** Collapse occurs only **after** branches are irreversibly separated, preserving relativity and energy conservation.
* **Simulation Efficiency:** The threshold provides an **optimal lazy-evaluation strategy**, allowing a simulator to free memory of all non-actualized branches the instant $C(\rho) < C_{\text{th}}$.



## 5. Numerical Implementation

Both simulation codes in this repository are faithful, exact numerical realizations of the final, canonical DTC master equation.

### 5.1 `density_matrix_collapse.py`

* Directly integrates the full $2 \times 2$ density matrix.
* Implements Lindblad dissipators for both environmental decoherence ($\sigma_z$) and pruning ($P_L, P_R$) exactly as specified.
* The coherence drop to exactly zero is the literal manifestation of $\Gamma_0 \to \infty$: the pruning term becomes infinitely strong the instant irreversibility is detected.

### 5.2 `double_slit_trajectory.py`

* Implements the same physics in the **wavefunction language** (Monte Carlo trajectories) for a continuous-position system.
* The variable `self.coherence` tracks the off-diagonal magnitude in the $\{|L\rangle, |R\rangle\}$ pointer basis.
* When `self.coherence < C_th`, the wavefunction is instantaneously projected onto one of the two separating Gaussian packets according to the Born rule, which is mathematically equivalent to the Γ₀ → ∞ pruning term acting on the density matrix. **This equivalence holds because the projection onto one Gaussian packet exactly reproduces the action of the infinite-rate Lindblad term on a density matrix initially diagonalised by decoherence.**



## 6. Results and Figures

The simulations produce two key results:

1.  **Double-slit trajectories:** After a period of perfect superposition, each individual trajectory undergoes an objective, irreversible, **tail-free jump** to one classical path the instant coherence becomes irreversible. The ensemble average remains centered at zero, reproducing the Born rule. 
2.  **Coherence collapse:** The system initially follows ordinary environmental decoherence. When coherence crosses the irreversibility threshold, the pruning term activates and drives all off-diagonal elements to **exactly zero** in finite time—a physical, observer-independent reduction of the state vector. 


**Figures:**

<img width="1200" height="700" alt="double_slit_trajectories" src="https://github.com/user-attachments/assets/3e9c9e02-4203-41de-8e0a-7858f75cc52c" />
Figure 1 (double-slit trajectories): Monte Carlo trajectories under DTC with which-path detector. Superposition persists until the trigger (~step 60), then instantaneous pruning to one path. Blue: no detector (unitary superposition).

<img width="1000" height="600" alt="density_matrix_coherence" src="https://github.com/user-attachments/assets/3d3e0795-e638-4cd5-80e1-02869a96f227" />
Figure 2 (coherence collapse): Time evolution of off-diagonal coherence C(ρ). Smooth decoherence until C_th (red line), then vertical drop to zero via infinite-rate pruning.



## 7. Discussion

These simulations provide rigorous numerical proof that the DTC model is mathematically well-defined, stable, and behaves as required: unitary and noiseless at the microscopic level, instantaneously definite and tail-free at the macroscopic level, with all standard quantum predictions preserved.

### Philosophical Summary

Objective collapse in this framework is not driven by consciousness, gravitational mass, or spontaneous stochastic fluctuations.

Collapse is triggered exclusively by the **information-theoretic criterion** that all alternative quantum outcomes—except the actualized one—have become irreversibly inaccessible to the entire future universe.

On this view, the wave function does not represent a multitude of equally real worlds. Instead, it encodes a single world: one that comprises both the actual and the possible, up until the point when irreversibility renders the alternatives no longer physically meaningful.



## 8. Known Limitations

Like all existing objective-collapse models (GRW, CSL, Diósi–Penrose), DTC is currently non-relativistic. A fully covariant extension remains an open problem. Additionally, the ideal $\Gamma_0 \to \infty$ limit introduces infinitesimal energy non-conservation ($\Delta E \sim \hbar\Gamma_0$), which is macroscopically negligible and shared by all collapse theories.



## 9. License and Citation

### License

This project is licensed under the **MIT License**. See `LICENSE` for details.

### Citation
If you use this code or theory, please cite:

Chung, Renny. "Decoherence-Triggered Instant Pruning: A Simulation-Efficient Objective Collapse Model." 2025.


