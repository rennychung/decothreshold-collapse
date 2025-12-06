import matplotlib
# Use 'TkAgg' backend to force the plot window to display on most systems.
# If this doesn't work, try 'Qt5Agg' (may require 'pip install PyQt5').
matplotlib.use('TkAgg') 
import numpy as np
import matplotlib.pyplot as plt

# === REALISTIC 2025–2030 PARAMETERS (DTC Cat State Simulation) ===
# Parameters for a typical levitated nanosphere experiment.
mass = 1e-16                    # kg → ~100 nm silica sphere (m = 10^-16 kg)
Delta_x = 100e-9                # 100 nm spatial cat state (separation of the two peaks)
sigma_x = 5e-9                  # ground-state width of each peak
gamma_env = 1e4                 # s⁻¹ — environmental decoherence rate (calibrated gas/photon scattering)
C_th = 1e-20                    # DTC irreversibility threshold (The critical coherence value)

# === TIME GRID ===
t_final = 0.15                  # seconds — Total simulation time
steps = 12000
times = np.linspace(0, t_final, steps)
dt = times[1] - times[0]

# === INITIAL CAT STATE (Superposition of two localized Gaussians) ===
# Spatial grid (in meters)
x = np.linspace(-400e-9, 400e-9, 1600)
dx = x[1] - x[0]

# Two localized wave functions (Left and Right)
psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))

# Cat state (equal superposition)
psi_cat = (psi_L + psi_R)

# Normalize the initial cat state
norm = np.sqrt(np.sum(np.abs(psi_cat)**2) * dx)
psi_cat /= norm

# === COHERENCE FUNCTION (A simplified measure for a cat state) ===
def coherence(psi):
    # Proxy for the coherence C(rho) using the l¹-norm of the off-diagonals.
    rho = np.outer(psi, psi.conj())
    diag = np.diag(np.diag(rho))
    return np.sum(np.abs(rho - diag)) * dx

# === SIMULATION 1: DTC (Decoherence-Triggered Collapse) ===
def run_dtc():
    psi = psi_cat.copy()
    C = coherence(psi)
    psi_hist = [psi.copy()]
    C_hist = [C]
    triggered = False
    
    # Calculate the analytic exponential decay factor for the coherence
    decay_factor = np.exp(-gamma_env * (Delta_x**2) * dt / (4*sigma_x**2))
    
    for i in range(1, steps):
        # Apply environmental decoherence
        C *= decay_factor
        
        if not triggered and C < C_th: 
            # DTC TRIGGER: Instantaneous projection to one branch (the "snap")
            
            # Re-normalize the individual branches for projection
            psi_L_norm = psi_L / np.linalg.norm(psi_L)
            psi_R_norm = psi_R / np.linalg.norm(psi_R)
            
            # Randomly select Left or Right outcome
            if np.random.rand() < 0.5:
                psi = psi_L_norm
            else:
                psi = psi_R_norm
            
            triggered = True
            
        psi_hist.append(psi.copy())
        # If triggered, the coherence is instantly dropped.
        C_hist.append(coherence(psi) if triggered else C) 
        
    return psi_hist, C_hist, triggered

# === SIMULATION 2: Pure Decoherence (No Collapse/Pruning) ===
def run_pure_decoherence():
    # Coherence continues to decay smoothly (no collapse mechanism)
    C = coherence(psi_cat)
    C_hist = [C]
    decay_factor = np.exp(-gamma_env * (Delta_x**2) * dt / (4*sigma_x**2))
    
    for i in range(1, steps):
        C *= decay_factor
        C_hist.append(C)
    return C_hist

# Run the simulations
psi_dtc, C_dtc, triggered = run_dtc()
C_deco = run_pure_decoherence()

# Determine the time of the DTC trigger
t_trig = 0.0
# Find the exact time the pure decoherence curve crosses the threshold C_th
for t, c in zip(times, C_deco):
    if c < C_th:
        t_trig = t
        break

# === PLOT THE RESULTS ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# AXIS 1: Final Position Probability Distribution
# Use 'r' prefix for raw strings to avoid SyntaxWarning with LaTeX backslashes
ax1.plot(x*1e9, np.abs(psi_cat)**2, 'k--', lw=1.5, label=r'Initial Cat State ($|\psi_L + \psi_R|^2$)')
ax1.plot(x*1e9, np.abs(psi_dtc[-1])**2, 'red', lw=3, label='Final State (DTC) - Collapsed Outcome')
ax1.plot(x*1e9, np.abs(psi_L / np.linalg.norm(psi_L))**2, 'gray', alpha=0.5, lw=1)
ax1.plot(x*1e9, np.abs(psi_R / np.linalg.norm(psi_R))**2, 'gray', alpha=0.5, lw=1)
ax1.set_ylabel(r'$|\psi(x)|^2$')
ax1.set_xlabel('Position (nm)')
ax1.set_title(f'DTC Prediction: Cat State Collapse (Mass: {mass:.0e} kg)')
ax1.legend(loc='upper right')
ax1.grid(alpha=0.3)
ax1.set_xlim(-200, 200)

# AXIS 2: Coherence Loss Over Time
ax2.semilogy(times, C_dtc, 'blue', lw=3, label='DTC Coherence (Instant Collapse)')
ax2.semilogy(times, C_deco, 'gray', lw=2, ls='--', label='Pure Decoherence (Exponential Decay)')
ax2.axhline(C_th, color='orange', ls='--', lw=2, label=r'$C_{\rm th} = 10^{-20}$ (DTC Threshold)')

if triggered:
    ax2.axvline(t_trig, color='red', ls=':', lw=2, label=f'Instant Pruning at t≈{t_trig:.4f}s')

ax2.set_xlabel('Time (s)')
ax2.set_ylabel(r'Coherence $C(\rho)$ (log scale)')
ax2.legend()
ax2.grid(which='major', alpha=0.5)
ax2.grid(which='minor', alpha=0.1)

plt.tight_layout()
# The plot is saved to your script's directory:
plt.savefig('dtc_macroscopic_cat_test.pdf', dpi=300) 
plt.show() # Attempts to display the plot window
