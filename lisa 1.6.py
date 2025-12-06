# FINAL_LISA_PLOT_PERFECTLY_FIXED.py
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
prediction_values = [1e-36, 1e-23, 1e-36] # 1e-36 is used to represent 0 on log scale

# === 2. PLOT GENERATION ===
fig, ax = plt.subplots(figsize=(10, 6))

# --- A. Draw the Upper Limit/Forbidden Region Bars ---
# The bars must span the distance from the upper limit line (5.7e-34) down to the bottom of the plot.
# We draw the bars from the y_min_plot up to the upper_limit to fill the area.
# Height of the bar on a log scale plot needs careful handling, but we draw a single patch for the shaded region.

# Draw a single large rectangle for the upper limit area for clarity, and then override colors.
bars = ax.bar(x, [upper_limit] * 3, 
              bottom=y_min_plot, # Start the bar from the bottom of the visible axis
              width=0.6, 
              color='lightgray', 
              edgecolor='black', 
              linewidth=2)

# Set the appearance for the bars to match the image precisely
for i, bar in enumerate(bars):
    # What you will literally see: Three light-gray rectangles (Background)
    bar.set_facecolor('lightgray')
    bar.set_alpha(0.7)
    
    # Element in the plot: Middle bar turns bright red
    if i == 1:
        # What you will literally see: Middle bar is screaming red
        bar.set_facecolor('red')
        bar.set_alpha(0.9)


# --- B. Draw the Model Prediction Dots ---
# Element in the plot: Three big black circles
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
ax.set_ylim(y_min_plot, 5e-30) # Set Y-limit explicitly
ax.set_ylabel('Torque noise density (N² m² / Hz)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13)

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=16, pad=20)

# --- E. Custom Legend Creation ---
# Create patch objects to represent the bar and dot styles
# The bar in the legend should look gray (representing the general upper limit)
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
plt.savefig('LISA_DTC_PERFECT_REPRODUCED.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT_REPRODUCED.pdf', bbox_inches='tight')
# plt.show()
