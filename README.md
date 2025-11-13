Ringkasan & Penjelasan Kode Metode Numerik

Deskripsi Umum

Dokumen ini menjelaskan tiga metode inti integrasi numerik yang dipakai di tugas—Romberg (Richardson Extrapolation), Adaptive Simpson’s Rule, dan Gaussian Quadrature (Gauss–Legendre)—beserta quick start, kontrak fungsi, dan contoh penggunaan.


---

0) Dependencies

Python ≥ 3.9
numpy


---

1) Quick Start

import numpy as np, math
from gaussian import gauss_legendre, gauss_legendre_auto
# from adaptI import integral_adaptif_simpson
# from extrapolation import compute_R22

# Contoh fungsi uji
f1 = lambda x: np.cos(x)     # ∫_0^{π/2} cos x dx = 1
f2 = lambda x: x**2          # ∫_0^{1}    x^2 dx   = 1/3

# Gaussian Quadrature (Gauss–Legendre)
print(gauss_legendre(f1, 0.0, math.pi/2, n=4))   # ≈ 1
print(gauss_legendre(f2, 0.0, 1.0, n=2))         # ≈ 1/3
print(gauss_legendre_auto(f1, 0.0, math.pi/2, tol=1e-12))

# Adaptive Simpson
# I_adapt = integral_adaptif_simpson(f1, 0.0, math.pi/2, tol=1e-8)

# Romberg (R_2,2)
# I_R22 = compute_R22(f1, 0.0, math.pi/2)


---

Penjelasan Kode Extrapolation (Romberg) — extrapolation.py

Deskripsi Umum

Mengimplementasikan Romberg Integration: menerapkan Richardson Extrapolation pada deret aproksimasi Trapezoidal Rule sehingga orde galat meningkat secara sistematis.

Rumus Kunci

R_{n,m}=\frac{4^{\,m}\,R_{n,m-1}-R_{n-1,m-1}}{4^{\,m}-1}

Struktur Program

1. Import Library

import numpy as np

2. Fungsi Utama: compute_R22(f, a, b)

Parameter

f: fungsi integrand

a: batas bawah

b: batas atas


Output

Aproksimasi integral berakurasi tinggi  (orde ).


BAGIAN 1: Trapezoidal Rule (Kolom 1)

Hitung bertingkat:  (n=1),  (n=2),  (n=4).

R_0,0 (n=1)

h0  = b - a
R00 = 0.5 * h0 * (f(a) + f(b))

R_1,0 (n=2) — tambah titik tengah

h1  = h0 / 2.0
R10 = 0.5 * R00 + h1 * f(a + h1)

R_2,0 (n=4) — tambah dua titik baru

h2    = h1 / 2.0
sum_f = f(a + h2) + f(a + 3*h2)
R20   = 0.5 * R10 + h2 * sum_f

BAGIAN 2: Richardson Extrapolation (Kolom 2 & 3)

Kolom 2 (m=1)

R11 = (4.0 * R10 - R00) / 3.0
R21 = (4.0 * R20 - R10) / 3.0

Kolom 3 (m=2) — TARGET

R22 = (16.0 * R21 - R11) / 15.0

3. Fungsi Uji

def f1(x): return np.cos(x)   # ∫_0^{π/2} cos x dx = 1
def f2(x): return x**2        # ∫_0^{1} x^2 dx     = 1/3


---

Penjelasan Kode Adaptive Simpson — adaptI.py

Kontrak

Input: f, a, b, tol=1e-8, max_recursion
Output: float aproksimasi 

Inti Matematika

Untuk , ,

S(a,b)=\frac{h}{6}\,[f(a)+4f(m)+f(b)]

I \approx S_{\text{halus}} + \frac{S_{\text{halus}}-S_{\text{kasar}}}{15}

Struktur Program

1. Import

import numpy as np

2. Fungsi Publik: integral_adaptif_simpson(f, a, b, tol=1e-8, max_recursion=20)

Menyiapkan nilai awal fa, fm, fb lalu memanggil prosedur rekursif.


3. Inti Rekursif (sketsa)

