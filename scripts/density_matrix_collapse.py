# DTC_COMPARISON_PLOT_FINAL_V4.py
# FIX: Separates the DTC and QM evolution loops to ensure the QM line runs for 3000 steps.

import numpy as np
import matplotlib.pyplot as plt

# --- 1. Define the Physics Operators ---
hbar = 1.0 
sig_z = np.array([[1, 0], [0, -1]], dtype=complex)
P_L = np.array([[1, 0], [0, 0]], dtype=complex)
P_R = np.array([[0, 0], [0, 1]], dtype=complex)

def commutator(A, B):
    """[A, B] = AB - BA"""
    return np.dot(A, B) - np.dot(B, A)

def lindblad_dissipator(L, rho):
    """
    Standard Lindblad Dissipator: D[L]rho = L rho L^dagger - 0.5 * {L^dagger L, rho}
    """
    L_dag = L.conj().T
    term1 = np.dot(L, np.dot(rho, L_dag))
    L_dag_L = np.dot(L_dag, L)
    term2 = 0.5 * (np.dot(L_dag_L, rho) + np.dot(rho, L_dag_L)) # Anti-commutator
    return term1 - term2

# --- 2. Simulation Parameters ---
dt = 0.005
steps = 3000
times = np.linspace(0, steps*dt, steps)

# Hamiltonian
H = 1.0 * sig_z 

# Initial State
psi0 = np.array([[1], [1]], dtype=complex) / np.sqrt(2)
rho_initial = np.dot(psi0, psi0.conj().T)

# Parameters
gamma_decoherence = 0.3 
coherence_threshold = 0.15 

# --- 3a. DTC Evolution Loop (Can Break Early) ---
rho_dtc = rho_initial.copy()
coherence_history_dtc = []
snap_index = None

for i, t in enumerate(times):
    coherence_dtc = np.abs(rho_dtc[0, 1]) + np.abs(rho_dtc[1, 0])
    
    # Check DTC Snap Condition
    if snap_index is None and coherence_dtc < coherence_threshold:
        snap_index = i
        coherence_history_dtc.append(0.0) # Snap to zero coherence
        break # Terminate DTC evolution

    coherence_history_dtc.append(coherence_dtc)
    
    # Evolution step
    d_rho_unitary = -1j/hbar * commutator(H, rho_dtc)
    d_rho_env = gamma_decoherence * lindblad_dissipator(sig_z, rho_dtc)
    
    d_rho_dtc_dt = d_rho_unitary + d_rho_env
    rho_dtc = rho_dtc + d_rho_dtc_dt * dt
    
    # Ensure Trace Preservation
    rho_dtc = rho_dtc / np.trace(rho_dtc) 

# --- 3b. QM Evolution Loop (Must Run Full Time) ---
rho_qm = rho_initial.copy()
coherence_history_qm = [] # FIX: This list now runs for the full length

for i, t in enumerate(times):
    coherence_qm = np.abs(rho_qm[0, 1]) + np.abs(rho_qm[1, 0])
    coherence_history_qm.append(coherence_qm)
    
    # Evolution step
    d_rho_qm_dt = -1j/hbar * commutator(H, rho_qm) + gamma_decoherence * lindblad_dissipator(sig_z, rho_qm)
    rho_qm = rho_qm + d_rho_qm_dt * dt
    rho_qm = rho_qm / np.trace(rho_qm) 


# --- 4. Plotting (Comparison) ---
plt.figure(figsize=(10, 6))

# Plot Pure Decoherence (QM) - Gray line continues
# FIX: coherence_history_qm now has the same length as times (3000)
plt.plot(times, coherence_history_qm, color='gray', linestyle='--', linewidth=2,
          label='Pure Decoherence (Standard QM)')

# Plot DTC Coherence - Blue line terminates at snap_index
if snap_index is not None:
    # Use the length of the list, which includes the final 0.0 point
    times_dtc = times[:len(coherence_history_dtc)] 
    history_dtc = coherence_history_dtc
    
    plt.plot(times_dtc, history_dtc, color='blue', linewidth=3,
              label='DTC Objective Collapse')
else:
    # If no snap, plot the whole thing
    plt.plot(times, coherence_history_dtc, color='blue', linewidth=3,
              label='DTC Objective Collapse (No Snap)')

# Plot Threshold
plt.axhline(coherence_threshold, color='red', linestyle=':', linewidth=2,
             label='Irreversibility Threshold ($C_{th}$)')

# Annotations
plt.title("DTC vs. Standard Decoherence: Coherence", fontsize=14)
plt.xlabel("Time (arbitrary units)")
plt.ylabel("Coherence (Off-Diagonal Magnitude)")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Add text annotations for clarity
if snap_index is not None:
    t_snap = times[snap_index]
    
    # Annotation for Collapse
    plt.text(t_snap * 1.05, 0.05, "OBJECTIVE\nCOLLAPSE", color='red', fontsize=10, fontweight='bold', va='center')
    
    # Annotation for Environmental Decoherence
    plt.text(t_snap * 1.50, 0.25, "Environmental Decoherence", color='gray', fontsize=10, ha='center')

plt.ylim(0, 0.8)
plt.show()
