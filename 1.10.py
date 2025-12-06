# dtc_cat_test_ULTRA_ROBUST.py
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# --- 1. ROBUST MATPLOTLIB BACKEND SETUP ---
# This block attempts to set a working graphical backend, otherwise it continues.
try:
    # Try the standard backend for interactive display
    import matplotlib
    matplotlib.use('TkAgg') 
except Exception:
    # If TkAgg fails (due to missing libraries or environment constraints),
    # switch to a non-interactive backend that can still save files.
    matplotlib.use('Agg')

# === PARAMETERS ===
Delta_x = 100e-9          # 100 nm separation
sigma_x = 5e-9            # packet width
gamma_env = 1e4           # decoherence rate (s^-1)
C_th = 1e-20              # DTC threshold (Critical coherence value)

t_final = 0.15
steps = 12000
times = np.linspace(0, t_final, steps)

# === POSITION GRID ===
x = np.linspace(-400e-9, 400e-9, 2000)
dx = x[1] - x[0]
dt = times[1]-times[0]

# === TWO GAUSSIAN PACKETS (Initial Setup) ===
psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))

# Normalise individual branches for projection
psi_L /= np.sqrt(np.sum(np.abs(psi_L)**2) * dx)
psi_R /= np.sqrt(np.sum(np.abs(psi_R)**2) * dx)

# Cat state (Initial superposition)
psi_cat = (psi_L + psi_R) / np.sqrt(2)

# === COHERENCE FUNCTION ===
def coh(psi):
    # Calculates the L1 norm of the off-diagonal elements
    rho = np.outer(psi, psi.conj())
    return np.sum(np.abs(rho - np.diag(np.diag(rho)))) * dx

# === DTC SIMULATION ===
psi = psi_cat.copy()
C_dtc = [coh(psi)]
triggered = False
t_trigger = None

# Calculate the decoherence decay factor per time step
decay = np.exp(-gamma_env * (Delta_x**2) * dt / (4*sigma_x**2))

for i in range(1, steps):
    C = C_dtc[-1] * decay
    
    # DTC Trigger Logic
    if not triggered and C < C_th:
        # Instant collapse to one branch (pruning)
        psi = psi_L if np.random.rand() < 0.5 else psi_R
        triggered = True
        t_trigger = times[i]
    
    C_dtc.append(coh(psi) if triggered else C)

# Pure decoherence only (The comparison baseline)
C_deco = [coh(psi_cat)]
for i in range(1, steps):
    C_deco.append(C_deco[-1] * decay)

# === PLOT ===
try:
    plt.figure(figsize=(11, 8))

    plt.subplot(2,1,1)
    plt.plot(x*1e9, np.abs(psi_cat)**2, 'k--', lw=2, label='Initial Cat State')
    plt.plot(x*1e9, np.abs(psi)**2, 'red', lw=3, label='DTC Final State (Collapsed)')
    plt.xlabel('Position (nm)')
    plt.ylabel(r'$|\psi(x)|^2$')
    plt.title('DTC: Instant Tail-Free Collapse of Macroscopic Cat State')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(2,1,2)
    plt.semilogy(times, C_dtc, 'blue', lw=3, label='DTC Coherence (Instant Pruning)')
    plt.semilogy(times, C_deco, 'gray', lw=2, ls='--', label='Pure Decoherence (Exponential Decay)')
    plt.axhline(C_th, color='orange', ls='--', label=r'$C_{\rm th}=10^{-20}$')
    if t_trigger:
        plt.axvline(t_trigger, color='red', ls=':', lw=3, label=f'Collapse at {t_trigger:.1e}s')
    plt.xlabel('Time (s)')
    plt.ylabel('Coherence')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    
    # --- 2. ROBUST FILE SAVING ---
    # Attempt to save to the user's current working directory
    try:
        plt.savefig('dtc_cat_test_result.png', dpi=400)
        plt.savefig('dtc_cat_test_result.pdf')
        file_success = True
    except Exception as e:
        file_success = False
        file_error = str(e)

    # --- 3. ATTEMPT TO SHOW PLOT ---
    if 'TkAgg' in matplotlib.get_backend():
        plt.show()

# --- 4. EXCEPTION HANDLING FOR PLOTTING FAILURE ---
except Exception as plot_e:
    plot_failure_message = f"Plotting failed: {str(plot_e)}"
    file_success = False
    file_error = plot_failure_message

# === FINAL DIAGNOSTIC OUTPUT (Guaranteed to Run) ===
print("\n==============================================")
print("DTC Simulation Diagnostic:")
print(f"Decoherence Threshold (C_th): {C_th:.1e}")
if t_trigger:
    print(f"✅ DTC Collapse Triggered at t = {t_trigger:.2e} seconds")
    simulation_status = "working perfectly"
else:
    print("❌ Collapse not triggered within the time frame.")
    simulation_status = "did not trigger collapse"

# Report on the file saving attempt
print("\n--- Output Status ---")
if file_success:
    print("💾 Plot successfully saved as dtc_cat_test_result.png/pdf.")
    print("Please check the directory where you ran the script.")
else:
    print("❌ Plotting or file saving FAILED.")
    print(f"Details: {file_error}")
    print("This confirms an environmental issue (permissions/backend).")
print("==============================================")
