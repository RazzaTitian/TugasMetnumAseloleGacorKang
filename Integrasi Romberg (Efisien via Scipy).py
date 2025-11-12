import numpy as np
from scipy.integrate import romberg


# Definisi Fungsi

def f1(x):
    """Soal 1: cos(x)"""
    return np.cos(x)


def f2(x):
    """Soal 2: x^2"""
    return x**2


# Eksekusi Kode

print("MENGGUNAKAN 'scipy.integrate.romberg' UNTUK EFISIENSI")
print("=" * 60 + "\n")

# Soal 1
print("--- Soal 1: integral(cos(x), 0, pi/2) ---")
# Menghitung integral secara langsung
# Scipy akan otomatis menentukan level yang diperlukan
hasil_f1 = romberg(f1, 0, np.pi/2)
print(f"Hasil (default): {hasil_f1:.10f}")

# Menunjukkan tabel internal yang dibuat oleh Scipy
print("\nDemonstrasi 'show=True' untuk Soal 1:")
# Kita set 'divmax=2' agar berhenti di level yang sama (R_2,2)
# divmax=0 -> R_0,0
# divmax=1 -> R_1,1
# divmax=2 -> R_2,2
romberg(f1, 0, np.pi/2, divmax=2, show=True)


print("\n" + "=" * 60 + "\n")

# Soal 2
print("--- Soal 2: integral(x^2, 0, 1) ---")
# Menghitung integral secara langsung
hasil_f2 = romberg(f2, 0, 1)
print(f"Hasil (default): {hasil_f2:.10f}")

# Menunjukkan tabel internal yang dibuat oleh Scipy
print("\nDemonstrasi 'show=True' untuk Soal 2:")
romberg(f2, 0, 1, divmax=2, show=True)

print("\n" + "=" * 60)
print("Catatan: Scipy berhenti lebih awal (Romberg N=2) untuk Soal 2")
print("karena konvergensinya tercapai sangat cepat (hasilnya eksak).")