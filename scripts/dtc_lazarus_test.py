import numpy as np
import matplotlib.pyplot as plt

# --- PARAMETERS ---
# Tuned so the reduction happens visibly at ~7.6 µs (before the 10 µs pulse)
gamma = 6e6          # decoherence rate (s^-1) 
C_th = 1e-20         # DTC threshold
t = np.linspace(0, 20, 2000)        # time in microseconds (0 to 20 µs)

# --- PHASE 1: DECOHERENCE (0 to 10 µs) ---
mid = len(t)//2
t_decay = t[:mid]
C_decay = np.exp(-gamma * t_decay * 1e-6)   # convert µs → s

# --- PHASE 2: ATTEMPTED REVIVAL (10 to 20 µs) ---
t_revive = t[mid:]
revival_factor = 0.8                        # realistic echo efficiency (80%)
C_qm_revive = C_decay[-1] * np.exp(gamma * (t_revive - t_revive[0]) * 1e-6) * revival_factor

# --- BUILD CURVES ---
# 1. Standard QM Curve (Reversible)
C_qm = np.concatenate([C_decay, C_qm_revive])

# 2. DTC Curve (Irreversible)
C_dtc = np.copy(C_decay)
snap_idx = np.where(C_decay < C_th)[0]

snap_time = None
if len(snap_idx) > 0:
    first_snap = snap_idx[0]
    snap_time = t_decay[first_snap]
    # PHYSICS: Once crossed, the state is reduced to the pointer basis.
    C_dtc[first_snap:] = 0.0
    # During revival phase, it MUST remain 0 (Irreversibility)
    C_dtc_full = np.concatenate([C_dtc, np.zeros(len(t_revive))])
else:
    C_dtc_full = np.concatenate([C_dtc, C_qm_revive])

# --- PLOTTING ---
plt.figure(figsize=(11, 6.5))

# PLOT FIX: Thick transparent background for Standard QM
plt.semilogy(t, C_qm, color='steelblue', lw=8, alpha=0.4, label='Standard QM (Revival Possible)')

# Thin solid line for DTC
plt.semilogy(t, C_dtc_full, color='red', lw=2.5, label='DTC (Irreversible after Threshold)')

# Reference Lines
plt.axhline(C_th, color='orange', ls='--', lw=2, label=r'$C_{\rm th} = 10^{-20}$')
plt.axvline(t[mid], color='black', ls='-', lw=2, alpha=0.7, label='Eraser / Echo Pulse')

# Annotate the Snap
if snap_time is not None:
    # FIX: "Collapse Event" -> "Reduction Event"
    plt.axvline(snap_time, color='red', ls=':', lw=3, label='DTC Reduction Event')
    # FIX: "COLLAPSE" -> "REDUCTION"
    plt.text(snap_time + 0.2, 1e-22, "REDUCTION", color='red', fontsize=12, fontweight='bold', rotation=90)

# Labels and Formatting
plt.ylim(1e-24, 2)
plt.xlim(0, 20)
plt.xlabel('Time (µs)', fontsize=14)
plt.ylabel(r'Coherence $|2\rho_{12}(t)|$', fontsize=14)
# FIX: Title adjusted to match professional tone
plt.title('The Lazarus Test: Irreversibility of Objective Reduction', fontsize=16)
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, which='both', ls='--', alpha=0.3)
plt.tight_layout()

plt.show()
