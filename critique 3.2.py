# DTC_fair_test_CORRECTED_AND_WORKING.py
import numpy as np
import matplotlib.pyplot as plt

# --------------------------- Parameters ---------------------------
gamma_env = 1e5          # environmental decoherence rate in s^-1 → T₂ ≈ 10 µs
C_th      = 1e-20        # DTC irreversibility threshold
t_final   = 550e-6       # 550 µs total time
times     = np.linspace(0, t_final, 3000)   # more points = smoother curves

# --------------------------- Coherence evolution ---------------------------

# 1. Pure QM + environmental decoherence only
C_qm = np.exp(-gamma_env * times)                     # exact analytic result

# 2. CSL — extra exponential suppression
lambda_allowed  = 1e-11                               # 2025 upper bound
lambda_original = 1e-17                               # original GRW/CSL value
C_csl_allowed  = C_qm * np.exp(-lambda_allowed  * times)
C_csl_original = C_qm * np.exp(-lambda_original * times)

# 3. DTC — follows QM exactly until C_th, then instantly drops to zero
C_dtc = np.copy(C_qm)
snap_idx = np.where(C_qm < C_th)[0]
if len(snap_idx) > 0:
    first_snap = snap_idx[0]
    C_dtc[first_snap:] = 0.0                          # instant pruning
    snap_time = times[first_snap] * 1e6
    print(f"DTC snaps to zero at {snap_time:.1f} µs")
else:
    print("Warning: threshold never reached")

# --------------------------- Plot ---------------------------
plt.figure(figsize=(11, 7))

plt.semilogy(times*1e6, C_qm,               color='gray',    lw=3,   label='QM + decoherence')
plt.semilogy(times*1e6, C_csl_allowed,      color='green',   lw=3,   label=r'CSL allowed ($\lambda \leq 10^{-11}$ s$^{-1}$)')
plt.semilogy(times*1e6, C_csl_original,     color='limegreen', lw=2.5, ls='--',
             label=r'Original CSL ($\lambda = 10^{-17}$ s$^{-1}$)')
plt.semilogy(times*1e6, C_dtc,              color='red',     lw=5,   label='DTC (instant pruning)')

# Horizontal & vertical markers
plt.axhline(C_th, color='orange', ls='--', lw=2.5, label=r'$C_{\rm th} = 10^{-20}$')
plt.axvline(100,  color='blue',   ls=':',  lw=2.5, label='100 µs')
if len(snap_idx) > 0:
    plt.axvline(times[first_snap]*1e6, color='red', ls=':', lw=4, label=f'DTC snap ≈{snap_time:.0f} µs')
plt.axhline(1e-12, color='purple', ls='-.', lw=2.5, label='2026 projected sensitivity')

plt.ylim(1e-23, 1.5)
plt.xlim(0, 550)
plt.xlabel('Time (µs)', fontsize=15)
plt.ylabel(r'Coherence $C(t) = 2|\rho_{12}(t)|$', fontsize=15)
plt.title('Honest DTC Test — All curves correct and visible', fontsize=17)
plt.legend(fontsize=13, loc='lower left')
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.tight_layout()

plt.savefig('DTC_fair_test_CORRECT.png', dpi=500, bbox_inches='tight')
plt.savefig('DTC_fair_test_CORRECT.pdf', bbox_inches='tight')
plt.show()
