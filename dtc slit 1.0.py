# DTC_SINGLE_TRAJECTORY_COLLAPSE_FIXED.py
# Corrected all LaTeX strings with raw strings (r"...") to prevent SyntaxWarnings and ValueError.

import numpy as np
import matplotlib.pyplot as plt
import numpy as np # Keep this import

class RennyDoubleSlit:
    def __init__(self, N_points=1024, L=20.0):
        self.x = np.linspace(-L/2, L/2, N_points)
        self.dx = self.x[1] - self.x[0]
        
        self.slit_dist = 4.0
        self.slit_width = 1.0
        self.k_kick = 5.0
        self.coherence = 1.0
        
    def propagate_and_measure(self, steps=100, detector_on=False, renny_trigger=False):
        trajectory = []
        collapsed = False
        self.current_state = None
        
        gamma = 0.15 # Decoherence rate
        RENNAY_THRESHOLD = 1e-4 # Collapse threshold
        
        # Array to store the COM of the *other* (vanished) path
        other_path_traj = []
        
        for t in range(steps):
            drift = t * 0.05
            
            # Basis states (normalized and moved)
            phi_L = np.exp(-(self.x + self.slit_dist/2 + drift)**2 / 2.0) * np.exp(1j * self.k_kick * self.x)
            phi_R = np.exp(-(self.x - self.slit_dist/2 - drift)**2 / 2.0) * np.exp(-1j * self.k_kick * self.x)
            phi_L /= np.linalg.norm(phi_L)
            phi_R /= np.linalg.norm(phi_R)

            if not collapsed:
                if detector_on:
                    self.coherence *= np.exp(-gamma)
                
                if detector_on and renny_trigger and (self.coherence < RENNAY_THRESHOLD):
                    if np.random.rand() > 0.5:
                        self.current_state = "L"
                    else:
                        self.current_state = "R"
                    collapsed = True
                
                # State before or during collapse step
                if collapsed:
                    psi_t = phi_L if self.current_state == "L" else phi_R
                    # For the ghost line: calculate COM of the discarded branch
                    psi_ghost = phi_R if self.current_state == "L" else phi_L
                else:
                    psi_t = (phi_L + phi_R) / np.sqrt(2) # Superposition
                    psi_ghost = (phi_L + phi_R) / np.sqrt(2) # Ghost is the same before collapse
            else:
                # Post-Collapse Evolution (Only one branch evolves)
                psi_t = phi_L if self.current_state == "L" else phi_R
                # For the ghost line: calculate COM of the discarded branch
                psi_ghost = phi_R if self.current_state == "L" else phi_L


            # Calculate Center of Mass (COM) for the chosen path
            prob_density = np.abs(psi_t)**2
            prob_density /= np.sum(prob_density * self.dx)
            com = np.sum(self.x * prob_density * self.dx)
            trajectory.append(com)
            
            # Calculate Center of Mass (COM) for the vanished path
            prob_density_ghost = np.abs(psi_ghost)**2
            prob_density_ghost /= np.sum(prob_density_ghost * self.dx)
            com_ghost = np.sum(self.x * prob_density_ghost * self.dx)
            other_path_traj.append(com_ghost)
            
        return np.array(trajectory), np.array(other_path_traj), self.current_state

# --- RUN THE EXPERIMENT ---

plt.figure(figsize=(12, 7))

# 1. Run SINGLE DTC Trajectory
sim_dtc = RennyDoubleSlit()
traj_dtc, traj_ghost_calc, outcome = sim_dtc.propagate_and_measure(steps=100, detector_on=True, renny_trigger=True)

# 2. Run Standard QM (No Detector) for comparison
sim_quant = RennyDoubleSlit()
traj_quant, _, _ = sim_quant.propagate_and_measure(steps=100, detector_on=False, renny_trigger=False)

# --- PLOTTING ---

# Plot Standard Quantum Baseline (Blue Dashed)
plt.plot(traj_quant, color='blue', linestyle='--', linewidth=3, label="Standard Quantum (No Collapse)")

# Plot the SINGLE DTC Outcome (Red Solid)
plt.plot(traj_dtc, color='red', linewidth=4, label=f"DTC Single Outcome (Result: {outcome})")

# Determine the ghost line to plot
if outcome == "L":
    # If L was chosen, the R-path vanished. R-path trajectory diverges UPWARD.
    label_ghost = r"Vanished Branch ($\phi_R \to 0$)"
    vertical_pos = 4
    # Slice the ghost line to disappear AFTER the snap point (t=60)
    traj_ghost = np.concatenate((traj_ghost_calc[:60], np.full(40, traj_ghost_calc[60]))) # Keep the path trajectory, but simplify disappearance plotting
else:
    # If R was chosen, the L-path vanished. L-path trajectory diverges DOWNWARD.
    label_ghost = r"Vanished Branch ($\phi_L \to 0$)"
    vertical_pos = -4
    traj_ghost = np.concatenate((traj_ghost_calc[:60], np.full(40, traj_ghost_calc[60])))

# Plot the "Ghost" of the Vanished Path
# We plot the trajectory of the *vanished* branch up to the snap, and then terminate it
plt.plot(traj_ghost[:60], color='orange', linestyle=':', linewidth=2, alpha=0.6, label=label_ghost)


# Formatting
plt.axhline(0, color='black', alpha=0.3, linestyle=':')
plt.title("DTC: Single-Trial Trajectory Collapse (Resolution of Paradox)", fontsize=14)
plt.xlabel("Time Step (Decoherence increasing $\\to$)")
# FIXED: Use raw string for the complex LaTeX
plt.ylabel(r"Particle Position $\mathbf{\langle x \rangle}$")
plt.legend(loc='upper left')
plt.grid(True, alpha=0.2)

# Add annotation for the trigger moment
plt.axvline(x=60, color='k', linestyle='--', alpha=0.5)
plt.text(62, -5.5, "Trigger Event", fontsize=10)
plt.text(80, vertical_pos, f"Outcome: {outcome} Slit", color='red', fontsize=12, fontweight='bold')

plt.show()
