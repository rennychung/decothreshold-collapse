import numpy as np
import matplotlib.pyplot as plt

# --- 1. Define the Physics ---
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
rho = np.dot(psi0, psi0.conj().T) 

# Parameters
gamma_decoherence = 0.3   
coherence_threshold = 0.15 # The cut-off point
gamma_collapse_rate = 100.0 

coherence_history = [] 

# --- 3. Time Evolution ---
for t in times:
    
    # Calculate Coherence (L1 norm of off-diagonals)
    coherence = np.abs(rho[0, 1]) + np.abs(rho[1, 0])
    
    # The Logic: Decoherence-Triggered Pruning
    if coherence < coherence_threshold:
        current_gamma_collapse = gamma_collapse_rate
    else:
        current_gamma_collapse = 0.0
        
    d_rho_unitary = -1j * commutator(H, rho)
    d_rho_env = gamma_decoherence * lindblad_dissipator(sig_z, rho)
    d_rho_prune = current_gamma_collapse * (lindblad_dissipator(P_L, rho) + lindblad_dissipator(P_R, rho))
    
    d_rho_dt = d_rho_unitary + d_rho_env + d_rho_prune
    rho = rho + d_rho_dt * dt
    
    coherence_history.append(coherence)

# --- 4. Plotting (Fixed Labels) ---
plt.figure(figsize=(10, 6))

# Plot Coherence
plt.plot(times, coherence_history, color='blue', linewidth=3, label='System Coherence $C(\\rho)$')

# Plot Threshold
plt.axhline(coherence_threshold, color='red', linestyle='--', linewidth=2, label='Irreversibility Threshold $(C_{th})$')

# Annotations
plt.title("Dynamics of Decoherence-Triggered Objective Collapse", fontsize=14)
plt.xlabel("Time (arbitrary units)")
plt.ylabel("Coherence (Off-Diagonal Magnitude)")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Find the drop point for text placement
try:
    drop_idx = next(i for i, v in enumerate(coherence_history) if v < coherence_threshold)
    
    # --- FIX IS HERE ---
    # Moved text to 25% of the drop time (earlier) and y=0.2 (lower)
    # This puts it in the bottom-left corner, strictly UNDER the blue line.
    plt.text(times[drop_idx]*0.25, 0.2, "Environmental\nDecoherence", color='blue', fontsize=11, ha='center')
    
    # Annotation 2: The Event (kept same)
    plt.text(times[drop_idx], 0.02, "  OBJECTIVE\n  COLLAPSE", color='red', fontsize=11, fontweight='bold', va='bottom')
except StopIteration:
    pass

plt.show()
