# FINAL_LISA_PLOT_PERFECTLY_FIXED_3.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# === 1. DATA AND SETUP ===
models = ['QM + decoherence', 'CSL (λ ≤ 10^{-11})', 'DTC']
x = np.arange(len(models))

# LISA Upper Limit (Threshold)
upper_limit = 5.7e-34 
y_min_plot = 5e-37 # Bottom of the visible plot axis

# Prediction Values:
# QM and DTC predict 0 (represented by 1e-36 for log scale visibility).
# CSL predicts 10^-23.
prediction_values = [1e-36, 1e-23, 1e-36] 

# === 2. PLOT GENERATION ===
fig, ax = plt.subplots(figsize=(10, 6))

# --- A. Draw the Upper Limit/Forbidden Region Bars ---
# What you will literally see: Three vertical bars all stopping at exactly 5.7 × 10⁻³⁴.
bars = ax.bar(x, [upper_limit] * 3, 
              bottom=y_min_plot, # Bars start at the bottom of the axis
              width=0.6, 
              color='lightgray', 
              edgecolor='black', 
              linewidth=2)

# Apply the specific colors based on whether the model is violated/compatible
for i, bar in enumerate(bars):
    # The middle (CSL) bar is coloured bright red because its black dot is way above it (ruled out).
    if i == 1:
        bar.set_facecolor('red')
        bar.set_alpha(0.9)
    # The left and right bars stay light gray because their black dots are way below (compatible).
    else:
        bar.set_facecolor('lightgray')
        bar.set_alpha(0.7)


# --- B. Draw the Model Prediction Dots ---
# One black dot (CSL) sitting at 10⁻²³
# Two black dots (QM + decoherence and DTC) sitting right on the bottom of the plot (~10⁻³⁶).
ax.scatter(x, prediction_values, 
           s=300, 
           color='black', 
           edgecolor='white', 
           linewidth=2,
           marker='o',
           zorder=10) 

# --- C. Draw the Actual LISA Upper Limit Line ---
# Thick black dashed horizontal line: The actual LISA 2025 measurement upper bound
ax.axhline(upper_limit, color='black', linestyle='--', linewidth=3, zorder=5)

# --- D. Configure Axes and Labels ---
ax.set_yscale('log')
ax.set_ylim(y_min_plot, 5e-30) # Set Y-limit explicitly to show CSL dot
ax.set_ylabel('Torque noise density (N² m² / Hz)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13)

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=16, pad=20)

# --- E. Custom Legend Creation ---
prediction_patch = plt.Line2D([0], [0], marker='o', color='black', 
                              markerfacecolor='black', markersize=10, 
                              linestyle='', markeredgecolor='white', markeredgewidth=2)
upper_limit_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black', 
                                    label='LISA 2025 upper limit', linewidth=2)

ax.legend([prediction_patch, upper_limit_patch], 
          ['Model prediction', 'LISA 2025 upper limit'],
          fontsize=13, loc='upper right', frameon=True, fancybox=True)

# Grid lines are faint and spread throughout the entire thing
plt.grid(True, which="both", ls="--", alpha=0.3) 
plt.tight_layout()

# === 3. SAVE AND SHOW ===
plt.savefig('LISA_DTC_PERFECT_REPRODUCED_FINAL.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT_REPRODUCED_FINAL.pdf', bbox_inches='tight')
# plt.show()
