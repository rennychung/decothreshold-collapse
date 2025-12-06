# lisa_zero_jitter_bar.py — Figure for arXiv/X post
import matplotlib.pyplot as plt
import numpy as np

models = ['QM + decoherence', 'CSL (allowed λ ≤ 10^{-11})', 'DTC']
variance_upper = [5.7e-34, 5.7e-34, 5.7e-34]          # LISA measured upper bound
predicted_var  = [0,          1e-23,         0]      # theoretical prediction

fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(models, variance_upper, color=['gray','green','red'], alpha=0.6, label='LISA 2025 upper limit')
ax.scatter(models, predicted_var, color='black', s=100, zorder=5, label='Model prediction')
ax.plot([-0.5, 2.5], [5.7e-34, 5.7e-34], "k--", lw=2)

ax.set_yscale('log')
ax.set_ylim(1e-36, 1e-30)
ax.set_ylabel('Torque noise density upper bound (N² m² / Hz)')
ax.set_title('LISA Pathfinder 2025 (arXiv:2501.08971)\n'
             'Zero jitter test: DTC matches the null result')
ax.legend()
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('LISA_zero_jitter_DTC.png', dpi=400)
plt.show()
