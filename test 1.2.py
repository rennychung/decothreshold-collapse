import matplotlib
# Use 'TkAgg' backend to force the plot window to display on most systems.
# If this doesn't work, try 'Qt5Agg' (may require 'pip install PyQt5').
matplotlib.use('TkAgg') 
import numpy as np
import matplotlib.pyplot as plt

# === REALISTIC 2025–2030 PARAMETERS (DTC Cat State Simulation) ===
# Parameters for a typical levitated nanosphere experiment.
mass = 1e-16                    # kg → ~100 nm silica sphere (m = 10^-16 kg)
Delta_x = 100e-9                # 100 nm spatial cat state (separation of the two peaks)
sigma_x = 5e-9                  # ground-state width of each peak
gamma_env = 1e4                 # s⁻¹ — environmental decoherence rate (calibrated gas/photon scattering)
C_th = 1e-20                    # DTC irreversibility threshold (The critical coherence value)

# === TIME GRID ===
t_final = 0.15                  # seconds — Total simulation time
steps = 12000
times = np.linspace(0, t_final, steps)
dt = times[1] - times[0]

# === INITIAL CAT STATE (Superposition of two localized Gaussians) ===
# Spatial grid (in meters)
x = np.linspace(-400e-9, 400e-9, 1600)
dx = x[1] - x[0]

# Two localized wave functions (Left and Right)
psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))

# Cat state (equal superposition)
psi_cat = (psi_L + psi_R)

# Normalize the initial cat state
norm = np.sqrt(np.sum(np.abs(psi_cat)**2) * dx)
psi_cat /= norm

# === COHERENCE FUNCTION (A simplified measure for a cat state) ===
def coherence(psi):
    # Proxy for the coherence C(rho) using the l¹-norm of the off-diagonals.
    rho = np.outer(psi, psi.conj())
    diag = np.diag(np.diag(rho))
    return np.sum(np.abs(rho - diag)) * dx

# === SIMULATION 1: DTC (Decoherence-Triggered Collapse) ===
def run_dtc():
    psi = psi_cat.copy()
    C = coherence(psi)
    psi_hist = [psi.copy
