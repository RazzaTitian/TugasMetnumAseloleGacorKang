🧮 Numerical Integration – Metode Numeris

📘 Deskripsi Umum

Dokumen ini merangkum tiga metode inti integrasi numerik yang dipakai di tugas:
Romberg (Extrapolation), Adaptive Simpson’s Rule, dan Gaussian Quadrature (Gauss–Legendre).






---

⚙️ Dependencies

Python ≥ 3.9

numpy



---

🚀 Quick Start

import numpy as np, math
from gaussian import gauss_legendre, gauss_legendre_auto
# from adaptI import integral_adaptif_simpson
# from extrapolation import compute_R22

# Gaussian Quadrature (Metode 4)
f1 = lambda x: np.cos(x)
f2 = lambda x: x**2
print(gauss_legendre(f1, 0.0, math.pi/2, n=4))  # ≈ 1
print(gauss_legendre(f2, 0.0, 1.0, n=2))        # ≈ 1/3
print(gauss_legendre_auto(f1, 0.0, math.pi/2, tol=1e-12))

# Adaptive Simpson (Metode 3)
# I_adapt = integral_adaptif_simpson(f1, 0.0, math.pi/2, tol=1e-8)

# Romberg (Metode 2)
# I_R22  = compute_R22(f1, 0.0, math.pi/2)  # R_2,2


---

2️⃣ Romberg Integration (extrapolation.py)

Ringkasan

Romberg meningkatkan hasil Trapesium melalui Richardson Extrapolation:

R_{n,m}=\frac{4^m R_{n,m-1}-R_{n-1,m-1}}{4^m-1}

Alur Perhitungan

1. Kolom 1 (Trapesium): , , 


2. Kolom 2: , 


3. Kolom 3:  (hasil akhir)



Fungsi Uji

def f1(x): return np.cos(x)   # ∫ cos, 0→π/2 = 1
def f2(x): return x**2        # ∫ x^2, 0→1   = 1/3


---

3️⃣ Adaptive Simpson’s Rule (adaptI.py)

Kontrak

Input: f, batas a,b, tol (default 1e-8), max_recursion

Output: aproksimasi ∫_a^b f(x) dx (float)


Inti Matematika

Simpson pada , , :


S(a,b)=\frac{h}{6}\,[f(a)+4f(m)+f(b)]

Jika  → bagi interval, panggil rekursi.

Koreksi Richardson:


I \approx S_{\text{halus}} + \frac{S_{\text{halus}}-S_{\text{kasar}}}{15}

Catatan Implementasi

Kirim fa,fm,fb ke fungsi rekursif → hindari evaluasi ulang.

Bagi toleransi jadi tol/2 per sub-interval.

max_level mencegah rekursi tak terbatas (fungsi osilatif/diskontinu).



---

4️⃣ Gaussian Quadrature – Gauss–Legendre (gaussian.py)

Ide Dasar

\int_a^b f(x)\,dx \;\approx\; \frac{b-a}{2}\sum_{i=1}^{n}w_i\,
f\!\Big(\tfrac{b-a}{2}t_i+\tfrac{a+b}{2}\Big)

Eksak untuk polinomial derajat .

Implementasi Minimal (NumPy only)

import numpy as np

def gauss_legendre(f, a, b, n):
    t, w = np.polynomial.legendre.leggauss(n)  # nodes & weights in [-1,1]
    mid = 0.5*(a + b); rad = 0.5*(b - a)
    return float(rad * np.dot(w, f(mid + rad*t)))

def gauss_legendre_auto(f, a, b, tol=1e-10, n_start=2, n_max=256):
    n = max(2, n_start); prev = None; hist = []
    while True:
        In = gauss_legendre(f, a, b, n)
        hist.append((n, In))
        if prev is not None and abs(In - prev) < tol: return In, n, hist
        if n >= n_max: return In, n, hist
        prev = In; n = n*2 if n < 32 else n+16


---

📊 Hasil Uji – Gaussian Quadrature

Integral 1 — 

| n | Aproksimasi  | Galat |I−I_n| | |-----:|-------------------------:|--------:| | 1 | 1.110720734540 | 1.107207e-01 | | 2 | 0.998472613404 | 1.527387e-03 | | 3 | 1.000008121556 | 8.121556e-06 | | 4 | 0.999999977197 | 2.280285e-08 |

Integral 2 — 

| n | Aproksimasi  | Galat |I−I_n| | |-----:|-------------------------:|--------:| | 1 | 0.250000000000 | 8.333333e-02 | | 2 | 0.333333333333 | ≈ 0 | | 3 | 0.333333333333 | ≈ 0 |

Catatan: Eksak untuk polinomial derajat ≤ ; karena  derajat 2,  sudah tepat (hingga presisi floating-point).


---

✅ Rekomendasi Praktis

Romberg: cepat naik akurasi ketika fungsi halus; enak untuk “3 level minimal”.

Adaptive Simpson: pakai jika ada bagian berkurvatur tinggi; hemat evaluasi fungsi.

Gaussian Quadrature: pilihan utama untuk fungsi halus; gunakan auto-ladder  hingga selisih antar- < toleransi.



---

📚 Referensi

R.L. Burden & J.D. Faires, Numerical Analysis, 9th ed.

S.C. Chapra & R.P. Canale, Numerical Methods for Engineers, 7th ed.

NumPy: numpy.polynomial.legendre.leggauss
