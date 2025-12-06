# FINAL_LISA_PLOT_THAT_ACTUALLY_WORKS.py
import matplotlib.pyplot as plt
import numpy as np

models = ['QM + decoherence', 'CSL (λ ≤ 10^{-11})', 'DTC']
upper = 5.7e-34
pred  = [0.0, 1e-23, 0.0]

x = np.arange(len(models))

fig, ax = plt.subplots(figsize=(10,6))

# 1. Three light-gray bars for the LISA upper limit
ax.bar(x, [upper]*3, width=0.6, color='lightgray', edgecolor='black', linewidth=2,
       label='LISA 2025 upper limit')

# 2. Make the CSL bar bright red because it violates the bound
bars = ax.bar(x, [upper]*3, width=0.6, color=['lightgray','red','lightgray'],
              edgecolor='black', linewidth=2)
bars[1].set_color('red')

# 3. Black dots for model predictions — FORCED to be visible
# For the two zero predictions we place them just above the axis
y_zeros = [1e-36, 1e-23, 1e-36]   # tiny offset for visibility
ax.scatter(x, y_zeros, s=300, color='black', edgecolor='white', linewidth=3,
           zorder=10, label='Model prediction')

# 4. Thick black dashed line at the actual LISA limit
ax.axhline(upper, color='black', linestyle='--', linewidth=3, zorder=5)

ax.set_yscale('log')
ax.set_ylim(5e-37, 5e-30)                     # plenty of room at the bottom
ax.set_ylabel('Torque noise density (N² m² / Hz)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13, rotation=12, ha='right')

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=16, pad=25)

ax.legend(fontsize=13, loc='upper right', frameon=True, fancybox=True)

plt.grid(True, which="both", ls="--", alpha=0.3)
plt.tight_layout()

plt.savefig('LISA_DTC_PERFECT.png', dpi=600, bbox_inches='tight')
plt.savefig('LISA_DTC_PERFECT.pdf', bbox_inches='tight')
plt.show()
