import numpy as np

def f1(x):
    """Fungsi untuk soal pertama"""
    return np.cos(x)

def f2(x):
    """Fungsi untuk soal kedua"""
    return x**2

def simpson_rule(f, a, b):
    """
    Menghitung aturan Simpson 1/3 pada interval [a, b].
    """
    h = (b - a) / 2
    c = (a + b) / 2
    return (h / 3) * (f(a) + 4 * f(c) + f(b))

def adaptive_integration(f, a, b, tol, level=0, max_level=15):
    """
    Menghitung integral f(x) dari a ke b dengan toleransi 'tol'
    menggunakan Adaptive Simpson's Rule.
    """
    
    # Mencegah rekursi tak terbatas
    if level > max_level:
        print("Peringatan: Level rekursi maksimum tercapai.")
        return simpson_rule(f, a, b)

    # 1. Hitung S(a, b)
    S_ab = simpson_rule(f, a, b)
    
    # 2. Hitung S(a, c) + S(c, b)
    c = (a + b) / 2
    S_ac = simpson_rule(f, a, c)
    S_cb = simpson_rule(f, c, b)
    S_sub = S_ac + S_cb
    
    # 3. Hitung estimasi error
    # Faktor 1/15 berasal dari perbandingan orde error O(h^4) dan O(h^5)
    # |S_sub - S_ab| adalah estimasi untuk error di S_ab, 
    # dan error di S_sub (yang lebih akurat) adalah sekitar 1/15 kalinya.
    error_estimate = (1/15) * abs(S_sub - S_ab)
    
    # 4. Cek kondisi toleransi
    if error_estimate < tol:
        # Hasil S_sub lebih akurat, jadi kita kembalikan S_sub.
        # Kadang ditambahkan koreksi (S_sub - S_ab)/15, tapi S_sub saja
        # sudah merupakan aproksimasi yang sangat baik.
        return S_sub
    else:
        # Jika error terlalu besar, ulangi secara rekursif
        # pada dua sub-interval dengan toleransi dibagi dua.
        I_left = adaptive_integration(f, a, c, tol / 2, level + 1, max_level)
        I_right = adaptive_integration(f, c, b, tol / 2, level + 1, max_level)
        
        return I_left + I_right

# --- Menjalankan Perhitungan ---

# Set toleransi
tolerance = 1e-7

# --- Soal 1 ---
integral_1 = adaptive_integration(f1, 0, np.pi/2, tolerance)
solusi_eksak_1 = 1.0
error_1 = abs(integral_1 - solusi_eksak_1)

print("--- Soal 1: I = integral(cos(x) dx) from 0 to pi/2 ---")
print(f"Solusi Eksak   : {solusi_eksak_1}")
print(f"Hasil Numerik    : {integral_1}")
print(f"Error Absolut    : {error_1}")
print("-" * 50)


# --- Soal 2 ---
integral_2 = adaptive_integration(f2, 0, 1, tolerance)
solusi_eksak_2 = 1/3
error_2 = abs(integral_2 - solusi_eksak_2)

print("--- Soal 2: I = integral(x^2 dx) from 0 to 1 ---")
print(f"Solusi Eksak   : {solusi_eksak_2}")
print(f"Hasil Numerik    : {integral_2}")
print(f"Error Absolut    : {error_2}")
print("-" * 50)