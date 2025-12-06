# DTC_fair_test_FINAL_NO_ERRORS.py
# FINAL FIX: Increased the time offset for the three highly overlapping curves (Red, Gray, Lime)
# to 10 µs to guarantee they appear side-by-side, even on the compressed initial axis.

import numpy as np
import matplotlib.pyplot as plt

# --- PARAMETERS ---
gamma_env = 1e5           # s^-1 -> T2 ≈ 10 µs
C_th      = 1e-20         # Coherence threshold for DTC collapse
t_final   = 600e-6        # 600 µs
times     = np.linspace(0, t_final, 5000) # Time array
TIME_OFFSET_MU_S = 10.0   # <-- INCREASED OFFSET for clear visual separation

# --- MODELS: QM + Decoherence ---
C_qm = np.exp(-gamma_env * times)

# --- MODELS: CSL ---
lambda_allowed  = 1e-11
lambda_original = 1e-17
C_csl_allowed  = C_qm * np.exp(-lambda_allowed  * times)
C_csl_original = C_qm * np.exp(-lambda_original * times)

# --- MODEL: DTC (Decoherence-Triggered Collapse) ---
snap_idx = np.where(C_qm < C_th)[0]
if len(snap_idx) > 0:
    first_snap = snap_idx[0]
    snap_time = times[first_snap] * 1e6 # Convert to µs
    print(f"DTC snaps at {snap_time:.1f} µs")
else:
    first_snap = len(times)
    snap_time = None

C_dtc = np.copy(C_qm)
C_dtc[first_snap:] = 1e-40

# --- PLOTTING ---
plt.figure(figsize=(12, 7.5))
time_mu_s = times * 1e6 # Pre-calculate time in µs

# 1. 2025-allowed CSL (Dark green solid) - Plotted first, ZERO OFFSET, high LW to show its split.
csl_allowed_lw = 4.0
plt.semilogy(time_mu_s, C_csl_allowed, color='green', lw=csl_allowed_lw, ls='-',
             label=r'2025-allowed CSL ($\lambda\leq10^{-11}$ s$^{-1}$)')

# 2. Original CSL (Lime-green dashed) - NEGATIVE offset (-10 µs).
csl_original_lw = 3.0
time_offset_csl_original = time_mu_s - TIME_OFFSET_MU_S
plt.semilogy(time_offset_csl_original, C_csl_original, color='limegreen', lw=csl_original_lw, ls='--',
             label=r'Original CSL ($\lambda=10^{-17}$ s$^{-1}$)')

# 3. QM + normal decoherence (Gray solid) - The central, true track (zero offset).
qm_lw = 3.5
plt.semilogy(time_mu_s, C_qm, color='gray', lw=qm_lw, ls='-',
             label='QM + normal decoherence')

# 4. DTC (Red solid + Vertical drop) - POSITIVE offset (+10 µs).
dtc_lw = 3.0
if snap_time is not None:
    # Part A: The curve before snap
    time_pre_snap = time_mu_s[:first_snap+1]
    coherence_pre_snap = C_dtc[:first_snap+1]

    # APPLY POSITIVE TIME OFFSET
    time_offset_pre_snap = time_pre_snap + TIME_OFFSET_MU_S

    plt.semilogy(time_offset_pre_snap, coherence_pre_snap,
                 color='red', lw=dtc_lw, ls='-', label='DTC (instant pruning)')

    # Part B: Instant vertical drop and flat line after snap
    if first_snap < len(times)-1:
        # Note: The snap point for the red line must also be offset.
        snap_time_offset = snap_time + TIME_OFFSET_MU_S
        
        # Vertical drop line (starts from the offset point)
        plt.plot([snap_time_offset, snap_time_offset], 
                 [C_dtc[first_snap], C_dtc[first_snap+1]],
                 color='red', lw=dtc_lw, ls='-')

        # Horizontal line for 'zero' after snap (starts from the offset point)
        time_offset_post_snap = time_mu_s[first_snap:] + TIME_OFFSET_MU_S
        plt.semilogy(time_offset_post_snap, C_dtc[first_snap:],
                     color='red', lw=dtc_lw, ls='-')
else:
     plt.semilogy(time_mu_s + TIME_OFFSET_MU_S, C_dtc, color='red', lw=dtc_lw, ls='-', label='DTC (no snap)')


# --- REFERENCE LINES ---

# Orange dashed horizontal: DTC irreversibility threshold (C_th = 10^-20)
plt.axhline(C_th, color='orange', ls='--', lw=3, label=r'$C_{\rm th}=10^{-20}$ (DTC threshold)')

# Purple dash-dot horizontal: Projected 2026 experimental sensitivity (10^-12)
plt.axhline(1e-12, color='purple', ls='-.', lw=3, label='Projected 2026 sensitivity ($10^{-12}$)')

# Red dotted vertical: Moment DTC snaps (~460 µs) - Marks the TRUE snap time (zero offset)
if snap_time is not None:
    plt.axvline(snap_time, color='red', ls=':', lw=5,
                label=f'DTC snap $\\approx{snap_time:.0f}$ $\\mu$s')


# --- AXIS AND FORMATTING ---
plt.ylim(1e-24, 2)
plt.xlim(0, 600)
plt.xlabel('Time (µs)', fontsize=16)
plt.ylabel(r'Coherence $C(t)=2|\rho_{12}(t)|$', fontsize=16)
plt.title('DTC vs CSL Coherence Decay — Final Visibility Fix (10 µs Offset)', fontsize=18)
plt.legend(fontsize=13, loc='upper right')
plt.grid(True, which='both', ls='--', alpha=0.4)
plt.tight_layout()

# --- SAVE AND SHOW ---
plt.savefig('DTC_vs_CSL_TRACKS_FINAL_PERFECT.png', dpi=600, bbox_inches='tight')
plt.savefig('DTC_vs_CSL_TRACKS_FINAL_PERFECT.pdf', bbox_inches='tight')
plt.show()
