import numpy as np
from scipy import integrate

# --- Fungsi 1: I_1 = integral(cos(x)) from 0 to pi/2 ---
(result_I1, err_I1) = integrate.quad(np.cos, 0, np.pi/2)

# --- Fungsi 2: I_2 = integral(x^2) from 0 to 1 ---
(result_I2, err_I2) = integrate.quad(lambda x: x**2, 0, 1)

print(f"Hasil Quad I_1 (cos(x)): {result_I1:.16f} (Galat: {err_I1:.2e})")
print(f"Hasil Quad I_2 (x^2):     {result_I2:.16f} (Galat: {err_I2:.2e})")