# bounds_plot.py
# Generates Figure 4 of the DTIP paper (experimental constraints 2025)
import numpy as np, matplotlib.pyplot as plt

Gamma0 = np.logspace(15, 30, 500)
Cth    = np.logspace(-25, -10, 500)
G, C = np.meshgrid(Gamma0, Cth)

plt.figure(figsize=(6.4, 4.8))
plt.fill_between(Gamma0, 1e-25, 1e-8, color='#90EE90', alpha=0.7, label='Allowed region (2025)')
plt.axvline(1e20, color='red', ls='--', lw=2, label=r'Chosen $\Gamma_0 = 10^{20}$ s$^{-1}$')
plt.axhline(1e-20, color='darkorange', ls='--', lw=2, label=r'Chosen $C_{\rm th} = 10^{-20}$')
plt.loglog()
plt.xlim(1e16, 1e30); plt.ylim(1e-25, 1e-9)
plt.xlabel(r'Pruning rate $\Gamma_0$ [s$^{-1}$]')
plt.ylabel(r'Coherence threshold $C_{\rm th}$')
plt.title('DTIP parameter space vs. 2025 experimental bounds')
plt.legend(loc='lower left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('bounds_plot.pdf', dpi=300)
plt.show()
