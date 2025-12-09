# FINAL_LISA_PLOT_PERFECTLY_FIXED_4.py
# Generates the final LISA Pathfinder comparison plot (likely Figure 7)

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# === 1. DATA AND SETUP ===
# Renamed CSL label to be explicit about the model's lambda parameter
models = ['Standard QM', r'CSL ($\lambda \leq 10^{-11}$ s$^{-1}$)', 'DTC']
x = np.arange(len(models))

# LISA Upper Limit (Threshold)
upper_limit = 5.7e-34 
y_min_plot = 5e-37 # Bottom of the visible plot axis

# Prediction Values:
# QM and DTC predict 0 (represented by 1e-36 for log scale visibility).
# CSL predicts 10^-23 (ruled out by LISA).
prediction_values = [1e-36, 1e-23, 1e-36] 

# === 2. PLOT GENERATION ===
fig, ax = plt.subplots(figsize=(10, 6))

# --- A. Draw the Upper Limit/Forbidden Region Bars ---
bars = ax.bar(x, [upper_limit] * 3, 
              bottom=y_min_plot, 
              width=0.6, 
              color='lightgray', 
              edgecolor='black', 
              linewidth=2)

# Apply the specific colors based on violation/compatibility
for i, bar in enumerate(bars):
    # CSL (middle bar) is RED because its prediction dot is above the limit (VIOLATED)
    if i == 1:
        bar.set_facecolor('red')
        bar.set_alpha(0.9)
    # QM and DTC are GRAY because their dots are below the limit (COMPATIBLE)
    else:
        bar.set_facecolor('lightgray')
        bar.set_alpha(0.7)


# --- B. Draw the Model Prediction Dots ---
ax.scatter(x, prediction_values, 
            s=300, 
            color='black', 
            edgecolor='white', 
            linewidth=2,
            marker='o',
            zorder=10) 

# --- C. Draw the Actual LISA Upper Limit Line ---
ax.axhline(upper_limit, color='black', linestyle='--', linewidth=3, zorder=5)

# --- D. Configure Axes and Labels ---
ax.set_yscale('log')
ax.set_ylim(y_min_plot, 1e-20) 
ax.set_ylabel(r'Rotational Noise Density ($\rm N^2 m^2 / Hz$)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13)

# FIX: Refined title for a formal scientific tone
ax.set_title('LISA Pathfinder 2025 Noise Limits: Comparison of Standard Models to DTC',
             fontsize=16, pad=20)

# --- E. Custom Legend Creation ---
prediction_patch = plt.Line2D([0], [0], marker='o', color='black', 
                              markerfacecolor='black', markersize=10, 
                              linestyle='', markeredgecolor='white', markeredgewidth=2)
upper_limit_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black', 
                                   label='LISA 2025 upper limit', linewidth=2)

ax.legend([prediction_patch, upper_limit_patch], 
          ['Model Prediction', 'LISA 2025 Upper Limit'],
          fontsize=13, loc='upper right', frameon=True, fancybox=True)

# Grid lines
plt.grid(True, which="both", ls="--", alpha=0.3) 
plt.tight_layout()

# === 3. SAVE AND SHOW ===
plt.savefig('LISA_DTC_PERFECT_REPRODUCED_FINAL.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT_REPRODUCED_FINAL.pdf', bbox_inches='tight')
# plt.show()
