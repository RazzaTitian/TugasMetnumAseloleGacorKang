import numpy as np

# =============================================================================
# DEFINISI FUNGSI (Menggunakan NumPy)
# =============================================================================

def f1(x):
    """Fungsi pertama dari soal: cos(x)"""
    return np.cos(x)

def f2(x):
    """Fungsi kedua dari soal: x^2"""
    return x**2

# =============================================================================
# ALGORITMA ADAPTIVE SIMPSON (Logika Inti Tetap Sama)
# =============================================================================

def _rekursi_simpson(f, a, b, tol, fa, fm, fb, level, max_level):
    """
    Fungsi helper rekursif (inti dari algoritma).
    Logika ini bekerja pada skalar, jadi tidak ada perubahan.
    """
    
    m = (a + b) / 2
    h = b - a
    S_kasar = (h / 6) * (fa + 4 * fm + fb)

    # Hitung 2 titik baru di sub-interval
    ml = (a + m) / 2
    mr = (m + b) / 2
    fml = f(ml)
    fmr = f(mr)

    # S_halus adalah jumlah dari Simpson di [a, m] dan [m, b]
    S_halus = (h / 12) * (fa + 4 * fml + 2 * fm + 4 * fmr + fb)

    # Estimasi Error
    error = (1 / 15) * abs(S_halus - S_kasar)

    # Cek Batas Rekursi
    if level > max_level:
        return S_halus

    # Cek Toleransi
    if error < tol:
        # Kembalikan S_halus + koreksi Ekstrapolasi Richardson
        return S_halus + (S_halus - S_kasar) / 15
    else:
        # Jika error terlalu besar, bagi interval jadi dua
        tol_setengah = tol / 2
        
        # Rekursi sisi kiri [a, m]
        kiri = _rekursi_simpson(f, a, m, tol_setengah, fa, fml, fm, level + 1, max_level)
        
        # Rekursi sisi kanan [m, b]
        kanan = _rekursi_simpson(f, m, b, tol_setengah, fm, fmr, fb, level + 1, max_level)
        
        return kiri + kanan

def integral_adaptif_simpson(f, a, b, tol=1e-8, max_recursion=20):
    """
    Fungsi utama (wrapper) untuk Adaptive Simpson's Integration.
    """
    print(f"\n--- Menghitung Integral {f.__name__} dari {a} sampai {b} ---")
    print(f"--- Toleransi Error: {tol} ---")
    
    # Hitung 3 titik awal
    m = (a + b) / 2
    fa = f(a)
    fm = f(m)
    fb = f(b)
    
    # Mulai rekursi
    hasil = _rekursi_simpson(f, a, b, tol, fa, fm, fb, 0, max_recursion)
    
    print(f"Hasil Integral Numerik: {hasil}")
    return hasil

# =============================================================================
# EKSEKUSI PROGRAM
# =============================================================================
if __name__ == "__main__":
    
    tolerance = 1e-9

    # --- Soal 1: Integral cos(x) dx from 0 to pi/2 ---
    a1 = 0
    b1 = np.pi / 2  # <-- Menggunakan NumPy
    hasil_eksak_1 = 1.0
    
    hasil_integral_1 = integral_adaptif_simpson(f1, a1, b1, tol=tolerance)
    error_1 = abs(hasil_integral_1 - hasil_eksak_1)
    
    print(f"Hasil Eksak (cos(x)): {hasil_eksak_1}")
    print(f"Error Aktual: {error_1}")
    print("-" * 50)

    # --- Soal 2: Integral x^2 dx from 0 to 1 ---
    a2 = 0
    b2 = 1
    hasil_eksak_2 = 1/3
    
    hasil_integral_2 = integral_adaptif_simpson(f2, a2, b2, tol=tolerance)
    error_2 = abs(hasil_integral_2 - hasil_eksak_2)

    print(f"Hasil Eksak (x^2): {hasil_eksak_2}")
    print(f"Error Aktual: {error_2}")
    print("-" * 50)