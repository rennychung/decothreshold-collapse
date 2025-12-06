# dtc_cat_test_FINAL_WORKING.py
# Copy-paste → run → you get the figure immediately
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# REALISTIC 2025–2030 cat-state parameters
# ------------------------------------------------------------------
Delta_x = 100e-9          # 100 nm separation (already done in labs)
sigma_x = 5e-9            # ground-state width
gamma_env = 1e4           # s^-1 — typical environmental decoherence
C_th = 1e-20              # DTC irreversibility threshold

t_final = 0.15            # seconds
steps = 12000
times = np.linspace(0, t_final, steps)
dt = times[1] - times[0]

# ------------------------------------------------------------------
# Position grid and initial cat state
# ------------------------------------------------------------------
x = np.linspace(-400e-9, 400e-9, 2000)
dx = x[1] - x[0]

psi_L = np.exp(-(x + Delta_x/2)**2 / (4*sigma_x**2))
psi_R = np.exp(-(x - Delta_x/2)**2 / (4*sigma_x**2))

# Normalise each packet
psi_L /= np.sqrt(np.sum(np.abs(psi_L)**2) * dx)
psi_R /= np.sqrt(np.sum(np.abs(psi_R)**2) * dx)

# Cat state
psi_cat = (psi_L + psi_R) / np.sqrt(2)

# ------------------------------------------------------------------
# Coherence measure
# ------------------------------------------------------------------
def coherence(psi):
    rho = np.outer(psi, psi.conj())
    return np.sum(np.abs(rho - np.diag(np.diag(rho)))) * dx

# ------------------------------------------------------------------
# DTC simulation
# ------------------------------------------------------------------
psi = psi_cat.copy()
C_dtc = [coherence(psi)]
triggered = False
t_trigger = None

decay_factor = np.exp(-gamma_env * (Delta_x**2) * dt / (4*sigma_x**2))

for i in range(1, steps):
    C = C_dtc[-1] * decay_factor
    
    if not triggered and C < C_th:
        # Instant collapse
        psi = psi_L if np.random.rand() < 0.5 else psi_R
        psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)
        triggered = True
        t_trigger = times[i]
    
    C_dtc.append(coherence(psi) if triggered else C)

# Pure decoherence (no collapse)
C_deco = [coherence(psi_cat)]
for i in range(1, steps):
    C_deco.append(C_deco[-1] * decay_factor)

# ------------------------------------------------------------------
# PLOT
# ------------------------------------------------------------------
plt.figure(figsize=(11, 8))

# Top panel: final wavefunction
plt.subplot(2,1,1)
plt.plot(x*1e9, np.abs(psi_cat)**2, 'k--', lw=2, label='Initial cat state')
plt.plot(x*1e9, np.abs(psi)**2, 'red', lw=3, label='DTC final state')
plt.xlabel('Position (nm)')
plt.ylabel(r'$|\psi(x)|^2$')
plt.title('DTC: Macroscopic Cat State → Instant Tail-Free Collapse')
plt.legend()
plt.grid(alpha=0.3)

# Bottom panel: coherence vs time
plt.subplot(2,1,2)
plt.semilogy(times, C_dtc, 'blue', lw=3, label='DTC')
plt.semilogy(times, C_deco, 'gray', lw=2, ls='--', label='Pure decoherence')
plt.axhline(C_th, color='orange', ls='--', label=r'$C_{\rm th}=10^{-20}$')
if t_trigger:
    plt.axvline(t_trigger, color='red', ls=':', lw=3, label=f'Collapse at t={t_trigger:.1e}s')
plt.xlabel('Time (s)')
plt.ylabel('Coherence')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('dtc_cat_test.png', dpi=400)
plt.savefig('dtc_cat_test.pdf')
plt.show()

print("Figure saved as dtc_cat_test.png and .pdf")
if t_trigger:
    print(f"DTC collapse triggered at t = {t_trigger:.2e} seconds")
