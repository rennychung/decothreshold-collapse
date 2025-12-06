# dtc_cat_test_FINAL_GUARANTEED_EXIT.py
# FIX: Cleaned up hidden nonprintable characters that caused the "invalid nonprintable character" error.
# Also ensures the correct exponential decay and snap behavior is maintained.

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import matplotlib.patches as mpatches

# --- 1. ROBUST MATPLOTLIB BACKEND SETUP ---
try:
    import matplotlib
    matplotlib.use('Agg') # Non-interactive backend for file saving
except Exception:
    pass

# === PARAMETERS ===
Delta_x = 100e-9            # 100 nm separation
sigma_x = 5e-9              # packet width
gamma_env = 1e4             # decoherence rate (s^-1)
C_th = 1e-20                # DTC threshold

# CALCULATED DECOHERENCE RATE: Gamma = 10^6 s^-1. Snap time ≈ 46 µs.
t_final = 200e-6 # Set to 200 µs to capture the 46 µs snap point
steps = 12000
times = np.linspace(0, t_final, steps)
dt = times[1]-times[0]

# === POSITION GRID ===
x = np.linspace(-400e-9, 400e-9, 2000)
dx = x[1] - x[0]

# === INITIAL STATE SETUP ===
psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))
psi_L /= np.sqrt(np.sum(np.abs(psi_L)**2) * dx)
psi_R /= np.sqrt(np.sum(np.abs(psi_R)**2) * dx)
psi_cat = (psi_L + psi_R) / np.sqrt(2)

# === COHERENCE FUNCTION (Used only for initial state C(0) and final state C_dtc) ===
def coh(psi):
    # Approximation for coherence C(t) = 2|ρ_LR|
    rho = np.outer(psi, psi.conj())
    # Return 2 * |Off-diagonal coherence term| (Approximation)
    return np.sum(np.abs(rho - np.diag(np.diag(rho)))) * dx

# === DTC SIMULATION ===
print("\n[STARTING] Running DTC Simulation...")
sys.stdout.flush()

# --- CORE SIMULATION LOGIC ---
psi = psi_cat.copy()
# Start all coherence tracking from 1.0 for a clean exponential decay plot
C_dtc_track = [1.0]
C_deco_track = [1.0]
triggered = False
t_trigger = None

# Correct decay rate is Gamma = gamma_env * (Delta_x / 2sigma_x)^2
Gamma_deco = gamma_env * (Delta_x**2) / (4*sigma_x**2)
decay_factor = np.exp(-Gamma_deco * dt)

try:
    for i in range(1, steps):
        # 1. Pure Decoherence step
        C_deco_next = C_deco_track[-1] * decay_factor
        
        # 2. DTC logic
        if not triggered:
            C_dtc_next = C_deco_next
            if C_dtc_next < C_th:
                # INSTANT COLLAPSE TRIGGERED
                psi = psi_L if np.random.rand() < 0.5 else psi_R # Collapse to L or R
                triggered = True
                t_trigger = times[i]
                C_dtc_next = 1e-40 # Instant drop to near zero for plot visibility
        else:
            # DTC is already triggered
            C_dtc_next = 1e-40

        C_dtc_track.append(C_dtc_next)
        C_deco_track.append(C_deco_next)

    print("[100%] Simulation complete.")
    sys.stdout.flush()

    # --- RESULT SUMMARY PRINT ---
    print("\n==============================================")
    print("Simulation Key Results (Calculations Completed):")
    print(f"Decoherence Threshold (C_th): {C_th:.1e}")
    print(f"Decoherence Rate (Gamma_deco): {Gamma_deco:.2e} s^-1")
    if t_trigger:
        print(f"✅ DTC Collapse Triggered at t = {t_trigger*1e6:.1f} µs")
    else:
        print("❌ Collapse not triggered within the time frame.")
    print("==============================================")
    
    simulation_success = True
    
except Exception as sim_e:
    print(f"❌ SIMULATION FAILED: {sim_e}")
    simulation_success = False


# === PLOT GENERATION (Only attempt if simulation succeeded) ===
if simulation_success:
    print("\n[NEXT STEP] Generating plots and saving files...")
    sys.stdout.flush()
    
    try:
        plt.figure(figsize=(11, 8))
        
        # --- SUBPLOT 1: FINAL STATE ---
        plt.subplot(2,1,1)
        plt.plot(x*1e9, np.abs(psi_cat)**2, 'k--', lw=2, label='Initial Cat State (Superposition)')
        psi_final = psi if triggered else psi_cat
        
        # Plot only the final state (which should be one localized peak)
        plt.plot(x*1e9, np.abs(psi_final)**2, 'red', lw=3, label='DTC Final State (Collapsed)')
        
        plt.xlabel('Position (nm)')
        plt.ylabel(r'$|\psi(x)|^2$')
        plt.title('DTC: Instant Tail-Free Collapse of Macroscopic Cat State')
        plt.legend(loc='upper right')
        plt.grid(alpha=0.3)

        # --- SUBPLOT 2: COHERENCE DECAY ---
        plt.subplot(2,1,2)
        plt.semilogy(times*1e6, C_dtc_track, 'blue', lw=3, label='DTC Coherence (Instant Pruning)')
        plt.semilogy(times*1e6, C_deco_track, 'gray', lw=2, ls='--', label='Pure Decoherence (Exponential Decay)')
        plt.axhline(C_th, color='orange', ls='--', lw=2, label=r'$C_{\rm th}=10^{-20}$')
        
        if t_trigger:
            plt.axvline(t_trigger*1e6, color='red', ls=':', lw=3, label=f'Collapse at {t_trigger*1e6:.1f} µs')
            
        plt.ylim(1e-45, 2)
        plt.xlim(0, t_final*1e6)
        plt.xlabel('Time ($\mu$s)')
        plt.ylabel('Coherence $C(t)$')
        plt.legend(loc='upper right')
        plt.grid(True, which="both", ls="--", alpha=0.3)
        plt.tight_layout()
        
        # --- FILE SAVING ---
        print("💾 Saving files now...")
        sys.stdout.flush()
        plt.savefig('dtc_cat_test_RESULT.png', dpi=400)
        plt.savefig('dtc_cat_test_RESULT.pdf')
        file_success = True
        
    except Exception as plot_e:
        file_success = False
        print(f"❌ PLOTTING FAILED: {plot_e}")
        
    # === FINAL REPORT AND EXIT ===
    print("\n--- FINAL REPORT ---")
    if file_success:
        print("✅ SUCCESS: Plot saved. You can close the Python window now.")
    
    sys.exit()
