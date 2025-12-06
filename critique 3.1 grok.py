# DTC_fair_test_FINAL_WORKING.py
# This version runs perfectly and shows the red DTC line clearly

import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, ket2dm, sigmaz, mesolve

# --------------------------- Parameters ---------------------------
gamma_env = 1e5          # s^-1 → T2 ≈ 10 µs
C_th      = 1e-20        # DTC threshold
lambda_allowed = 1e-11   # 2025 CSL upper bound
lambda_original = 1e-17  # original GRW/CSL
t_final   = 550e-6       # 550 µs
times     = np.linspace(0, t_final, 2000)

# --------------------------- Initial state ---------------------------
psi0 = (basis(2,0) + basis(2,1)).unit()
rho0 = ket2dm(psi0)

# 1. Pure QM + normal decoherence
result_qm = mesolve(0*sigmaz(), rho0, times, c_ops=[np.sqrt(gamma_env)*sigmaz()])
C_qm = np.array([2 * abs(rho[0,1]) for rho in result_qm.states])

# 2. CSL allowed & original (mean only)
C_csl_allowed  = np.exp(-gamma_env * times) * np.exp(-lambda_allowed * times)
C_csl_original = np.exp(-gamma_env * times) * np.exp(-lambda_original * times)

# 3. DTC – manual integration so the pruning is visible
C_dtc = np.zeros(len(times))
rho   = rho0.full()           # work with numpy arrays
triggered = False

for i, t in enumerate(times):
    dt = times[1] - times[0]
    # normal dephasing
    rho[0,1] *= np.exp(-gamma_env * dt)
    rho[1,0]  = np.conj(rho[0,1])

    current_C = 2 * abs(rho[0,1])

    # DTC instant pruning
    if not triggered and current_C < C_th:
        if np.random.rand() < 0.5:
            rho = np.diag([1.0, 0.0])
        else:
            rho = np.diag([0.0, 1.0])
        triggered = True

    C_dtc[i] = 2 * abs(rho[0,1])

# --------------------------- Plot ---------------------------
plt.figure(figsize=(11,7))
plt.semilogy(times*1e6, C_qm,               color='gray',   lw=2.5, label='QM + decoherence')
plt.semilogy(times*1e6, C_csl_allowed,      color='green',  lw=2.2, label=r'CSL allowed ($\lambda \leq 10^{-11}$ s$^{-1}$)')
plt.semilogy(times*1e6, C_csl_original,     color='lime',   lw=2,   ls='--', label=r'Original CSL ($\lambda = 10^{-17}$ s$^{-1}$)')
plt.semilogy(times*1e6, C_dtc,              color='red',    lw=4,   label='DTC (instant pruning)')

plt.axhline(C_th,      color='orange',  ls='--', lw=2,   label=r'$C_{\rm th} = 10^{-20}$')
plt.axvline(100,       color='blue',    ls=':',  lw=2,   label='100 µs')
plt.axvline(460,       color='red',     ls=':',  lw=3,   label='DTC snap ≈460 µs')
plt.axhline(1e-12,     color='purple', ls='-.', lw=2,   label='2026 projected sensitivity')

plt.ylim(1e-22, 1.1)
plt.xlim(0, 550)
plt.xlabel('Time (µs)', fontsize=14)
plt.ylabel(r'Coherence $C(t) = 2|\rho_{12}(t)|$', fontsize=14)   # ← fixed LaTeX
plt.title('Honest DTC Test – Fully Working & Visible', fontsize=16)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('DTC_test_VISIBLE.png', dpi=400)
plt.show()

# Summary
snap_idx = np.where(C_dtc < 1e-25)[0]
if len(snap_idx) > 0:
    snap_time = times[snap_idx[0]] * 1e6
    print(f"\nDTC snaps to zero at {snap_time:.1f} µs")
    print("Red line is now clearly visible!")
else:
    print("\nNo snap detected (should not happen)")
