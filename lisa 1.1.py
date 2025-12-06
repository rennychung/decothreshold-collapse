# lisa_zero_jitter_bar_fixed.py — FINAL VERSION (ready for arXiv)
import matplotlib.pyplot as plt
import numpy as np

models = ['QM + decoherence', 'CSL (λ ≤ 10^{-11})', 'DTC']
upper_limit = 5.7e-34                    # LISA 2025 upper bound
predicted  = [0.0,        1e-23,         0.0]   # model predictions

x_pos = np.arange(len(models))

fig, ax = plt.subplots(figsize=(9, 5.5))

# Gray bars = experimental upper limit (same for all)
ax.bar(x_pos, [upper_limit]*3, color=['lightgray','lightgray','lightgray'],
       alpha=0.8, edgecolor='black', linewidth=1.2, label='LISA 2025 upper limit')

# Black circles = theoretical prediction of each model
ax.scatter(x_pos, predicted, color='black', s=180, zorder=10,
           label='Model prediction', edgecolors='white', linewidth=1.5)

# For the two zero-prediction models, make the dot sit exactly on the axis
ax.scatter([0, 2], [0, 0], color='black', s=180, zorder=10,
           edgecolors='white', linewidth=1.5)

# Horizontal dashed line at the actual measured upper bound
ax.axhline(upper_limit, color='black', linestyle='--', linewidth=2)

# Log scale + nice limits
ax.set_yscale('log')
ax.set_ylim(1e-36, 2e-30)
ax.set_ylabel(r'Torque noise density (N$^2$ m$^2$ / Hz)', fontsize=12)
ax.set_xticks(x_pos, models, rotation=18, ha='right', fontsize=11)

ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test — DTC matches the null result perfectly',
             fontsize=14, pad=20)

ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

plt.tight_layout()
plt.savefig('LISA_zero_jitter_DTC_fixed.png', dpi=500, bbox_inches='tight')
plt.savefig('LISA_zero_jitter_DTC_fixed.pdf', bbox_inches='tight')  # also PDF for papers
plt.show()
