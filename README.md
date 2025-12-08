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
| **Macroscopic Measurement** | Strong decoherence causes $C(\rho) \to 0$ in the timescale $$\tau_{\rm dec} \approx 10^{-20}\;{\rm s}$$ $\Gamma_{\text{trigger}} \to \infty$. | One definite outcome is selected, and other branches are physically deleted immediately after irreversibility.|
| **Born Rule**               | Probability of jumping to state $n$ is $\mathrm{Tr}(P_n \rho P_n)$ immediately before trigger.| The standard probability rule is recovered because the system is already diagonalized in the pointer basis by environmental decoherence. |
| **No Superluminal Signaling** | Collapse only occurs *after* branches are irreversibly separated (orthogonality is established).| Guarantees consistency with relativity and energy conservation.                                                                      |
| **Simulation Efficiency**   | The threshold provides an optimal lazy-evaluation strategy, allowing a simulator to free the memory of all non-actualized branches the instant $C(\rho)$ < $C_{\rm irr}$. | A direct application for resource-bounded simulation of quantum systems. |                                                            


## 5. Code & Usage

- **Requirements:** Python 3, NumPy, Matplotlib

## 6. Figures

This section illustrates the core simulation results that define the **Decoherence-Triggered Instant Pruning (DTC)** model.

### Figure 1: Objective Bifurcation (Double-Slit Trajectories)

<img width="1200" height="700" alt="double_slit_trajectory" src="https://github.com/user-attachments/assets/08cdf420-1764-4255-a81b-0fe2c6385049" />


This plot shows Monte Carlo trajectories for a quantum particle under the DTC model. Superposition persists until the trigger is activated, resulting in an instantaneous, tail-free jump to a single classical path.

### Figure 2: Coherence Collapse
<img width="1000" height="600" alt="density_matrix_coherence" src="https://github.com/user-attachments/assets/53725933-24ab-40fa-8c8a-4c323c8824f2" />

This figure demonstrates the smooth decay of coherence due to decoherence, which instantly triggers the pruning term ($\Gamma_0 \to \infty$) when the state hits the Irreversibility Threshold ($C_{\text{th}}$).



### Figure 3: Theoretical Bounds and Parameter Space
<img width="640" height="480" alt="parameter_space" src="https://github.com/user-attachments/assets/6a5c1697-b70c-43df-9d46-4c3da102823e" />

The DTC theory relies on the irreversibility threshold ($C_{\text{th}}$) and the maximum pruning rate ($\Gamma_0$). The plot above illustrates the allowed parameter space, confirming that the microscopic regime is safely separated from the instantaneous collapse regime.


### Figure 4: coherence_decay_DTC

<img width="7119" height="4447" alt="dtc_vs_csl" src="https://github.com/user-attachments/assets/b20399ad-9b3b-42ed-8ff8-db70a22711aa" />

### Figure 5: dtc_cat_test



### Figure 6: lazarus_test
<img width="1100" height="650" alt="dtc_lazarus_test" src="https://github.com/user-attachments/assets/418b62b4-d958-42d2-9bdc-868891138ea0" />


### Figure 7: dtc_lisa

## 7. Philosophical Summary
The Decoherence-Triggered Collapse (DTC) model does not invoke consciousness, gravitational effects, or additional stochastic fields as the origin of wave-function collapse.  
Collapse arises exclusively from the physical process of environment-induced decoherence itself.

When off-diagonal coherence in the pointer basis is suppressed below the irreversibility threshold $C_{\rm irr} \approx 10^{-20}$ — a scale derived from the scattering rates of macroscopic objects with environmental photons and particles (Joos & Zeh, 1985; Zurek, 2003) — the non-actualized branches become inaccessible to all future physical interactions, even in principle. At that point the theory activates an infinitely sharp pruning term that instantaneously projects the state onto the pointer basis selected by the environment.

Consequently, the quantum state never describes a multitude of co-existing, equally real parallel worlds. Prior to the threshold, off-diagonal terms encode physically accessible superpositions; once the threshold is crossed, those terms lose all observable consequences and are legitimately removed from the description. The wave function thus represents a single ontological world that temporarily carries latent possibilities until environmental entanglement renders the alternatives irreversibly unrecoverable. Collapse is therefore not an extra postulate grafted onto quantum mechanics, but an objective dynamical consequence of the same irreversible decoherence process that already explains the quantum-to-classical transition.

## 8. Experimental and Testable Implications

The DTC model recovers exact standard quantum mechanics for all isolated or microscopically coherent systems because the trigger rate $\Gamma_{\text{trigger}}(\rho)$ remains strictly zero as long as $C(\rho) \gg C_{\rm irr} \approx 10^{-20}$. Collapse occurs only after environmental decoherence has already suppressed off-diagonal terms below the physical irreversibility threshold derived by Joos & Zeh (1985) and Zurek (2003).

