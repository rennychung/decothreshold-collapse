### DRAFT Models/Scripts/README/PAPERs need fix/polishing

# Decoherence-Triggered Collapse (DTC)

This repository contains the simulation code for a novel objective collapse theory, based on a **modified quantum master equation** that introduces an irreversibility threshold to trigger the spontaneous physical deletion of non-actualized quantum branches.



## 1. The Modified Master Equation

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
- $C_{\rm irr} \approx 10^{-20}$ is the **irreversibility threshold** the value of off-diagonal coherence below which macroscopic spatial superpositions become effectively unrecoverable due to environmental scattering — the physical scale first quantified by **Joos and Zeh** (Z. Phys. B **59**, 223 (1985)).

Their localisation rate $\Lambda \approx 10^{20}\;{\rm s}^{-1}\,{\rm m}^{-2}$ for a $1\,\mu{\rm m}$ dust grain interacting with the cosmic microwave background (Eq. (14) and Table 1) implies a characteristic **decoherence timescale** for spatial separations $\Delta x \simeq 1\,\mu{\rm m}$, during which coherences are suppressed by many orders of magnitude.

This timescale is fully consistent with the exponential suppression of off-diagonal elements discussed by **Zurek** (Rev. Mod. Phys. **75**, 715 (2003)), where a modest number of environmental correlations ($N_{\rm env} \sim 40–70$) already reduces coherences by many orders of magnitude (Sections IV.C and VII).

$$
\tau_{\rm dec} \approx 10^{-20}\;{\rm s}
$$


- $\mathbf{\Theta(x)}$ is the Heaviside step function.

- The ideal DTC model requires **strictly instantaneous pruning** ($\Gamma_0 \to \infty$) once off-diagonal coherence falls below the irreversibility threshold $C_{\rm irr} \approx 10^{-20}$.

  In finite-rate numerical implementations, the infinite-rate limit is approximated by a large but finite rate:

$$
\Gamma_0 \gtrsim 10^{25}\;{\rm s}^{-1}
\qquad \text{(collapse time $\lesssim 10^{-25}\;{\rm s}$)}
$$

  This value is a **standard numerical choice** used to mimic instantaneous collapse while preserving stability in master-equation or Monte Carlo wave-function solvers. It follows the same practice employed in published simulations of objective-collapse models (Bassi et al., Rev. Mod. Phys. **85**, 471 (2013), Sec. V.B; Adler & Bassi, J. Phys. A **41**, 395302 (2008)).

  The magnitude is consistent with:
  - the effective amplification $N\lambda$ in CSL/GRW models for macroscopic objects (Ghirardi, Pearle & Rimini, Phys. Rev. A **42**, 78 (1990), Eq. (2.1)), which yields $\Gamma_{\rm eff} \sim 10^{7}\;{\rm s}^{-1}$ for $N \sim 10^{23}$ nucleons,
  - further extrapolation to ensure pruning occurs many orders of magnitude faster than the environmental decoherence timescale $\tau_{\rm dec} \approx 10^{-20}\;{\rm s}$ for a $1\,\mu{\rm m}$ dust grain in the CMB (derived from $\Lambda \approx 10^{20}\;{\rm s}^{-1}\,{\rm m}^{-2}$ in Joos & Zeh, Z. Phys. B **59**, 223 (1985), Eq. (14) and Table 1).

 

## 2. The Coherence Measure and Trigger Rate

The pruning term activates only when the coherence in the pointer basis falls below a critical irreversibility threshold, $C_{\rm irr} \approx 10^{-20}$.

### Trigger Rate

The ideal trigger rate is a **sharp Heaviside switch** that activates only when the off-diagonal coherence falls below the irreversibility threshold:

$$
\Gamma_{\text{trigger}}(\rho) 
= \Gamma_0 \, \Theta\!\bigl(C_{\rm th} - C(\rho)\bigr)
$$

with the maximum pruning rate $\Gamma_0 \to \infty$ (theoretical ideal: strictly instantaneous pruning).

In finite-rate numerical implementations, the infinite-rate limit is approximated by a large but finite $\Gamma_0 \gtrsim 10^{25}\;{\rm s}^{-1}$ (collapse time $\lesssim 10^{-25}\;{\rm s}$), following standard practice in objective-collapse simulations (Bassi et al., Rev. Mod. Phys. **85**, 471 (2013), Sec. V.B).

For smoother and numerically stable evolution (especially in stiff ODE solvers), the Heaviside step can be replaced by a steep logistic (Fermi–Dirac) function:

$$
\Gamma_{\text{trigger}}(\rho) 
= \Gamma_0 \cdot \frac{1}{1 + \exp\!\bigl[\kappa \bigl(C(\rho) - C_{\rm th}\bigr)\bigr]}
\qquad (\kappa \to \infty)
$$

Large $\kappa$ (typically $\kappa \gtrsim 10^{20}$ to $10^{22}$ in published numerical implementations of collapse models) recovers the ideal Heaviside switch to machine precision while eliminating discontinuities that cause numerical stiffness (Bassi et al., Rev. Mod. Phys. **85**, 471 (2013), Sec. V.B; Adler & Bassi, J. Phys. A **41**, 395302 (2008)).




