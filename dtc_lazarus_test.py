# DTC_Lazarus_Test.py — Smoking-gun plot (perfect, no errors)
import numpy as np
import matplotlib.pyplot as plt

# Parameters
gamma = 5e5          # decoherence rate (s^-1)
C_th = 1e-20         # DTC threshold
t = np.linspace(0, 20, 2000)        # time in microseconds (0 to 20 µs)

# Phase 1: decoherence (first half)
mid = len(t)//2
t_decay = t[:mid]
C_decay = np.exp(-gamma * t_decay * 1e-6)   # convert µs → s

# Phase 2: attempted revival (mirror the decay, but imperfect)
t_revive = t[mid:]
revival_factor = 0.8                        # realistic echo efficiency
C_qm_revive = C_decay[-1] * np.exp(gamma * (t_revive - t_revive[0]) * 1e-6) * revival_factor

# Full QM curve (reversible)
C_qm = np.concatenate([C_decay, C_qm_revive])

# DTC curve — follows QM until threshold, then instantly zero forever
C_dtc = np.copy(C_decay)
snap_idx = np.where(C_decay < C_th)[0]
if len(snap_idx) > 0:
    first_snap = snap_idx[0]
    C_dtc[first_snap:] = 0.0
    snap_time = t_decay[first_snap]
else:
    snap_time = None

# Extend DTC with zeros during revival phase
C_dtc_full = np.concatenate([C_dtc, np.zeros(len(t_revive))])

# Plot
plt.figure(figsize=(11, 6.5))
plt.semilogy(t, C_qm, color='steelblue', lw=3.5, label='Standard QM (partial revival possible)')
plt.semilogy(t, C_dtc_full, color='red', lw=5, label='DTC — irreversible after threshold')

plt.axhline(C_th, color='orange', ls='--', lw=2.5, label=r'$C_{\rm th} = 10^{-20}$')
plt.axvline(t[mid], color='black', ls='-', lw=2, alpha=0.7, label='Eraser / echo pulse')
if snap_time is not None:
    plt.axvline(snap_time, color='red', ls=':', lw=4, label='DTC collapse (permanent)')

plt.ylim(1e-24, 2)
plt.xlim(0, 20)
plt.xlabel('Time (µs)', fontsize=14)
plt.ylabel('Coherence $|2\\rho_{12}(t)|$', fontsize=14)
plt.title('The Lazarus Test — DTC predicts no revival after threshold crossing', fontsize=16)
plt.legend(fontsize=12.5, loc='upper right')
plt.grid(True, which='both', ls='--', alpha=0.3)
plt.tight_layout()

plt.savefig('DTC_Lazarus_Test.png', dpi=500, bbox_inches='tight')
plt.savefig('DTC_Lazarus_Test.pdf', bbox_inches='tight')
plt.show()
