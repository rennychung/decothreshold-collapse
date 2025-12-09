# DTC_fair_test_PHYSICALLY_CORRECT.py
# This code adheres strictly to the physical parameters and curve formulas.
# The CSL Allowed (Green) line now perfectly overlaps the QM (Gray) line.
# Visual offsets are only used for the Lime Dashed (Original CSL) and Red (DTC)
# curves to distinguish them from the Gray curve.

import numpy as np
import matplotlib.pyplot as plt

# --- PARAMETERS (PHYSICALLY CORRECT VALUES) ---
gamma_env = 1e5           # s^-1 -> T2 ≈ 10 µs
C_th      = 1e-20         # Coherence threshold for DTC reduction
t_final   = 600e-6        # 600 µs
times     = np.linspace(0, t_final, 5000) # Time array
TIME_OFFSET_MU_S = 10.0   # 10 µs offset for visual separation

# --- MODELS: QM + Decoherence ---
C_qm = np.exp(-gamma_env * times)

# --- MODELS: CSL ---
C_csl_allowed  = np.exp(-(gamma_env + 1e-11) * times)  # Overlaps QM
C_csl_original = np.exp(-(gamma_env + 1e-17) * times)  # Overlaps QM

# --- MODEL: DTC ---
snap_idx = np.where(C_qm < C_th)[0]
if len(snap_idx) > 0:
    first_snap = snap_idx[0]
    snap_time = times[first_snap] * 1e6 # Convert to µs
else:
    first_snap = len(times)
    snap_time = None

C_dtc = np.copy(C_qm)
C_dtc[first_snap:] = 1e-40

# --- PLOTTING ---
plt.figure(figsize=(12, 7.5))
time_mu_s = times * 1e6 

# 1. 2025-allowed CSL (Dark green solid)
csl_allowed_lw = 3.0
csl_allowed_label = (
    r'2025-allowed CSL ($\lambda\leq10^{-11}$ s$^{-1}$)'
    '\n(Physically indistinguishable from QM/Gray curve)'
)
plt.semilogy(time_mu_s, C_csl_allowed, color='green', lw=csl_allowed_lw, ls='-',
             label=csl_allowed_label)

# 2. Original CSL (Lime-green dashed)
csl_original_lw = 2.5
time_offset_csl_original = time_mu_s - TIME_OFFSET_MU_S
plt.semilogy(time_offset_csl_original, C_csl_original, color='limegreen', lw=csl_original_lw, ls='--',
             label=r'Original CSL ($\lambda=10^{-17}$ s$^{-1}$) (Left Track)')

# 3. QM + normal decoherence (Gray solid)
qm_lw = 3.5
plt.semilogy(time_mu_s, C_qm, color='gray', lw=qm_lw, ls='-',
             label='QM + normal decoherence (Central Track)')

# 4. DTC (Red solid + Vertical drop)
dtc_lw = 3.0
if snap_time is not None:
    time_pre_snap = time_mu_s[:first_snap+1]
    coherence_pre_snap = C_dtc[:first_snap+1]

    time_offset_pre_snap = time_pre_snap + TIME_OFFSET_MU_S

    # FIX: "Instant Pruning" -> "Rapid Reduction"
    plt.semilogy(time_offset_pre_snap, coherence_pre_snap,
                 color='red', lw=dtc_lw, ls='-', label='DTC (Rapid Reduction) (Right Track)')

    if first_snap < len(times)-1:
        snap_time_offset = snap_time + TIME_OFFSET_MU_S
        plt.plot([snap_time_offset, snap_time_offset],
                 [C_dtc[first_snap], C_dtc[first_snap+1]],
                 color='red', lw=dtc_lw, ls='-')
        time_offset_post_snap = time_mu_s[first_snap:] + TIME_OFFSET_MU_S
        plt.semilogy(time_offset_post_snap, C_dtc[first_snap:],
                     color='red', lw=dtc_lw, ls='-')
else:
     plt.semilogy(time_mu_s + TIME_OFFSET_MU_S, C_dtc, color='red', lw=dtc_lw, ls='-', label='DTC (no reduction) (Right Track)')


# --- REFERENCE LINES ---
plt.axhline(C_th, color='orange', ls='--', lw=3, label=r'$C_{\rm irr}=10^{-20}$ (Reduction threshold)')
plt.axvline(1e-12, color='purple', ls='-.', lw=3, label='Projected 2026 sensitivity')

if snap_time is not None:
    # FIX: "DTC snap" -> "Reduction Event"
    plt.axvline(snap_time, color='red', ls=':', lw=5,
                label=f'Reduction Event $\\approx{snap_time:.0f}$ $\\mu$s (True time)')


# --- AXIS AND FORMATTING ---
plt.ylim(1e-24, 2)
plt.xlim(0, 600)
plt.xlabel('Time (µs)', fontsize=16)
plt.ylabel(r'Coherence $C(t)=2|\rho_{12}(t)|$', fontsize=16)
# FIX: Formal Title
plt.title('DTC State Reduction vs CSL Decay — Physically Correct Model', fontsize=18)
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, which='both', ls='--', alpha=0.4)
plt.tight_layout()

plt.savefig('DTC_vs_CSL_PHYSICALLY_CORRECT.png', dpi=600, bbox_inches='tight')
plt.savefig('DTC_vs_CSL_PHYSICALLY_CORRECT.pdf', bbox_inches='tight')
plt.show()
