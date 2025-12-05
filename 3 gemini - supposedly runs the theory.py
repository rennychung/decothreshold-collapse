import numpy as np
import matplotlib.pyplot as plt

class RennyDoubleSlit:
    def __init__(self, N_points=1024, L=20.0):
        self.x = np.linspace(-L/2, L/2, N_points)
        self.dx = self.x[1] - self.x[0]
        self.psi = np.exp(-(self.x)**2 / 2.0)  # Initial Gaussian
        self.psi /= np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx) # Normalize
        
        # Double Slit Potential (Approximate with transmission function)
        self.slit_dist = 4.0
        self.slit_width = 1.0
        
        # Define Left and Right Basis masks (smooth)
        self.mask_L = np.exp(-(self.x + self.slit_dist/2)**2 / (2*self.slit_width**2))
        self.mask_R = np.exp(-(self.x - self.slit_dist/2)**2 / (2*self.slit_width**2))
        
        # Dynamics parameters
        self.k_kick = 5.0 # Momentum to move wavepacket forward (simulated by time evolution)
        self.coherence = 1.0 # Starts fully coherent
        
    def propagate_and_measure(self, steps=200, detector_on=False, renny_trigger=False):
        """
        Simulates the particle. 
        If detector_on=True: Coherence decays.
        If renny_trigger=True: Instant collapse occurs when coherence is dead.
        """
        trajectory = []
        collapsed = False
        
        # Environmental Decay Rate (The "Air molecules")
        gamma = 0.15 
        
        # Renny's "Sharp Switch" Threshold
        RENNAY_THRESHOLD = 1e-4 # Using 1e-4 for visual plotting scale (in reality 1e-20)
        
        # We simulate the split wavepacket by creating a superposition
        # psi = (1/sqrt(2)) * (|L> + |R>) moving apart
        
        for t in range(steps):
            # 1. Simple drift model: The L and R packets separate over time
            drift = t * 0.05
            
            # Construct the superposition state
            # This represents the unitary evolution U(t)|psi>
            phi_L = np.exp(-(self.x + self.slit_dist/2 + drift)**2 / 2.0) * np.exp(1j * self.k_kick * self.x)
            phi_R = np.exp(-(self.x - self.slit_dist/2 - drift)**2 / 2.0) * np.exp(-1j * self.k_kick * self.x)
            
            # Normalize basis states
            phi_L /= np.linalg.norm(phi_L)
            phi_R /= np.linalg.norm(phi_R)
            
            if not collapsed:
                # Superposition with current Coherence level
                # In Density Matrix language: rho = |L><L| + |R><R| + C(|L><R| + |R><L|)
                # In Wavefunction language for a single run, we simulate the "Pre-Collapse" 
                # as maintaining the superposition until the trigger fires.
                
                # Apply Decoherence if detector is on
                if detector_on:
                    self.coherence *= np.exp(-gamma)
                
                # --- RENNY'S TRIGGER CHECK ---
                if detector_on and renny_trigger and (self.coherence < RENNAY_THRESHOLD):
                    # "Every other outcome has become nonexistent"
                    # Born Rule: 50/50 for this symmetric setup
                    if np.random.rand() > 0.5:
                        self.current_state = "L"
                    else:
                        self.current_state = "R"
                    collapsed = True
                
                # Determine current effective wavefunction for plotting
                if collapsed:
                    if self.current_state == "L":
                        psi_t = phi_L
                    else:
                        psi_t = phi_R
                else:
                    # Still in superposition
                    psi_t = (phi_L + phi_R) / np.sqrt(2)
            
            else:
                # Post-Collapse: Unitary evolution of the single branch
                if self.current_state == "L":
                    psi_t = phi_L
                else:
                    psi_t = phi_R

            # Track the "Center of Mass" of the probability distribution
            prob_density = np.abs(psi_t)**2
            prob_density /= np.sum(prob_density * self.dx)
            com = np.sum(self.x * prob_density * self.dx)
            trajectory.append(com)
            
        return np.array(trajectory)

# --- RUN THE EXPERIMENT ---

plt.figure(figsize=(12, 7))

# 1. Run 15 Trajectories with Renny's Trigger
for i in range(15):
    sim = RennyDoubleSlit()
    # Varying randomness in the "drift" or environment slightly would separate lines more,
    # but here the random choice of Left/Right shows the bifurcation.
    traj = sim.propagate_and_measure(steps=100, detector_on=True, renny_trigger=True)
    
    # Plot with transparency to show the "bundle"
    if i == 0:
        plt.plot(traj, color='red', alpha=0.4, linewidth=2, label="Single Run (Detector + Trigger)")
    else:
        plt.plot(traj, color='red', alpha=0.4, linewidth=2)

# 2. Run "Quantum Average" (No Detector / Interference) for comparison
sim_quant = RennyDoubleSlit()
traj_quant = sim_quant.propagate_and_measure(steps=100, detector_on=False, renny_trigger=False)
plt.plot(traj_quant, color='blue', linestyle='--', linewidth=3, label="Standard Quantum (No Detector)")

# Formatting aligned with the theory
plt.axhline(0, color='black', alpha=0.3, linestyle=':')
plt.text(0, 0.5, "Source", ha='center')
plt.text(80, 4, "Right Slit Outcome", color='red')
plt.text(80, -4, "Left Slit Outcome", color='red')

plt.title("Renny's Theory: Decoherence-Triggered Instant Pruning", fontsize=14)
plt.xlabel("Time Step (Decoherence increasing ->)")
plt.ylabel("Particle Position <x>")
plt.legend(loc='upper left')
plt.grid(True, alpha=0.2)

# Add annotation for the trigger moment
plt.axvline(x=60, color='k', linestyle='--', alpha=0.5)
plt.text(62, -5, "Trigger Event\n(Coherence < Threshold)", fontsize=10)

plt.show()
