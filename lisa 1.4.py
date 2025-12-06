# FINAL_LISA_PLOT_THAT_ACTUALLY_WORKS_FIXED.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# === 1. DATA AND SETUP ===
models = ['QM + decoherence', 'CSL (λ ≤ 10^{-11})', 'DTC']
x = np.arange(len(models))

# LISA Upper Limit (Threshold)
upper_limit = 5.7e-34 

# Model Prediction Values (Torque Noise Density)
# QM and DTC predict 0 (null result), CSL predicts a value that violates the limit.
# The dots for 0 are plotted with a small offset (1e-36) for visibility.
prediction_values_for_dots = [1e-36, 1e-23, 1e-36] # Actual data for scatter plot
prediction_colors = ['black', 'black', 'black']
prediction_markers = ['o', 'o', 'o']

# === 2. PLOT GENERATION ===
fig, ax = plt.subplots(figsize=(10, 6))

# --- A. Draw the Upper Limit Bars (Gray and Red) ---
# The bar height is just the upper limit value.
# The CSL bar is drawn bright red because it is VIOLATED by the CSL prediction.
bar_colors = ['lightgray', 'red', 'lightgray']
bar_hatches = ['', '', ''] # Use solid fill

bars = ax.bar(x, [upper_limit] * 3, 
              width=0.6, 
              color=bar_colors, 
              edgecolor='black', 
              linewidth=2)

# Set the appearance for the gray bars to match the image precisely
for bar in bars:
    bar.set_facecolor('lightgray')
    bar.set_alpha(0.7) # Added slight alpha for better visualization

# --- B. Draw the Model Prediction Dots (Black Circles) ---
ax.scatter(x, prediction_values_for_dots, 
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
ax.set_ylim(5e-37, 5e-30) 
ax.set_ylabel('Torque noise density (N² m² / Hz)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13) # Removed rotation for clarity

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=16, pad=20)

# --- E. Custom Legend Creation (The key fix) ---
# Create patch objects to represent the bar and dot styles
prediction_patch = plt.Line2D([0], [0], marker='o', color='black', 
                              markerfacecolor='black', markersize=10, 
                              linestyle='', markeredgecolor='white', markeredgewidth=2)
upper_limit_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black', 
                                    label='LISA 2025 upper limit', linewidth=2)

# Use the custom patches in the legend call
ax.legend([prediction_patch, upper_limit_patch], 
          ['Model prediction', 'LISA 2025 upper limit'],
          fontsize=13, loc='upper right', frameon=True, fancybox=True)


plt.grid(True, which="both", ls="--", alpha=0.3)
plt.tight_layout()

# === 3. SAVE AND SHOW ===
plt.savefig('LISA_DTC_PERFECT_REPRODUCED.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT_REPRODUCED.pdf', bbox_inches='tight')
# plt.show() # Uncomment to display the plot