This leads to sharp empirical distinctions from stochastic collapse models such as GRW and CSL, which introduce continuous, mass-dependent noise even in isolated systems (Bassi et al., Rev. Mod. Phys. **85**, 471 (2013) and subsequent updates):

- **No excess microscopic noise** — DTC predicts exactly zero additional decoherence, heating, or spontaneous radiation in low-mass systems, fully compatible with the tightest current bounds on CSL parameters ($\lambda \lesssim 10^{-11}\;{\rm s}^{-1}$ at $r_C = 10^{-7}\;{\rm m}$, Carlesso et al., Phys. Rev. Lett. **121**, 130401 (2018); Vinante et al., Phys. Rev. Lett. **125**, 100404 (2020)).
- **Sharper macroscopic localisation** — In large-spatial-superposition experiments (optomechanical systems, levitated nanoparticles, molecular interferometry), DTC produces an instantaneous, tail-free collapse once environmental decoherence crosses $C_{\rm irr}$, whereas CSL yields gradual, diffusion-like localisation.
- **No spontaneous X-ray emission or momentum diffusion** — Unlike CSL, DTC predicts zero collapse-induced radiation or heating in cryogenic cantilevers and space-borne test masses, consistent with LISA Pathfinder null results and projected LISA sensitivity (Armano et al., Phys. Rev. Lett. **131**, 231401 (2023)).

Ongoing non-interferometric tests (cantilever experiments, ultracold atoms, space-based detectors) and near-term matter-wave interferometry with massive molecules or nanoparticles can directly discriminate DTC’s environment-dependent, threshold-triggered collapse from CSL’s intrinsic, continuous noise (see reviews in Carlesso & Bassi, Phys. Rep. **1005**, 1 (2023); Donadi & Bassi, Phys. Rep. **1053**, 1 (2024)). Because DTC leverages the same irreversible decoherence rates already present in standard quantum mechanics, it remains consistent with all experiments to date while offering a falsifiable prediction: collapse events are strictly correlated with the moment environmental entanglement renders alternative outcomes physically unrecoverable.

## 9. Current Limitations and Open Questions

While the DTC model offers a parameter-free, environment-triggered collapse mechanism consistent with all existing experiments, several theoretical and practical limitations remain:

- **Relativistic generalisation** — The present formulation uses a non-relativistic Lindblad master equation with an explicit preferred pointer basis selected by the environment. A fully covariant version that respects locality and avoids superluminal signalling in multi-particle systems has not yet been constructed (cf. ongoing challenges for all objective collapse theories, Tumulka, 2023; Bassi et al., 2023).

- **Exact definition of the pointer basis in interacting field theories** — In realistic many-body systems the instantaneous eigenbasis of the interaction Hamiltonian is time-dependent and non-trivial. Numerical simulations in the repository use simplified or pre-defined pointer bases; a systematic, basis-independent formulation of the trigger remains under development.

- **Finite-rate numerical artefacts** — Ideal DTC requires $\Gamma_0 \to \infty$ and a perfect Heaviside switch. Real simulations use large but finite $\Gamma_0 \gtrsim 10^{25}\;{\rm s}^{-1}$ and a steep logistic function. These approximations are standard in the collapse-model literature (Bassi et al., Rev. Mod. Phys. **85**, 471 (2013)) and do not affect macroscopic predictions, but they slightly blur the exact moment of pruning.

- **Lack of direct experimental discrimination to date** — Because DTC activates only after environmental decoherence has already made branches irreversibly inaccessible, current matter-wave interferometers and optomechanical tests (which operate well above $C_{\rm irr}$) cannot yet distinguish DTC from standard quantum mechanics plus ordinary decoherence. Future experiments must probe the precise dynamics at or below the $10^{-20}$ coherence level (e.g. space-based molecular interferometry or kilometre-scale baselines).

- **Energy non-conservation at the instant of pruning** — The ideal infinite-rate limit violates energy conservation by an arbitrarily small amount for macroscopic objects (consistent with the uncertainty principle over $\sim 10^{-25}\;{\rm s}$). Regularised finite-rate versions restore strict conservation at the cost of a brief residual tail, exactly as in CSL and GRW implementations.


## 10. License
This project is licensed under the MIT License.
See LICENSE for details.

## 11. Citation
If you use this code or theory, please cite:

Renny Chung, "Decoherence-Triggered Instant Pruning: A Simulation-Efficient Objective Collapse Model" (2025).

## 12. Contact
Questions, suggestions, or feedback?
Open an issue or email renny.chung.physics@gmail.com.

## 13. Topics
quantum-physics • decoherence • objective-collapse • open-quantum-systems • simulation • python • reproducible-research

This repository is intended as the canonical reference for Renny’s DTC theory. The model is presented in its complete form, and no additional ingredients are proposed.

