# DTC_SINGLE_TRAJECTORY_COLLAPSE_FULLY_FIXED_FINAL_V2.py
# FIX: Corrects the NumPy UFuncOutputCastingError by initializing phi_L and phi_R as complex arrays.

import numpy as np
import matplotlib.pyplot as plt

class RennyDoubleSlit:
    def __init__(self, N_points=1024, L=20.0):
        self.x = np.linspace(-L/2, L/2, N_points)
        self.dx = self.x[1] - self.x[0]
        
        self.slit_dist = 4.0
        self.slit_width = 1.0
        self.k_kick = 0.5 
        self.coherence = 1.0
        
    def calculate_path_trajectories(self, steps=100):
        """
        Calculates the full, independent trajectories for the Left and Right paths.
        FIXED: Ensures phi_L and phi_R are initialized as complex types.
        """
        traj_L = []
        traj_R = []
        
        for t in range(steps):
            pos_L = -self.slit_dist / 2.0 - t * 0.05
            pos_R = self.slit_dist / 2.0 + t * 0.05
            
            # Basis states: INITIALIZE AS COMPLEX DTYPE to avoid the error
            phi_L = np.exp(-(self.x - pos_L)**2 / (2 * self.slit_width**2), dtype=complex)
            phi_R = np.exp(-(self.x - pos_R)**2 / (2 * self.slit_width**2), dtype=complex)
            
            # Apply momentum kick (complex multiplication is now allowed)
            phi_L *= np.exp(1j * self.k_kick * self.x)
            phi_R *= np.exp(-1j * self.k_kick * self.x)

            # Normalize and calculate COM
            # Note: COM calculation uses np.abs(phi)**2, which yields a real number (prob density)
            phi_L /= np.linalg.norm(phi_L)
            phi_R /= np.linalg.norm(phi_R)

            # Calculate COM for L path
            prob_density_L = np.abs(phi_L)**2
            com_L = np.sum(self.x * prob_density_L * self.dx)
            traj_L.append(com_L)
            
            # Calculate COM for R path
            prob_density_R = np.abs(phi_R)**2
            com_R = np.sum(self.x * prob_density_R * self.dx)
            traj_R.append(com_R)
            
        return np.array(traj_L), np.array(traj_R)
        
    def propagate_and_measure(self, steps=100, detector_on=False, renny_trigger=False, traj_L_ref=None, traj_R_ref=None):
        trajectory = []
        self.current_state = None
        
        gamma = 0.15 
        RENNAY_THRESHOLD = 1e-4
        
        # Determine the snap point where the collapse occurs
        snap_index = next((t for t in range(steps) if self.coherence * np.exp(-gamma * t) < RENNAY_THRESHOLD), steps - 1)
        
        # Determine the random outcome at the start for consistency
        if np.random.rand() > 0.5:
            self.current_state = "L"
        else:
            self.current_state = "R"

        # Simulate the single run trajectory
        for t in range(steps):
            if t < snap_index:
                # Pre-Collapse: Superposition COM (y=0)
                trajectory.append(0.0)
            else:
                # Post-Collapse: Follow the chosen path trajectory
                if self.current_state == "L":
                    trajectory.append(traj_L_ref[t])
                else:
                    trajectory.append(traj_R_ref[t])
            
        return np.array(trajectory), self.current_state, snap_index

# --- RUN THE EXPERIMENT ---

plt.figure(figsize=(12, 7))

# 0. Calculate ALL possible path trajectories first
sim_ref = RennyDoubleSlit()
traj_L_ref, traj_R_ref = sim_ref.calculate_path_trajectories(steps=100)

# 1. Run SINGLE DTC Trajectory to get the chosen outcome and snap index
sim_dtc = RennyDoubleSlit()
traj_dtc, outcome, snap_index = sim_dtc.propagate_and_measure(
    steps=100, detector_on=True, renny_trigger=True,
    traj_L_ref=traj_L_ref, traj_R_ref=traj_R_ref
)

# --- PLOTTING ---

times = np.arange(100)

# 1. Determine the Ghost Line and Plot
if outcome == "L":
    traj_ghost = traj_R_ref
    label_ghost = r"Vanished Branch ($\phi_R$ Disappears)"
    vertical_pos = traj_R_ref[-1] 
else:
    traj_ghost = traj_L_ref
    label_ghost = r"Vanished Branch ($\phi_L$ Disappears)"
    vertical_pos = traj_L_ref[-1]

# Plot the ghost line: it MUST follow the diverging path until the snap, and then terminate.
traj_ghost_diverge = traj_ghost[:snap_index]

# The orange line must show the path that would have been taken
# We plot the full reference trajectory of the *vanished* branch up to the snap index.
plt.plot(times[:snap_index], traj_ghost_diverge, color='orange', linestyle=':', linewidth=3, alpha=0.6, label=label_ghost)


# 2. Plot the SINGLE DTC Outcome (Red Solid)
plt.plot(times, traj_dtc, color='red', linewidth=4, label=f"DTC Single Outcome (Result: {outcome})")


# 3. Plot the Standard Quantum Baseline (Blue Dashed)
plt.plot(times, np.zeros(100), color='blue', linestyle='--', linewidth=3, label="Standard Quantum (No Collapse)")


# Formatting
plt.axhline(0, color='black', alpha=0.3, linestyle=':')
plt.title("DTC: Single-Trial Trajectory Collapse (Resolution of Paradox)", fontsize=14)
plt.xlabel(r"Time Step (Decoherence increasing $\to$)")
plt.ylabel(r"Particle Position $\mathbf{\langle x \rangle}$")
plt.legend(loc='upper left')
plt.grid(True, alpha=0.2)

# Add annotation for the trigger moment
plt.axvline(x=snap_index, color='k', linestyle='--', alpha=0.5)
plt.text(snap_index + 2, -5.5, "Trigger Event (Collapse)", fontsize=10)
plt.text(80, vertical_pos * 0.9, f"Chosen: {outcome} Slit", color='red', fontsize=12, fontweight='bold')

plt.ylim(-7, 7)
plt.show()
