# dtc_real_time_weak_measurement_EXTENDED_TIME.py
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# --- 1. ROBUST MATPLOTLIB BACKEND SETUP ---
try:
    import matplotlib
    matplotlib.use('Agg') 
except Exception:
    pass

# === PARAMETERS ===
gamma_env = 1e5          # s^-1
C_th = 1e-20             # DTC irreversibility threshold

# --- FIX APPLIED HERE: EXTENDED SIMULATION TIME ---
# Target time is ~4.6e-4 s. We set it to 5.0e-4 s (500 μs)
t_final = 5.0e-4 
steps = 15000 # Reduced steps slightly to offset longer time
dt = t_final / steps
times = np.linspace(0, t_final, steps)

# === INITIAL STATE SETUP ===
psi0 = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2) 
rho = np.outer(psi0, psi0.conj())
P0 = np.array([[1, 0], [0, 0]], dtype=complex)
P1 = np.array([[0, 0], [0, 1]], dtype=complex)

def coherence(rho):
    return 2 * np.abs(rho[0,1])

def run_dtc():
    rho = np.outer(psi0, psi0.conj())
    C_hist = [coherence(rho)]
    triggered = False
    t_trigger = None
    for i in range(1, steps):
        C = coherence(rho)
        rho[0,1] *= np.exp(-gamma_env * dt)
        rho[1,0] = np.conj(rho[0,1])
        if not triggered and C < C_th:
            if np.random.rand() < 0.5:
                rho = P0
            else:
                rho = P1
            triggered = True
            t_trigger = times[i]
        C_hist.append(coherence(rho))
    return C_hist, t_trigger

def run_csl_noise():
    rho = np.outer(psi0, psi0.conj())
    C_hist = [coherence(rho)]
    noise_strength = 1e-8
    for i in range(1, steps):
        rho[0,1] *= np.exp(-gamma_env * dt) * np.exp(1j * noise_strength * np.random.randn())
        rho[1,0] = np.conj(rho[0,1])
        C_hist.append(coherence(rho))
    return C_hist

def run_pure_deco():
    C = 1.0
    C_hist = [C]
    for i in range(1, steps):
        C *= np.exp(-gamma_env * dt)
        C_hist.append(C)
    return C_hist

# === RUN SIMULATIONS ===
print("[STARTING] Running real-time collapse simulations (500 μs)...")
sys.stdout.flush()
t_trig = None
file_success = False

try:
    C_dtc, t_trig = run_dtc()
    C_csl = run_csl_noise()
    C_deco = run_pure_deco()
    
    print("[COMPLETE] Simulation finished. Starting plotting...")
    sys.stdout.flush()

    # === PLOT GENERATION ===
    plt.figure(figsize=(10, 6))
    plt.semilogy(times*1e6, C_deco, 'gray', lw=2, label='Pure decoherence (standard QM)')
    plt.semilogy(times*1e6, C_csl, 'green', alpha=0.8, lw=2, label='CSL/GRW (stochastic noise)')
    plt.semilogy(times*1e6, C_dtc, 'red', lw=4, label='DTC (instant pruning)')

    plt.axhline(C_th, color='orange', ls='--', lw=2, label=r'$C_{\rm th} = 10^{-20}$')
    if t_trig:
        plt.axvline(t_trig*1e6, color='red', ls=':', lw=3, label=f'DTC collapse at {t_trig*1e6:.1f} μs')

    plt.xlabel('Time (μs)')
    plt.ylabel(r'Coherence $C(t) = 2|\rho_{12}(t)|$') 
    plt.title('Real-Time Weak Measurement Test of DTC\n(Superconducting Qubit or Levitated Oscillator)')
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.tight_layout()

    # === SAVE FILES ===
    plt.savefig('dtc_real_time_test.png', dpi=400)
    plt.savefig('dtc_real_time_test.pdf')
    file_success = True

except Exception as e:
    # --- ERROR EXPOSED HERE ---
    print(f"\n[CRITICAL PLOTTING ERROR DETAILS]: {e}")
    sys.stdout.flush()
    # Ensure t_trig is printed in the final summary even on plot failure
    
# === FINAL DIAGNOSTIC AND EXIT ===
print("\n==============================================")
if t_trig and file_success:
    print(f"✅ Simulation SUCCESS: DTC collapse triggered at t = {t_trig*1e6:.2f} μs")
    print("💾 Plot files saved as dtc_real_time_test.png/pdf.")
elif t_trig:
    print(f"❌ Plotting/Saving FAILED, but Collapse calculated at {t_trig*1e6:.2f} μs.")
else:
     print("❌ Simulation FAILED (Collapse never triggered in the extended time frame).")
print("==============================================")

sys.exit()
