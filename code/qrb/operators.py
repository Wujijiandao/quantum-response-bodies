import numpy as np

I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[-1, 0], [0, 1]], dtype=complex)  # |g>, |e>
sigma_plus = np.array([[0, 0], [1, 0]], dtype=complex)   # |e><g|
sigma_minus = sigma_plus.conj().T                       # |g><e|
proj_e = sigma_plus @ sigma_minus

def kron(a, b):
    return np.kron(a, b)

SP1SM2 = kron(sigma_plus, sigma_minus)
N1 = kron(proj_e, I2)
N2 = kron(I2, proj_e)