def _adaptive(f, a, b, fa, fm, fb, S_ab, tol, level, max_level):
    m   = 0.5*(a+b); h = b-a
    lm  = 0.5*(a+m); rm = 0.5*(m+b)
    flm = f(lm); frm = f(rm)

    S_left  = (h/12.0) * (fa + 4*flm + fm)
    S_right = (h/12.0) * (fm + 4*frm + fb)
    S_ref   = S_left + S_right

    if level >= max_level:
        return S_ref  # fallback

    if abs(S_ref - S_ab) <= 15*tol:
        return S_ref + (S_ref - S_ab)/15.0  # Richardson fix

    # Rekursi ke kiri & kanan; bagi toleransi
    left  = _adaptive(f, a, m,  fa, flm, fm,  S_left,  tol/2.0, level+1, max_level)
    right = _adaptive(f, m, b,  fm, frm, fb,  S_right, tol/2.0, level+1, max_level)
    return left + right

Catatan Implementasi

Hindari evaluasi ulang: teruskan fa, fm, fb ke fungsi rekursif.

Bagi toleransi per subinterval (tol/2).

Batasi rekursi (max_level) untuk fungsi berosilasi/diskontinu.



---

Penjelasan Kode Gaussian Quadrature (Gauss–Legendre) — gaussian.py

Ide Dasar

Transformasi linier dari  ke  memberi pendekatan:

\int_a^b f(x)\,dx \;\approx\; \frac{b-a}{2}\sum_{i=1}^{n} w_i \;
f\!\bigg(\tfrac{b-a}{2}t_i+\tfrac{a+b}{2}\bigg)

Implementasi Minimal (NumPy-only)

1. Import

import numpy as np

2. Fungsi: gauss_legendre(f, a, b, n)

def gauss_legendre(f, a, b, n):
    t, w = np.polynomial.legendre.leggauss(n)  # node & bobot di [-1,1]
    mid = 0.5 * (a + b)
    rad = 0.5 * (b - a)
    return float(rad * np.dot(w, f(mid + rad * t)))

3. Fungsi: gauss_legendre_auto(f, a, b, tol=1e-10, n_start=2, n_max=256)

Adaptasi jumlah titik sampai konvergen.

def gauss_legendre_auto(f, a, b, tol=1e-10, n_start=2, n_max=256):
    n = max(2, n_start); prev = None; hist = []
    while True:
        In = gauss_legendre(f, a, b, n)
        hist.append((n, In))
        if prev is not None and abs(In - prev) < tol:
            return In, n, hist
        if n >= n_max:
            return In, n, hist
        prev = In
        n = n*2 if n < 32 else n+16


---

Hasil Uji — Gaussian Quadrature

Integral 1 — 

|  n | Aproksimasi        | Galat  | |---:|--------------------:|------------------:| |  1 | 1.110720734540     | 1.107207e-01      | |  2 | 0.998472613404     | 1.527387e-03      | |  3 | 1.000008121556     | 8.121556e-06      | |  4 | 0.999999977197     | 2.280285e-08      |

Integral 2 — 

|  n | Aproksimasi        | Galat  | |---:|--------------------:|------------------:| |  1 | 0.250000000000     | 8.333333e-02      | |  2 | 0.333333333333     | ≈ 0               | |  3 | 0.333333333333     | ≈ 0               |

Catatan: Eksak untuk polinomial derajat ≤ . Karena  derajat 2, maka  sudah tepat (hingga presisi floating-point).


---

Rekomendasi Praktis

Romberg: cepat menaikkan akurasi pada fungsi halus; enak untuk “3 level minimal” (hingga ).

Adaptive Simpson: cocok saat ada bagian berkurvatur/gradien tinggi; hemat evaluasi fungsi via pembagian adaptif.

Gaussian Quadrature: pilihan utama untuk fungsi halus; gunakan auto-ladder sampai  toleransi.



---

Referensi

R.L. Burden & J.D. Faires, Numerical Analysis, 9th ed.

S.C. Chapra & R.P. Canale, Numerical Methods for Engineers, 7th ed.

NumPy: numpy.polynomial.legendre.leggauss
