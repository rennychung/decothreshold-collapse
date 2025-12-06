import matplotlib
# Switching to 'Qt5Agg' backend. You may need to run: pip install PyQt5
# If this still doesn't work, revert to 'TkAgg' or check the saved file.
matplotlib.use('Qt5Agg') 
import numpy as np
import matplotlib.pyplot as plt

# === REALISTIC 2025–2030 PARAMETERS (DTC Cat State Simulation) ===
mass = 1e-16                    # kg → ~100 nm silica sphere
Delta_x = 100e-9                # 100 nm spatial cat state
sigma_x = 5e-9                  # ground-state width
gamma_env = 1e4                 # s⁻¹ — environmental decoherence rate
C_th = 1e-20                    # DTC irreversibility threshold

# === TIME GRID ===
t_final = 0.15                  # seconds
steps = 12000
times = np.linspace(0, t_final, steps)
dt = times[1] - times[0]

# === INITIAL CAT STATE (Superposition of two localized Gaussians) ===
x = np.linspace(-400e-9, 400e-9, 1600)
dx = x[1] - x[0]
psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))
psi_cat = (psi_L + psi_R)
norm = np.sqrt(np.sum(np.abs(psi_cat)**2) * dx)
psi_cat /= norm

# === COHERENCE FUNCTION ===
def coherence(psi):
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
    
    decay_factor = np.exp(-gamma_env * (Delta_x**2) * dt / (4*sigma_x**2))
    
    for i in range(1, steps):
        C *= decay_factor
        
        if not triggered and C < C_th: 
            psi_L_norm = psi_L / np.linalg.norm(psi_L)
            psi_R_norm = psi_R / np.linalg.norm(psi_R)
            
            # Randomly select Left or Right outcome
            if np.random.rand() < 0.5:
                psi = psi_L_norm
            else:
                psi = psi_R_norm
            
            triggered = True
            
        psi_hist.append(psi.copy())
        C_hist.append(coherence(psi) if triggered else C) 
        
    return psi_hist, C_hist, triggered

# === SIMULATION 2: Pure Decoherence (No Collapse/Pruning) ===
def run_pure_decoherence():
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
for t, c in zip(times, C_deco):
    if c < C_th:
        t_trig = t
        break

# === PLOT THE RESULTS ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# AXIS 1: Final Position Probability Distribution
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
# Saving to a simple PNG file in the current working directory
plt.savefig('dtc_macroscopic_cat_test.png', dpi=300) 
plt.show()
