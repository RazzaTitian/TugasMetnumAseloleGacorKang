import numpy as np

def compute_R22(f, a, b):
    """
    Menghitung integral Poin 1 sampai level R_2,2
    dengan menghitung nilai perantara satu per satu
    """
    
    print(f"--- Menghitung R_2,2 untuk {f.__name__} ---\n")
    
    # BAGIAN 1: "Dengan Trapezoidal Rule R_0,0..."
    # Menghitung 3 nilai Trapesium (Kolom 1)

    print("1. Menghitung nilai Trapesium (Kolom 1):")

    # Hitung R_0,0 (n=1)
    h0 = b - a
    R00 = 0.5 * h0 * (f(a) + f(b))
    print(f"   R_0,0 (n=1) = {R00:.10f}")
    
    # Hitung R_1,0 (n=2) secara efisien dari R_0,0
    h1 = h0 / 2.0
    R10 = 0.5 * R00 + h1 * f(a + h1)
    print(f"   R_1,0 (n=2) = {R10:.10f}")

    # Hitung R_2,0 (n=4) secara efisien dari R_1,0
    h2 = h1 / 2.0
    sum_f = f(a + h2) + f(a + 3*h2) # Titik baru: 1h dan 3h
    R20 = 0.5 * R10 + h2 * sum_f
    print(f"   R_2,0 (n=4) = {R20:.10f}")

    # BAGIAN 2: "...minimal 3 level sampai R_2,2"
    # Menghitung nilai ekstrapolasi (Kolom 2 & 3)

    print("\n2. Menghitung nilai Ekstrapolasi (Kolom 2 & 3):")

    # Hitung R_1,1 (Kolom 2)
    R11 = (4.0 * R10 - R00) / 3.0
    print(f"   R_1,1 (Kolom 2) = {R11:.10f}")
    
    # Hitung R_2,1 (Kolom 2)
    R21 = (4.0 * R20 - R10) / 3.0
    print(f"   R_2,1 (Kolom 2) = {R21:.10f}")
    
    # Hitung R_2,2 (Kolom 3) - Ini target kita
    # R(2,2) = (16*R(2,1) - R(1,1)) / 15
    R22 = (16.0 * R21 - R11) / 15.0
    print(f"   R_2,2 (Kolom 3) = {R22:.10f}")

    # HASIL AKHIR
    print(f"\nHASIL AKHIR (R_2,2): {R22:.10f}")
    print("\n")
    
    return R22

# --- FUNGSI-FUNGSI DARI SOAL ---
def f1(x):
    """Soal 1: cos(x)"""
    return np.cos(x) 

def f2(x):
    """Soal 2: x^2"""
    return x**2      

# --- Eksekusi Soal 1 ---
computeNo1 = compute_R22(f1, 0, np.pi/2)

# --- Eksekusi Soal 2 ---
computeNo2 = compute_R22(f2, 0, 1)