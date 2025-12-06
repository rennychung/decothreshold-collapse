### DRAFT Models/Scripts/README/PAPERs need fix/polishing

# Decoherence-Triggered Collapse (DTC)

This repository contains the simulation code for a novel objective collapse theory, based on a **modified quantum master equation** that introduces an irreversibility threshold to trigger the spontaneous physical deletion of non-actualized quantum branches.



## 1. The Modified Master Equation

EDIT
The density operator $\rho$ evolves according to the following equation, which adds the **objective pruning collapse term** to the standard unitary and Lindblad evolution:

$$
\frac{d\rho}{dt} = -i[H,\rho] + \sum_k \gamma_k \mathcal{D}[L_k]\rho + \Gamma_{\text{trigger}}(\rho) \sum_n \mathcal{D}[P_n]\rho
$$

where the Lindblad dissipator is defined in standard form as

$$
\mathcal{D}[A]\rho \equiv A\rho A^\dagger - \frac{1}{2}\{A^\dagger A,\rho\}
$$

where:
- $H$ is the system Hamiltonian.
- $\{L_k\}$ are the usual Lindblad operators describing environmental decoherence, with rates $\gamma_k \ge 0$.
- $\{P_n = |n\rangle\langle n|\}$ are orthogonal projectors onto the **pointer basis** selected by the environment, satisfying $\sum_n P_n = \mathbf{1}$.
- $C(\rho) = \sum_{i \neq j} |\rho_{ij}|$ (or equivalent $l_1$-norm) measures total off-diagonal coherence.
- $C_{\rm th} \approx 10^{-20}$ is the **irreversibility threshold** derived from quantum Darwinism (Zurek, 2003).
- $\Theta(x)$ is the Heaviside step function.
- $\Gamma_0 \to \infty$ (or $\Gamma_0 \gtrsim 10^{25}~\text{s}^{-1}$ in finite-rate numerical implementations) ensures **instantaneous pruning** the moment coherence falls below $C_{\rm th}$.


## 2. The Coherence Measure and Trigger Rate

The pruning term activates only when the coherence in the pointer basis falls below a critical irreversibility threshold, $C_{\text{th}}$.

### Trigger Rate

The ideal trigger rate, $\Gamma_{\text{trigger}}(\rho)$, is a sharp, Heaviside switch:

$$
\Gamma_{\text{trigger}}(\rho) = \Gamma_0 \cdot \Theta\bigl(C_{\text{th}} - C(\rho)\bigr)
$$

with the maximum pruning rate $\Gamma_0 \to \infty$ (ideal sharp pruning).

For smooth numerical approximations, the formula uses a logistic function where $\kappa \to \infty$.

### Coherence Measure $C(\rho)$

The function $C(\rho)$ is the coherence measure used in the trigger:

**1. Conceptual Coherence (L¹-Norm, Exact Measure):**

    C_l1(ρ) ≡ Σ_{n ≠ m} |⟨n|ρ|m⟩|   (l¹-norm of off-diagonal elements)

**2. Operational Trigger Function (Purity Proxy):**

    C(ρ) ≡ sqrt[1 − Tr(ρ²)]   (purity proxy, monotonic with l¹ in the decoherence-dominated regime)

(purity proxy, monotonic with $l^1$ in the decoherence-dominated regime)

In realistic measurement processes, environmental decoherence ensures $C_{l1}(\rho)$ and the purity proxy vanish simultaneously (up to negligible corrections), allowing the purity proxy to be the preferred operational definition.



## 3. Fundamental Parameters of the Theory

| Parameter    | Physical Meaning                                    | Realistic Value             | Renny’s Choice (Ideal)          |
| :----------- | :-------------------------------------------------- | :-------------------------- | :------------------------------ |
| $\Gamma_0$   | Maximum pruning rate (collapse speed once triggered)| $\ge 10^{20} \text{ s}^{-1}$ (instantaneous) | $\infty$ (ideal sharp switch)   |
| $C_\text{th}$| Irreversibility threshold                           | $\sim 10^{-20} \text{ -- } 10^{-15}$ | $10^{-20}$                      |
| $\kappa$     | Steepness of the switch (smooth approximation)      | $> 10^{20}$                 | $\infty$ (ideal sharp switch)   |



## 4. Key Theorems and Consequences

