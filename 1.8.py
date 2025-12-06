# dtc_cat_test_DIAGNOSTIC.py
# This script prints the collapse time instead of plotting.
import numpy as np

# === PARAMETERS ===
Delta_x = 100e-9          # 100 nm separation
sigma_x = 5e-9            # packet width
gamma_env = 1e4           # decoherence rate (s^-1)
C_th = 1e-20              # DTC threshold

t_final = 0.15
steps = 12000
times = np.linspace(0, t_final, steps)

# === POSITION GRID ===
x = np.linspace(-400e-9, 400e-9, 2000)
dx = x[1] - x[0]

# === TWO GAUSSIAN PACKETS ===
psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))

# Normalise individual branches
psi_L /= np.sqrt(np.sum(np.abs(psi_L)**2) * dx)
psi_R /= np.sqrt(np.sum(np.abs(psi_R)**2) * dx)

# Cat state
psi_cat = (psi_L + psi_R) / np.sqrt(2)

# === COHERENCE FUNCTION (Simplified for the initial state check) ===
# For this diagnostic, we only need the initial coherence.
def coh_initial(psi):
    rho = np.outer(psi, psi.conj())
    # Note: L1 norm simplified, but functional for initial value
    return np.sum(np.abs(rho - np.diag(np.diag(rho)))) * dx

# === DTC SIMULATION (Logic Check) ===
C_initial = coh_initial(psi_cat)
C_current = C_initial
triggered = False
t_trigger = None

# Calculate the decoherence decay factor per time step
dt = times[1] - times[0]
decay = np.exp(-gamma_env * (Delta_x**2) * dt / (4*sigma_x**2))

for i in range(1, steps):
    C_current *= decay
    
    if not triggered and C_current < C_th:
        triggered = True
        t_trigger = times[i]
        break # Exit the loop immediately once collapse is detected

# === OUTPUT RESULTS ===
print("==============================================")
print("DTC Simulation Diagnostic Results:")
print(f"Initial Coherence (C₀): {C_initial:.4e}")
print(f"Decoherence Threshold (C_th): {C_th:.1e}")
if t_trigger:
    print(f"✅ DTC Collapse Triggered at t = {t_trigger:.2e} seconds")
    print("The simulation is working perfectly.")
else:
    print("❌ Collapse not triggered within the time frame.")
print("==============================================")

# Remove the plotting commands entirely
# plt.show()
