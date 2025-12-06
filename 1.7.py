# FINAL_LISA_PLOT_PERFECTLY_FIXED_2.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# === 1. DATA AND SETUP ===
models = ['QM + decoherence', 'CSL (λ ≤ 10^{-11})', 'DTC']
x = np.arange(len(models))

# LISA Upper Limit (Threshold)
upper_limit = 5.7e-34 
y_min_plot = 5e-37 # Bottom of the plot

# What you will literally see: Three big black circles
# QM and DTC predict 0, represented by 1e-36 (right on the bottom axis)
# CSL predicts 1e-23 (far above the limit)
prediction_values = [1e-36, 1e-23, 1e-36] 

# === 2. PLOT GENERATION ===
fig, ax = plt.subplots(figsize=(10, 6))

# --- A. Draw the Bar Background (to represent the maximum height of the valid/invalid region) ---
# We use the y_max_plot for the bar height to visually fill the space.
y_max_bar = 5e-30 

bars = ax.bar(x, [y_max_bar] * 3, 
              bottom=y_min_plot, 
              width=0.6, 
              color='lightgray', 
              edgecolor='black', 
              linewidth=2)

# Set the appearance for the bars to match the image precisely
for i, bar in enumerate(bars):
    # What you will literally see: Three tall light-gray rectangles (Background)
    bar.set_facecolor('lightgray')
    bar.set_alpha(0.7)
    
    # Element in the plot: Middle bar turns bright red (CSL is violated)
    if i == 1:
        # What you will literally see: Middle bar is screaming red
        bar.set_facecolor('red')
        bar.set_alpha(0.9)


# --- B. Draw the Model Prediction Dots ---
# Element in the plot: Three big black circles
# The dots are correctly placed at 1e-36 (for QM/DTC) and 1e-23 (for CSL)
ax.scatter(x, prediction_values, 
           s=300, 
           color='black', 
           edgecolor='white', 
           linewidth=2,
           marker='o',
           zorder=10) # Ensure dots are on top

# --- C. Draw the Actual LISA Upper Limit Line ---
# Element in the plot: Thick black dashed horizontal line
ax.axhline(upper_limit, color='black', linestyle='--', linewidth=3, zorder=5)

# --- D. Configure Axes and Labels ---
ax.set_yscale('log')
ax.set_ylim(y_min_plot, y_max_bar) 
ax.set_ylabel('Torque noise density (N² m² / Hz)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13)

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=16, pad=20)

# --- E. Custom Legend Creation (Ensures correct visual linkage) ---
# Create patch objects to represent the bar and dot styles
prediction_patch = plt.Line2D([0], [0], marker='o', color='black', 
                              markerfacecolor='black', markersize=10, 
                              linestyle='', markeredgecolor='white', markeredgewidth=2)
upper_limit_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black', 
                                    label='LISA 2025 upper limit', linewidth=2)

ax.legend([prediction_patch, upper_limit_patch], 
          ['Model prediction', 'LISA 2025 upper limit'],
          fontsize=13, loc='upper right', frameon=True, fancybox=True)


# What you will literally see: The background grey lines are spread throughout in a very faint color
plt.grid(True, which="both", ls="--", alpha=0.3) 
plt.tight_layout()

# === 3. SAVE AND SHOW ===
plt.savefig('LISA_DTC_PERFECT_REPRODUCED_FINAL.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT_REPRODUCED_FINAL.pdf', bbox_inches='tight')
# plt.show()
