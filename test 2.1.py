# dtc_real_time_weak_measurement_FIXED.py
# The ULTIMATE test: continuous weak measurement of a qubit/cat state
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# --- 1. ROBUST MATPLOTLIB BACKEND SETUP ---
try:
    import matplotlib
    matplotlib.use('Agg') # Use Agg for guaranteed file saving
except Exception:
    pass

# === REALISTIC 2025 PARAMETERS ===
gamma_env = 1e5          # s^-1 — decoherence rate (real transmon: 10^4–10^6 s^-1)
C_th = 1e-20             # DTC irreversibility threshold
Gamma_0 = 1e25           # s^-1 — effectively infinite pruning (instant)

t_final = 1.0 / gamma_env * 3   # 3 decoherence times
steps = 20000
dt = t_final / steps
times = np.linspace(0, t_final, steps)

# === INITIAL SUPERPOSITION STATE ===
# Use complex initial state to correctly handle complex number evolution in CSL
psi0 = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2) 
rho = np.outer(psi0, psi0.conj())

# === PROJECTORS ===
P0 = np.array([[1, 0], [0, 0]], dtype=complex)
P1 = np.array([[0, 0], [0, 1]], dtype=complex)

# === COHERENCE FUNCTION ===
def coherence(rho):
    # Coherence is defined as 2 * |off-diagonal element|
    return 2 * np.abs(rho[0,1])

# === THREE SIMULATIONS ===
def run_dtc():
    rho = np.outer(psi0, psi0.conj())
    C_hist = [coherence(rho)]
    triggered = False
    t_trigger = None
    
    for i in range(1, steps):
        C = coherence(rho)
        
        # Environmental decoherence (pure dephasing)
        rho[0,1] *= np.exp(-gamma_env * dt)
        rho[1,0] = np.conj(rho[0,1])
        
        # DTC pruning trigger
        if not triggered and C < C_th:
            # Instant projection to |0⟩ or |1⟩
            if np.random.rand() < 0.5:
                rho = P0
            else:
                rho = P1
            triggered = True
            t_trigger = times[i]
        
        C_hist.append(coherence(rho))
    
    return C_hist, t_trigger

def run_csl_noise():
    # Simulate CSL: continuous stochastic noise on off-diagonal
    rho = np.outer(psi0, psi0.conj())
    C_hist = [coherence(rho)]
    # noise_strength is applied to the phase
    noise_strength = 1e-8
    
    for i in range(1, steps):
        # Apply environmental decay and CSL stochastic phase noise
        # This handles the ComplexWarning by ensuring the result is complex
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
print("[STARTING] Running real-time collapse simulations...")
sys.stdout.flush()

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
    # --- FIX APPLIED HERE: USED RAW STRING r'...' ---
    plt.ylabel(r'Coherence $C(t) = 2|\rho_{12}(t)|$')
    plt.title('Real-Time Weak Measurement Test of DTC\n(Superconducting Qubit or Levitated Oscillator)')
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.tight_layout() # This should no longer crash

    # === SAVE FILES ===
    plt.savefig('dtc_real_time_test.png', dpi=400)
    plt.savefig('dtc_real_time_test.pdf')
    file_success = True

except Exception as e:
    file_success = False
    print(f"\n[CRITICAL PLOTTING ERROR]: {e}")
    sys.stdout.flush()

# === FINAL DIAGNOSTIC AND EXIT ===
print("\n==============================================")
if t_trig and file_success:
    print(f"✅ Simulation SUCCESS: DTC collapse triggered at t = {t_trig*1e6:.2f} μs")
    print("💾 Plot files saved as dtc_real_time_test.png/pdf.")
else:
    print("❌ Simulation FAILED or files were not saved.")
print("==============================================")

sys.exit() # Exit immediately to avoid hanging
