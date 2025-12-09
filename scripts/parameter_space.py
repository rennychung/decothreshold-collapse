# bounds_plot_FIXED_CONCEPT.py

import numpy as np, matplotlib.pyplot as plt

# --- 1. Define Axes ---
Gamma0 = np.logspace(16, 30, 500)
Cth_axis = np.logspace(-25, -5, 500) 
G, C = np.meshgrid(Gamma0, Cth_axis)

plt.figure(figsize=(10, 6)) # Increased size for better presentation

# --- 2. Define Exclusion Boundaries (The "Forbidden" Zones) ---

# Constraint A: Heating/Energy Limit (Diagonal boundary)
# Constraint is: Gamma_0 * C_th > 1e10 (Arbitrary illustrative diagonal limit)
Cth_heating_limit = 1e10 / Gamma0 

# Constraint B: Known Decoherence Limits (Horizontal boundary)
# Cth must be below the limit of our best decoherence experiments (e.g., 1e-15)
Cth_decoherence_limit = 1e-15 

# --- 3. Plot the Forbidden Regions (Red) ---

# Forbidden Zone 1: High Cth (Above the best decoherence limit)
plt.fill_between(Gamma0, Cth_decoherence_limit, Cth_axis.max(), 
                 color='red', alpha=0.3, label='Forbidden (QM/Decoherence Bounds)')

# Forbidden Zone 2: Excessive Heating/Energy (Above the diagonal limit)
# Note: Use np.maximum to ensure the diagonal band is defined correctly.
plt.fill_between(Gamma0, Cth_heating_limit, Cth_axis.max(), 
                 where=(Cth_heating_limit > Cth_axis.min()),
                 color='red', alpha=0.3)

# The Allowed Region (Green) is implicitly below both exclusion zones.
plt.fill_between(Gamma0, Cth_axis.min(), 
                 np.minimum(Cth_decoherence_limit, Cth_heating_limit), 
                 color='#90EE90', alpha=0.7, label='Allowed Region (DTC Compatible)')

# --- 4. Plot the Crosshairs (Chosen Parameters) ---
plt.axvline(1e20, color='blue', ls='--', lw=2, label=r'Chosen $\Gamma_0 = 10^{20}$ s$^{-1}$')
plt.axhline(1e-20, color='purple', ls='--', lw=2, label=r'Chosen $C_{\rm th} = 10^{-20}$')

# --- 5. Setup Axes ---
plt.loglog()
plt.xlim(1e16, 1e30)
plt.ylim(1e-25, 1e-5) 

plt.xlabel(r'Pruning rate $\Gamma_0$ [s$^{-1}$]')
plt.ylabel(r'Coherence threshold $C_{\rm th}$')
plt.title('DTIP Parameter Space vs. Conceptual Experimental Bounds')
plt.legend(loc='lower left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
