import numpy as np
import matplotlib.pyplot as plt

class RennyDoubleSlit:
    def __init__(self, N_points=1024, L=20.0):
        self.x = np.linspace(-L/2, L/2, N_points)
        self.dx = self.x[1] - self.x[0]
        
        self.slit_dist = 4.0
        self.slit_width = 1.0
        self.k_kick = 0.5  # Momentum kick to separate packets
        self.coherence = 1.0
        
    def calculate_path_trajectories(self, steps=100):
        """
        Calculates the full, independent Center of Mass (COM) trajectories for the Left and Right paths 
        if they were propagating alone (used as a reference).
        """
        traj_L = []
        traj_R = []
        
        for t in range(steps):
            # Dynamic position of the wavepacket centers (moving apart)
            pos_L = -self.slit_dist / 2.0 - t * 0.05
            pos_R = self.slit_dist / 2.0 + t * 0.05
            
            # Initialize Basis states (Complex) - for conceptual setup only
            phi_L = np.exp(-(self.x - pos_L)**2 / (2 * self.slit_width**2), dtype=complex)
            phi_R = np.exp(-(self.x - pos_R)**2 / (2 * self.slit_width**2), dtype=complex)
            
            # Apply momentum kick (for conceptual illustration of separation)
            phi_L *= np.exp(1j * self.k_kick * self.x)
            phi_R *= np.exp(-1j * self.k_kick * self.x)

            # Normalize as Discrete Vectors
            phi_L /= np.linalg.norm(phi_L)
            phi_R /= np.linalg.norm(phi_R)

            # Use the intended classical position (pos_L/R) as the COM trajectory
            traj_L.append(pos_L)
            traj_R.append(pos_R)
            
        return np.array(traj_L), np.array(traj_R)
        
    def propagate_and_measure(self, steps=100, traj_L_ref=None, traj_R_ref=None):
        """
        Simulates the DTC reduction process, projecting the trajectory 
        to one of the reference paths at the trigger time.
        """
        trajectory = []
        self.current_state = None
        
        # DTC Parameters
        gamma = 0.15  # Decoherence Rate
        THRESHOLD = 1e-4  # C_irr (The Reduction Threshold)
        
        # 1. Determine the REDUCTION POINT
        # Find the first time step (t) where coherence drops below the threshold
        snap_index = next((t for t in range(steps) if self.coherence * np.exp(-gamma * t) < THRESHOLD), steps - 1)
        
        # 2. Determine the CHOSEN OUTCOME (50/50 chance for L or R)
        if np.random.rand() > 0.5:
            self.current_state = "L"
        else:
            self.current_state = "R"

        # 3. Build the DTC Trajectory
        for t in range(steps):
            if t < snap_index:
                # Pre-Reduction: Superposition COM is exactly 0
                trajectory.append(0.0)
            else:
                # Post-Reduction: Project to the physical position of the chosen path
                if self.current_state == "L":
                    trajectory.append(traj_L_ref[t])
                else:
                    trajectory.append(traj_R_ref[t])
            
        return np.array(trajectory), self.current_state, snap_index

# --- RUN THE EXPERIMENT AND PLOT ---

plt.figure(figsize=(12, 7))

# 1. Calculate Reference Paths
sim_ref = RennyDoubleSlit()
traj_L_ref, traj_R_ref = sim_ref.calculate_path_trajectories(steps=100)

# 2. Run Single DTC Trial
sim_dtc = RennyDoubleSlit()
traj_dtc, outcome, snap_index = sim_dtc.propagate_and_measure(
    steps=100,
    traj_L_ref=traj_L_ref, traj_R_ref=traj_R_ref
)

steps = 100
times = np.arange(steps)

# 1. Determine which is the Nullified Path
if outcome == "L":
    traj_vanished_ref = traj_R_ref
    # FIX: Changed "Vanished" to "Nullified Component"
    vanished_label = "Nullified Component (Right)"
else:
    traj_vanished_ref = traj_L_ref
    # FIX: Changed "Vanished" to "Nullified Component"
    vanished_label = "Nullified Component (Left)"

# 2. Create the Nullified Path Visualization Array
traj_vanished_vis = np.zeros(steps)

# Implement the visualization logic:
traj_vanished_vis[snap_index:] = traj_vanished_ref[snap_index:]

# Plot the Full Potential Reference Paths
plt.plot(times, traj_L_ref, color='green', linestyle=':', linewidth=2, alpha=0.3, label=r"Potential Path L (Reference)")
plt.plot(times, traj_R_ref, color='purple', linestyle=':', linewidth=2, alpha=0.3, label=r"Potential Path R (Reference)")

# Plot the Nullified Path
# FIX: Updated label variable
plt.plot(times, traj_vanished_vis, color='orange', linestyle='--', linewidth=3, alpha=0.9, 
         label=vanished_label)

# Plot the Actual DTC Trajectory
# FIX: Changed "Observed Particle" to "Projected State" (Optional, but sounds more formal)
plt.plot(times, traj_dtc, color='red', linewidth=4, label=f"Projected State (Outcome: {outcome})")

# Formatting
plt.axhline(0, color='black', alpha=0.3, linestyle='-')

# FIX: Title changed from "Collapse" to "State Reduction"
plt.title("DTC: Single-Particle State Reduction", fontsize=16) 

plt.xlabel("Time Step (Decoherence/Evolution)", fontsize=12)
plt.ylabel("Center of Mass Position $\\langle x \\rangle$", fontsize=12)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.2)

# Trigger Annotation
plt.axvline(x=snap_index, color='k', linestyle='--', alpha=0.7)

# FIX: Changed "Collapse Event" to "Reduction Event"
plt.text(snap_index + 2, 0.5, "Reduction Event", fontsize=10, rotation=90) 

plt.ylim(-8, 8) 
plt.show()
