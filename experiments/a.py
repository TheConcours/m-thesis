import numpy as np
import qutip as qt
import matplotlib.pyplot as plt
from scipy.special import erf

# --- System Parameters ---
N = 3  # Truncate to Qutrit to model leakage
w_c = 2 * np.pi * 5.0  # Control frequency (GHz)
alpha_c = 2 * np.pi * -0.3  # Control anharmonicity
w_t = 2 * np.pi * 4.8  # Target frequency (GHz)
alpha_t = 2 * np.pi * -0.3  # Target anharmonicity
J = 2 * np.pi * 0.02  # Static capacitive coupling
w_d = w_t  # CR Drive frequency

# --- Operators ---
a = qt.tensor(qt.destroy(N), qt.qeye(N))
b = qt.tensor(qt.qeye(N), qt.destroy(N))

# Leakage projection operator for the control qubit: |2><2|
proj_2_c = qt.tensor(qt.basis(N, 2) * qt.basis(N, 2).dag(), qt.qeye(N))

# --- Static Hamiltonian ---
H0 = (
    w_c * a.dag() * a
    + 0.5 * alpha_c * a.dag() * a.dag() * a * a
    + w_t * b.dag() * b
    + 0.5 * alpha_t * b.dag() * b.dag() * b * b
    + J * (a.dag() * b + a * b.dag())
)

H_drive = a + a.dag()

# --- Pulse Envelopes ---
t_gate = 150.0  # Total gate time (ns)
tlist = np.linspace(0, t_gate, 1000)

# 1. Truncated Gaussian
# Truncated at +/- 2 sigma, causing abrupt edges at t=0 and t=t_gate
sigma_g = t_gate / 4.0
amp_g = 2 * np.pi * 0.04


def gaussian_env(t, args):
    env = amp_g * np.exp(-0.5 * ((t - t_gate / 2) / sigma_g) ** 2)
    return env * np.cos(w_d * t)


# 2. Flat-Top Gaussian (Error Function based)
# Smooth ramp up, hold plateau, smooth ramp down
amp_f = 2 * np.pi * 0.04
sigma_edge = 10.0  # Ramp width in ns


def flattop_env(t, args):
    # Constructing a smooth pulse using error functions
    rise = 0.5 * (1 + erf((t - 3 * sigma_edge) / sigma_edge))
    fall = 0.5 * (1 + erf((t_gate - t - 3 * sigma_edge) / sigma_edge))
    env = amp_f * (rise * fall)
    return env * np.cos(w_d * t)


# Build time-dependent Hamiltonians
H_g = [H0, [H_drive, gaussian_env]]
H_f = [H0, [H_drive, flattop_env]]

# --- Simulation ---
# Initial state: |0,0>
psi0 = qt.tensor(qt.basis(N, 0), qt.basis(N, 0))

# Evolve the system, requesting the expectation value of the leakage operator
res_g = qt.mesolve(H_g, psi0, tlist, e_ops=[proj_2_c])
res_f = qt.mesolve(H_f, psi0, tlist, e_ops=[proj_2_c])

# --- Plotting ---
plt.figure(figsize=(10, 5))
plt.plot(
    tlist, res_g.expect[0], label="Truncated Gaussian Leakage", color="red", linewidth=2
)
plt.plot(
    tlist, res_f.expect[0], label="Flat-top Gaussian Leakage", color="blue", linewidth=2
)
plt.axhline(0, color="black", linewidth=0.5)
plt.xlabel("Time (ns)")
plt.ylabel(r"Control Qubit $|2\rangle$ Population ($P_2$)")
plt.title("CR Gate Leakage Dynamics: Truncated Gaussian vs Flat-top")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