| Theorem              | Mechanism and Outcome                                                                                           | Significance                                                                                   |
| :------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| **Microscopic Systems**     | For isolated systems ($\gamma_k \approx 0$), $C(\rho)$ never drops below $C_{\text{th}}$ so $\Gamma_{\text{trigger}} = 0$ forever. | Perfectly unitary evolution and zero collapse noise, fully recovering standard QM in the microscopic regime (stronger than GRW/CSL). |
| **Macroscopic Measurement** | Strong decoherence causes $C(\rho) \to 0$ in $< 10^{-15} \text{ s}$ so $\Gamma_{\text{trigger}} \to \infty$.                     | One definite outcome is selected, and other branches are physically deleted immediately after irreversibility.                        |
| **Born Rule**               | Probability of jumping to state $n$ is $\mathrm{Tr}(P_n \rho P_n)$ immediately before trigger.            | The standard probability rule is recovered because the system is already diagonalized in the pointer basis by environmental decoherence. |
| **No Superluminal Signaling** | Collapse only occurs *after* branches are irreversibly separated (orthogonality is established).         | Guarantees consistency with relativity and energy conservation.                                                                        |
| **Simulation Efficiency**   | The threshold provides an optimal lazy-evaluation strategy, allowing a simulator to free the memory of all non-actualized branches the instant $C(\rho) < C_{\text{th}}$. | A direct application for resource-bounded simulation of quantum systems.                                                              |



## 5. Code & Usage

- **Requirements:** Python 3, NumPy, Matplotlib

## 6. Figures

This section illustrates the core simulation results that define the **Decoherence-Triggered Instant Pruning (DTC)** model.

### Figure 1: Objective Bifurcation (Double-Slit Trajectories)

This plot shows Monte Carlo trajectories for a quantum particle under the DTC model. Superposition persists until the trigger is activated, resulting in an instantaneous, tail-free jump to a single classical path.

![Monte Carlo trajectories under DTC showing superposition followed by instantaneous collapse.](figures/figure1_double_slit_trajectories.png)

### Figure 2: Coherence Collapse

This figure demonstrates the smooth decay of coherence due to decoherence, which instantly triggers the pruning term ($\Gamma_0 \to \infty$) when the state hits the Irreversibility Threshold ($C_{\text{th}}$).

![Time evolution of off-diagonal coherence C(ρ) showing the smooth decay followed by a vertical, objective collapse.](figures/figure2_density_matrix_coherence.png)

### Figure 3: Theoretical Bounds and Parameter Space

The DTC theory relies on the irreversibility threshold ($C_{\text{th}}$) and the maximum pruning rate ($\Gamma_0$). The plot below illustrates the allowed parameter space, confirming that the microscopic regime is safely separated from the instantaneous collapse regime.

![Plot showing the theoretical boundaries and required constraints on the C_th and Gamma_0 parameter space for the DTC theory.](figures/figure3_parameter_space.png)

### Figure 4: 
## 7. Philosophical Summary
Objective collapse, in this framework, is not driven by consciousness, gravitational mass, or spontaneous stochastic fluctuations.
Rather, collapse is triggered exclusively by the information-theoretic criterion that all alternative quantum outcomes—except the actualized one—have become irreversibly inaccessible to the entire future universe.
That is, collapse is a consequence of the objective, physical loss of coherence between branches. Specifically, when the off-diagonal elements of the system’s density matrix in the pointer basis have been suppressed below any threshold recoverable by physical processes—even in principle—the deletion of non-actualized branches is both theoretically justified and operationally necessary.
On this view, the wave function does not represent a multitude of equally real worlds. Instead, it encodes a single world: one that comprises both the actual and the possible, up until the point when irreversibility renders the alternatives no longer physically meaningful.

## 8. License
This project is licensed under the MIT License.
See LICENSE for details.

## 9. Citation
If you use this code or theory, please cite:

Renny Chung, "Decoherence-Triggered Instant Pruning: A Simulation-Efficient Objective Collapse Model" (2025).

## 10. Contact
Questions, suggestions, or feedback?
Open an issue or email renny.chung.physics@gmail.com.

## 11. Topics
quantum-physics • decoherence • objective-collapse • open-quantum-systems • simulation • python • reproducible-research

This repository is intended as the canonical reference for Renny’s DTC theory. The model is presented in its complete form, and no additional ingredients are proposed.

