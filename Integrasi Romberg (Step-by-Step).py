import numpy as np


def trapesium(f, a, b, n):
    """
    Menghitung integral komposit menggunakan aturan Trapesium.
    
    Argumen:
    f -- fungsi yang akan diintegralkan
    a -- batas bawah
    b -- batas atas
    n -- jumlah segmen (sub-interval)
    """
    h = (b - a) / n
    # Ambil titik ujung pertama dan terakhir
    integral = 0.5 * (f(a) + f(b))
    
    # Tambahkan semua titik di tengah
    for i in range(1, n):
        integral += f(a + i * h)
        
    integral *= h
    return integral


def hitung_romberg(f, a, b, level_target=2):
    """
    Menghitung dan mencetak tabel integrasi Romberg langkah demi langkah
    sampai ke level R(level_target, level_target).
    
    Untuk R(2,2), kita perlu 3 level (level 0, 1, 2).
    """
    
    # Kita menggunakan list 2D untuk menyimpan tabel R[k][m]
    # Ukurannya adalah (level_target + 1) x (level_target + 1)
    R = [[0.0] * (level_target + 1) for _ in range(level_target + 1)]
    
    print("-" * 50)
    print(f"Memulai Perhitungan Romberg untuk "
          f"level R({level_target},{level_target})")
    print("-" * 50)

    # Level 0: Kolom Pertama (Aturan Trapesium)
    # Ini adalah R(k, 0)
    
    print("\n--- Kolom Pertama (m=0): Aturan Trapesium ---")
    for k in range(level_target + 1):
        # n = 2^k (n=1, n=2, n=4, ...)
        n_segmen = 2**k
        R[k][0] = trapesium(f, a, b, n_segmen)
        print(f"R({k}, 0) [n={n_segmen:2d}]: {R[k][0]:.10f}")

    # Level 1 & 2: Kolom Ekstrapolasi
    # m adalah level ekstrapolasi (kolom)
    for m in range(1, level_target + 1):
        print(f"\n--- Kolom Ekstrapolasi (m={m}) [O(h^{2*(m+1)})] ---")
        
        # k adalah level trapesium (baris)
        # Perhatikan k harus mulai dari m
        for k in range(m, level_target + 1):
            # Rumus Ekstrapolasi Richardson / Romberg:
            # R(k, m) = R(k, m-1) + (R(k, m-1) - R(k-1, m-1)) / \
            #           (4**m - 1)
            
            pembagi = (4**m - 1)
            R[k][m] = R[k][m-1] + (R[k][m-1] - R[k-1][m-1]) / pembagi
            
            print(f"R({k}, {m}): {R[k][m]:.10f}")

    print("\n--- Hasil Tabel Segitiga Romberg (R[k,m]) ---")
    for k in range(level_target + 1):
        row_str = " ".join([f"{R[k][m]:.10f}" for m in range(k + 1)])
        print(row_str)
        
    # Simpan hasil ke var agar print() tidak terlalu panjang
    hasil_final = R[level_target][level_target]
    print(f"\n>>> Hasil Akhir R({level_target},{level_target}): "
          f"{hasil_final:.10f}")
    print("=" * 50 + "\n")


# Definisi Fungsi

def f1(x):
    """Soal 1: cos(x)"""
    return np.cos(x)


def f2(x):
    """Soal 2: x^2"""
    return x**2


# Eksekusi Perhitungan

# 1. Menjalankan Soal 1: integral(cos(x)) dari 0 sampai pi/2
print("===== SOAL 1: integral(cos(x), 0, pi/2) =====")
hitung_romberg(f1, 0, np.pi/2, level_target=2)

# Spasi untuk memisahkan output soal
print("\n")

# 2. Menjalankan Soal 2: integral(x^2) dari 0 sampai 1
print("===== SOAL 2: integral(x^2, 0, 1) =====")
hitung_romberg(f2, 0, 1, level_target=2)

# cara step by ste[p