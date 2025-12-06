# DTC_SINGLE_TRAJECTORY_COLLAPSE_FINAL.py
# Implements Renny's Dynamic Trajectory Collapse (DTC) Model
# Features:
# 1. Math Fix: Corrected Center of Mass (COM) scaling.
# 2. Logic: "0-Line" represents superposition average; "Snap" represents collapse.
# 3. Visualization: Shows Potential (Green/Purple), Ghost (Orange), and Real (Red) paths.

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
        Calculates the full, independent potential trajectories for Left and Right.
        """
        traj_L = []
        traj_R = []
        
        for t in range(steps):
            # Dynamic position of the wavepacket centers (moving apart)
            pos_L = -self.slit_dist / 2.0 - t * 0.05
            pos_R = self.slit_dist / 2.0 + t * 0.05
            
            # Initialize Basis states (Complex)
            phi_L = np.exp(-(self.x - pos_L)**2 / (2 * self.slit_width**2), dtype=complex)
            phi_R = np.exp(-(self.x - pos_R)**2 / (2 * self.slit_width**2), dtype=complex)
            
            # Apply momentum kick
            phi_L *= np.exp(1j * self.k_kick * self.x)
            phi_R *= np.exp(-1j * self.k_kick * self.x)

            # Normalize as Discrete Vectors
            phi_L /= np.linalg.norm(phi_L)
            phi_R /= np.linalg.norm(phi_R)

            # Calculate COM for L path
            # FIXED: Do not multiply by dx here, as normalization was vector-based.
            prob_density_L = np.abs(phi_L)**2
            com_L = np.sum(self.x * prob_density_L) 
            traj_L.append(com_L)
            
            # Calculate COM for R path
            prob_density_R = np.abs(phi_R)**2
            com_R = np.sum(self.x * prob_density_R)
            traj_R.append(com_R)
            
        return np.array(traj_L), np.array(traj_R)
        
    def propagate_and_measure(self, steps=100, detector_on=False, renny_trigger=False, traj_L_ref=None, traj_R_ref=None):
        trajectory = []
        self.current_state = None
        
        gamma = 0.15 
        RENNAY_THRESHOLD = 1e-4
        
        # Determine the snap point where the collapse occurs (The Math of DTC)
        snap_index = next((t for t in range(steps) if self.coherence * np.exp(-gamma * t) < RENNAY_THRESHOLD), steps - 1)
        
        # Determine outcome (Randomly choose a reality)
        if np.random.rand() > 0.5:
            self.current_state = "L"
        else:
            self.current_state = "R"

        for t in range(steps):
            if t < snap_index:
                # Pre-Collapse: Superposition COM is exactly 0 (Cloud covers both paths)
                trajectory.append(0.0)
            else:
                # Post-Collapse: Snap to the physical position of the chosen slit
                if self.current_state == "L":
                    trajectory.append(traj_L_ref[t])
                else:
                    trajectory.append(traj_R_ref[t])
            
        return np.array(trajectory), self.current_state, snap_index

# --- RUN THE EXPERIMENT ---

plt.figure(figsize=(12, 7))

# 1. Calculate Reference Paths (The Potentials)
sim_ref = RennyDoubleSlit()
traj_L_ref, traj_R_ref = sim_ref.calculate_path_trajectories(steps=100)

# 2. Run Single DTC Trial (The Observation)
sim_dtc = RennyDoubleSlit()
traj_dtc, outcome, snap_index = sim_dtc.propagate_and_measure(
    steps=100, detector_on=True, renny_trigger=True,
    traj_L_ref=traj_L_ref, traj_R_ref=traj_R_ref
)

# --- PLOTTING ---

times = np.arange(100)

# Plot the "Potential" paths (The branches that exist in Hilbert space)
plt.plot(times, traj_L_ref, color='green', linestyle=':', linewidth=2, alpha=0.5, label=r"Potential Path L")
plt.plot(times, traj_R_ref, color='purple', linestyle=':', linewidth=2, alpha=0.5, label=r"Potential Path R")

# Plot the "Ghost" line (The branch that vanishes)
if outcome == "L":
    traj_ghost = traj_R_ref
    ghost_label = "Vanished Path (Right)"
else:
    traj_ghost = traj_L_ref
    ghost_label = "Vanished Path (Left)"

# Only plot the ghost up to the snap point
plt.plot(times[:snap_index], traj_ghost[:snap_index], color='orange', linestyle='--', linewidth=3, alpha=0.7, label=ghost_label)

# Plot the Actual DTC Trajectory
plt.plot(times, traj_dtc, color='red', linewidth=4, label=f"Observed Particle (Result: {outcome})")


# Formatting
plt.axhline(0, color='black', alpha=0.3, linestyle='-')

# TITLE
plt.title("DTC: Single-Particle Trajectory Collapse", fontsize=16)

plt.xlabel("Time Step (Decoherence)", fontsize=12)
plt.ylabel("Position <x>", fontsize=12)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.2)

# Trigger Annotation
plt.axvline(x=snap_index, color='k', linestyle='--', alpha=0.5)
plt.text(snap_index + 2, 0.5, "Collapse Event", fontsize=10, rotation=90)

plt.ylim(-8, 8) 
plt.show()
