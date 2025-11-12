import math

def f1(x):
    """Fungsi pertama dari soal: cos(x)"""
    return math.cos(x)

def f2(x):
    """Fungsi kedua dari soal: x^2"""
    return x**2

def _adaptive_simpson(f, a, b, tol, fa, fm, fb, level, max_level):
    """
    Fungsi helper rekursif untuk Adaptive Simpson.
    
    Parameter:
    f: fungsi yang diintegralkan
    a, b: batas interval [a, b]
    tol: toleransi error untuk interval ini
    fa, fm, fb: nilai f(a), f(m), dan f(b) yang sudah dihitung, 
                dimana m = (a+b)/2
    level: level rekursi saat ini
    max_level: batas maksimum rekursi
    """
    
    # Mencegah rekursi tak terbatas
    if level > max_level:
        print(f"Peringatan: Level rekursi maksimum ({max_level}) tercapai. "
              "Hasil mungkin tidak akurat.")
        # Kembalikan estimasi terbaik saat ini
        h = b - a
        return (h / 6) * (fa + 4 * fm + fb)

    # Titik tengah
    m = (a + b) / 2
    h = b - a

    # 1. Hitung S1 (estimasi "kasar" menggunakan Simpson 1/3 di [a, b])
    # Kita sudah punya fa, fm, fb dari pemanggilan sebelumnya
    S1 = (h / 6) * (fa + 4 * fm + fb)

    # 2. Hitung S2 (estimasi "halus" dengan 2x interval Simpson 1/3)
    # Kita perlu 2 titik baru di antara a-m dan m-b
    ml = (a + m) / 2
    mr = (m + b) / 2
    fml = f(ml)
    fmr = f(mr)

    # S2 adalah jumlah dari Simpson di [a, m] dan [m, b]
    # h untuk S2 adalah h/2
    S2 = (h / 12) * (fa + 4 * fml + 2 * fm + 4 * fmr + fb)

    # 3. Estimasi error
    # Error pada S2 diperkirakan sebagai (1/15) * |S2 - S1|
    error = (1 / 15) * abs(S2 - S1)

    # 4. Cek toleransi
    if error < tol:
        # Jika error diterima, kembalikan S2
        # Kita tambahkan koreksi error (S2 - S1)/15,
        # ini adalah bagian dari ekstrapolasi Richardson
        return S2 + (S2 - S1) / 15
    else:
        # Jika error terlalu besar, bagi interval jadi dua dan ulangi (rekursi)
        # Bagikan toleransi error ke dua sub-interval
        tol_half = tol / 2
        
        # Panggil rekursi untuk [a, m]
        # Poin-poinnya adalah a, ml, m (fa, fml, fm)
        left = _adaptive_simpson(f, a, m, tol_half, fa, fml, fm, level + 1, max_level)
        
        # Panggil rekursi untuk [m, b]
        # Poin-poinnya adalah m, mr, b (fm, fmr, fb)
        right = _adaptive_simpson(f, m, b, tol_half, fm, fmr, fb, level + 1, max_level)
        
        # Jumlahkan hasil dari kedua sisi
        return left + right

def integrate_adaptive_simpson(f, a, b, tol=1e-8, max_recursion=20):
    """
    Fungsi utama (wrapper) untuk Adaptive Simpson's Integration.
    
    Parameter:
    :param f: Fungsi yang akan diintegralkan (menerima satu argumen float)
    :param a: Batas bawah integral
    :param b: Batas atas integral
    :param tol: Toleransi error total yang diinginkan (default: 1e-8)
    :param max_recursion: Batas rekursi maksimum (default: 20)
    :return: Nilai integral (float)
    """
    print(f"--- Menghitung Integral dari {f.__name__} dari {a} sampai {b} ---")
    
    # Hitung 3 titik awal
    m = (a + b) / 2
    fa = f(a)
    fm = f(m)
    fb = f(b)
    
    # Mulai rekursi dari level 0
    result = _adaptive_simpson(f, a, b, tol, fa, fm, fb, 0, max_recursion)
    print(f"Hasil: {result}\n")
    return result

# --- Main execution ---
if __name__ == "__main__":
    
    # --- Soal 1: Integral cos(x) dx from 0 to pi/2 ---
    a1 = 0
    b1 = math.pi / 2
    hasil_eksak_1 = 1.0  # Karena integral(cos(x)) = sin(x) -> sin(pi/2) - sin(0) = 1 - 0 = 1
    
    hasil_integral_1 = integrate_adaptive_simpson(f1, a1, b1, tol=1e-10)
    print(f"Hasil Eksak (cos(x)): {hasil_eksak_1}")
    print(f"Error Aktual: {abs(hasil_integral_1 - hasil_eksak_1)}")
    
    print("-" * 30)

    # --- Soal 2: Integral x^2 dx from 0 to 1 ---
    a2 = 0
    b2 = 1
    hasil_eksak_2 = 1/3  # Karena integral(x^2) = (x^3)/3 -> (1^3)/3 - (0^3)/3 = 1/3
    
    hasil_integral_2 = integrate_adaptive_simpson(f2, a2, b2, tol=1e-10)
    print(f"Hasil Eksak (x^2): {hasil_eksak_2}")
    print(f"Error Aktual: {abs(hasil_integral_2 - hasil_eksak_2)}")