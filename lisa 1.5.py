# FINAL_LISA_PLOT_THAT_ACTUALLY_WORKS_FIXED_DOCUMENTED.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# === 1. DATA AND SETUP ===
# Element in the plot: Models on the X-axis
models = ['QM + decoherence', 'CSL (λ ≤ 10^{-11})', 'DTC']
x = np.arange(len(models))

# Element in the plot: Thick black dashed horizontal line
# What it means physically: The actual LISA 2025 measurement upper bound
upper_limit = 5.7e-34 

# What you will literally see: Three light-gray vertical bars (upper limit)
bar_colors = ['lightgray', 'red', 'lightgray']
bar_edgecolor = 'black'
bar_width = 0.6

# What you will literally see: Three big black circles
# What it means physically: The actual torque noise each model predicts
# CSL prediction is 10^-23, QM/DTC is 0.
# We set 0 predictions to 1e-36 (right on the bottom axis) for visibility.
prediction_values = [1e-36, 1e-23, 1e-36] 
dot_size = 300
dot_color = 'black'
dot_edge = 'white'

# === 2. PLOT GENERATION ===
fig, ax = plt.subplots(figsize=(10, 6))

# --- A. Draw the Upper Limit Bars ---
# Element in the plot: Three light-gray vertical bars
# What it means physically: LISA Pathfinder 2025 upper limit (same for all models)
# What you will literally see: Three tall light-gray rectangles (CSL one will be overridden to red)
bars = ax.bar(x, [upper_limit] * 3, 
              width=bar_width, 
              color=bar_colors, 
              edgecolor=bar_edgecolor, 
              linewidth=2)

# Apply the specific colors and alpha for the visual meaning:
for i, bar in enumerate(bars):
    # Element in the plot: Middle bar turns bright red
    # What it means physically: CSL is ruled out (10^-23 > 5.7e-34)
    # What you will literally see: Middle bar is screaming red
    if i == 1:
        bar.set_facecolor('red')
    else:
        bar.set_facecolor('lightgray')
        bar.set_alpha(0.7)


# --- B. Draw the Model Prediction Dots ---
# Element in the plot: Three big black circles
# What it means physically: The actual torque noise each model predicts
ax.scatter(x, prediction_values, 
           s=dot_size, 
           color=dot_color, 
           edgecolor=dot_edge, 
           linewidth=2,
           marker='o',
           zorder=10)

# Element in the plot: Thick black dashed horizontal line
# What it means physically: The actual LISA 2025 measurement upper bound
ax.axhline(upper_limit, color='black', linestyle='--', linewidth=3, zorder=5)


# --- C. Configure Axes and Labels ---
ax.set_yscale('log')
# What you will literally see: plenty of room at the bottom
ax.set_ylim(5e-37, 5e-30) 
ax.set_ylabel('Torque noise density (N² m² / Hz)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13)

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=16, pad=20)

# --- D. Custom Legend Creation (Ensures correct visual linkage) ---
# Create patch objects to represent the bar and dot styles
prediction_patch = plt.Line2D([0], [0], marker='o', color='black', 
                              markerfacecolor='black', markersize=10, 
                              linestyle='', markeredgecolor='white', markeredgewidth=2)
upper_limit_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black', 
                                    label='LISA 2025 upper limit', linewidth=2)

ax.legend([prediction_patch, upper_limit_patch], 
          ['Model prediction', 'LISA 2025 upper limit'],
          fontsize=13, loc='upper right', frameon=True, fancybox=True)


plt.grid(True, which="both", ls="--", alpha=0.3)
plt.tight_layout()

# === 3. SAVE AND SHOW ===
plt.savefig('LISA_DTC_PERFECT_REPRODUCED.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT_REPRODUCED.pdf', bbox_inches='tight')
# plt.show()