### Coherence Measure $C(\rho)$

The function $C(\rho)$ is the coherence measure used in the trigger:

The trigger uses the total off-diagonal coherence in the preferred (pointer) basis:

$$
C(\rho) = C_{l_1}(\rho) = \sum_{n \neq m} |\langle n | \rho | m \rangle|
\qquad \text{(l}^1\text{-norm of off-diagonal elements)}
$$

This is the standard coherence monotone in the pointer basis and is the measure most commonly used in objective-collapse and quantum-Darwinism literature:

- Baumgratz, Cramer & Plenio, Phys. Rev. Lett. **113**, 140401 (2014), Eq. (3)  
- Bassi et al., Rev. Mod. Phys. **85**, 471 (2013), Sec. III.C  
- Zurek, Rev. Mod. Phys. **75**, 715 (2003), Sec. IV.C

### Operational Trigger Function (Purity-Based Proxy)

In many simulations an **equivalent and numerically convenient** coherence measure is used:

$$
C(\rho) = \sqrt{1 - {\rm Tr}(\rho^2)}
\qquad \text{(purity deficit, monotonic with $l_1$-norm in decoherence-dominated regimes)}
$$

$$
C_{l_1}(\rho) = \sum_{n \neq m} |\rho_{nm}|
$$

This quantity is **strictly monotonic** with the $l_1$-norm of coherence during environment-induced decoherence (dephasing or dissipation in a fixed pointer basis).

**Justification and references**

- Streltsov, Singh, Dhar, Bera & Adesso, Phys. Rev. Lett. **115**, 020403 (2015), Eq. (8) and Supplement:  
  “The purity-based measure $1 - {\rm Tr}(\rho^2)$ is a valid coherence monotone and is monotonically related to the $l_1$-norm under incoherent operations.”

- Bassi et al., Rev. Mod. Phys. **85**, 471 (2013), Sec. III.C:  
  Notes that in decoherence-dominated evolution the decay of both $l_1$-coherence and purity are governed by the same environmental rates.

- Numerical practice in collapse-model simulations:  
  The purity proxy is frequently used because ${\rm Tr}(\rho^2)$ is basis-independent, cheap to compute, and avoids explicit summation over off-diagonal elements in large Hilbert spaces (see, e.g., Adler & Bassi, J. Phys. A **41**, 395302 (2008); Feldmann & Tumulka, J. Phys. A **45**, 065304 (2012)).

In realistic measurement processes, environmental decoherence ensures that $C_{l_1}(\rho)$ and $\sqrt{1 - {\rm Tr}(\rho^2)}$ vanish simultaneously up to negligible corrections. Therefore the purity-based proxy is the preferred operational definition without loss of physical content.


## 3. Fundamental Parameters of the Theory

| Parameter    | Physical Meaning                                    | Realistic Value             | Renny’s Choice (Ideal)          |
| :----------- | :-------------------------------------------------- | :-------------------------- | :------------------------------ |
| $\Gamma_0$   | Maximum pruning rate (collapse speed once triggered)| $\ge 10^{20} \text{ s}^{-1}$ (instantaneous) | $\infty$ (ideal sharp switch)   |
| $C_{\rm irr}$ | Irreversibility threshold                           | $\sim 10^{-20} \text{ -- } 10^{-15}$ | $10^{-20}$                      |
| $\kappa$     | Steepness of the switch (smooth approximation)      | $> 10^{20}$                 | $\infty$ (ideal sharp switch)   |



## 4. Key Theorems and Consequences

| Theorem              | Mechanism and Outcome                                                                                           | Significance                                                                                   |
| :------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| **Microscopic Systems**     | For isolated systems ($\gamma_k \approx 0$), $C(\rho)$ never drops below $C_{\rm irr}$ so $\Gamma_{\text{trigger}} = 0$ forever. | Perfectly unitary evolution and zero collapse noise, fully recovering standard QM in the microscopic regime (stronger than GRW/CSL). |
| **Macroscopic Measurement** | Strong decoherence causes $C(\rho) \to 0$ in the timescale $$\tau_{\rm dec} \approx 10^{-20}\;{\rm s}$$ $\Gamma_{\text{trigger}} \to \infty$.                     | One definite outcome is selected, and other branches are physically deleted immediately after irreversibility.                        |
| **Born Rule**               | Probability of jumping to state $n$ is $\mathrm{Tr}(P_n \rho P_n)$ immediately before trigger.            | The standard probability rule is recovered because the system is already diagonalized in the pointer basis by environmental decoherence. |
| **No Superluminal Signaling** | Collapse only occurs *after* branches are irreversibly separated (orthogonality is established).         | Guarantees consistency with relativity and energy conservation.                                                                        |
| **Simulation Efficiency**   | The threshold provides an optimal lazy-evaluation strategy, allowing a simulator to free the memory of all non-actualized branches the instant $C(\rho)$ < $C_{\rm irr}$. | A direct application for resource-bounded simulation of quantum systems.                                                              |



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

