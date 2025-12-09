# DTC_COMPARISON_PLOT_FIXED.py
# Generates Figure 2: Comparison of Asymptotic Decoherence vs. DTC State Reduction

import numpy as np
import matplotlib.pyplot as plt

# --- 1. Define the Physics Operators ---
sig_z = np.array([[1, 0], [0, -1]], dtype=complex)
P_L = np.array([[1, 0], [0, 0]], dtype=complex)
P_R = np.array([[0, 0], [0, 1]], dtype=complex)

def commutator(A, B):
    return np.dot(A, B) - np.dot(B, A)

def anti_commutator(A, B):
    return np.dot(A, B) + np.dot(B, A)

def lindblad_dissipator(P, rho):
    term1 = np.dot(P, np.dot(rho, P.conj().T))
    term2 = 0.5 * anti_commutator(np.dot(P.conj().T, P), rho)
    return term1 - term2

# --- 2. Simulation Parameters ---
dt = 0.005
steps = 3000
times = np.linspace(0, steps*dt, steps)

# Hamiltonian
H = 1.0 * sig_z

# Initial State: SUPERPOSITION (1/sqrt(2) * (|L> + |R>))
psi0 = np.array([[1], [1]], dtype=complex) / np.sqrt(2)
rho_dtc = np.dot(psi0, psi0.conj().T)
rho_qm = rho_dtc.copy() # Independent copy for Standard QM

# Parameters
gamma_decoherence = 0.3
coherence_threshold = 0.15 # C_irr
gamma_reduction_rate = 100.0 # High rate for rapid reduction

coherence_history_dtc = []
coherence_history_qm = []
snap_index = None

# --- 3. Time Evolution ---
for i, t in enumerate(times):
    # Calculate Coherence (Off-diagonal magnitude)
    coherence_dtc = np.abs(rho_dtc[0, 1]) + np.abs(rho_dtc[1, 0])
    coherence_qm = np.abs(rho_qm[0, 1]) + np.abs(rho_qm[1, 0])
    
    # --- DTC Logic: Threshold Check ---
    if coherence_dtc < coherence_threshold:
        current_gamma_red = gamma_reduction_rate
        if snap_index is None:
            snap_index = i
    else:
        current_gamma_red = 0.0
        
    # --- 1. DTC Evolution ---
    d_rho_unitary = -1j * commutator(H, rho_dtc)
    d_rho_env = gamma_decoherence * lindblad_dissipator(sig_z, rho_dtc)
    d_rho_reduction = current_gamma_red * (lindblad_dissipator(P_L, rho_dtc) + lindblad_dissipator(P_R, rho_dtc))
    
    d_rho_dtc_dt = d_rho_unitary + d_rho_env + d_rho_reduction
    rho_dtc = rho_dtc + d_rho_dtc_dt * dt
    
    # --- 2. QM Evolution (Decoherence Only) ---
    d_rho_qm_dt = -1j * commutator(H, rho_qm) + gamma_decoherence * lindblad_dissipator(sig_z, rho_qm)
    rho_qm = rho_qm + d_rho_qm_dt * dt
    
    coherence_history_dtc.append(coherence_dtc)
    coherence_history_qm.append(coherence_qm)

# --- 4. Plotting (Comparison) ---
plt.figure(figsize=(10, 6))

# Plot Pure Decoherence (QM) - Gray line
plt.plot(times, coherence_history_qm, color='gray', linestyle='--', linewidth=2, alpha=0.6,
         label='Asymptotic Decoherence (Standard QM)')

# Plot DTC Coherence - Blue line
plt.plot(times, coherence_history_dtc, color='blue', linewidth=3,
         label='DTC Objective Reduction')

# Plot Threshold
plt.axhline(coherence_threshold, color='red', linestyle=':', linewidth=2,
            label=r'Critical Threshold ($C_{irr}$)')

# Annotations
plt.title("DTC State Reduction vs. Standard Decoherence", fontsize=14)
plt.xlabel("Time (arbitrary units)")
plt.ylabel(r"Coherence $|\rho_{01}| + |\rho_{10}|$")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Add text annotations
if snap_index is not None:
    t_snap = times[snap_index]
    
    # Annotation for Reduction (Left side)
    plt.text(t_snap * 1.1, 0.05, "RAPID STATE\nREDUCTION", color='blue', fontsize=10, fontweight='bold', va='center')
    
    # Annotation for Environmental Decoherence (MOVED TO RIGHT)
    # FIX: Changed x-position from (t_snap * 0.35) to (t_snap * 1.6)
    # This places it in the "tail" region where the lines are separated.
    plt.text(t_snap * 1.6, 0.25, "Environmental\nDecoherence", color='gray', fontsize=10, ha='center')

plt.ylim(-0.02, 0.8) 
plt.tight_layout()
plt.savefig('DTC_COMPARISON_PLOT_FIXED.png', dpi=300)
plt.show()
