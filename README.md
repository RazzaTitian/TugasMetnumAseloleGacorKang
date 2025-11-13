🧮 Numerical Integration Suite (Metnum 2024)

📘 Deskripsi Umum

Repositori ini berisi implementasi tiga metode utama integrasi numerik dalam Python:

1. Metode 1 – Trapezoidal Rule


2. Metode 2 – Romberg Integration (Richardson Extrapolation)


3. Metode 3 – Adaptive Simpson’s Rule


4. Metode 4 – Gaussian Quadrature (Gauss–Legendre)



Tujuan proyek ini adalah membandingkan akurasi, efisiensi, dan kompleksitas dari masing-masing metode dalam menghitung integral fungsi kontinu seperti

\int_0^{\pi/2} \cos(x)\,dx \quad \text{dan} \quad \int_0^1 x^2\,dx.

Semua kode kompatibel dengan Google Colab dan hanya membutuhkan NumPy.


---

⚙️ Dependencies

Python ≥ 3.9

NumPy

---


📑 1️⃣ Romberg Integration (extrapolation.py)

Deskripsi Umum

Mengimplementasikan Romberg Integration, yaitu penggabungan Trapezoidal Rule dengan Richardson Extrapolation untuk meningkatkan orde akurasi hingga O(h⁶).

Alur Singkat

1. Hitung nilai integral dengan Trapezoidal Rule pada berbagai tingkat pembagian.


2. Terapkan Richardson Extrapolation:



R_{n,m} = \frac{4^m R_{n,m-1} - R_{n-1,m-1}}{4^m - 1}

Fungsi Utama

def compute_R22(f, a, b):
    ...

Fungsi Contoh

def f1(x): return np.cos(x)
def f2(x): return x**2


---

🧠 2️⃣ Adaptive Simpson’s Rule (adaptI.py)

Ringkasan

adaptI.py mengimplementasikan Simpson Adaptif yang membagi interval hanya pada bagian dengan galat besar. Pendekatan ini meningkatkan efisiensi tanpa mengorbankan akurasi.

Inti Algoritma

1. Simpson dasar:



S(a,b) = \frac{h}{6}\,[f(a) + 4f(m) + f(b)]

3. Gunakan ekstrapolasi Richardson untuk koreksi:



I \approx S_\text{halus} + \frac{S_\text{halus}-S_\text{kasar}}{15}

Fitur Teknis

Caching nilai f(a), f(m), f(b) → mencegah evaluasi berulang.

Pembagian toleransi tol/2 di tiap sub-interval.

Kompleksitas: O(N) dengan evaluasi f sekitar 2 per subdivisi.



---

🔢 3️⃣ Gaussian Quadrature (gaussian.py)

Deskripsi Umum

Mengimplementasikan Metode Gaussian Quadrature (Gauss–Legendre) untuk menghitung integral numerik dengan akurasi tinggi menggunakan titik dan bobot optimal.

Rumus Dasar

I = \int_a^b f(x)\,dx \approx \frac{b-a}{2} 
   \sum_{i=1}^{n} w_i\, f\!\left(\frac{b-a}{2}t_i + \frac{a+b}{2}\right)

: bobot yang terkait

Eksak untuk semua polinomial hingga orde 


Implementasi Singkat

import numpy as np

def gauss_legendre(f, a, b, n):
    t, w = np.polynomial.legendre.leggauss(n)
    mid, rad = 0.5*(a+b), 0.5*(b-a)
    return float(rad * np.dot(w, f(mid + rad*t)))

def gauss_legendre_auto(f, a, b, tol=1e-10, n_start=2, n_max=256):
    n, prev, hist = max(2, n_start), None, []
    while True:
        In = gauss_legendre(f, a, b, n)
        hist.append((n, In))
        if prev is not None and abs(In - prev) < tol: return In, n, hist
        if n >= n_max: return In, n, hist
        prev = In; n = n*2 if n < 32 else n+16

Contoh Eksekusi

import math
f1 = lambda x: np.cos(x)
f2 = lambda x: x**2

I1 = gauss_legendre(f1, 0.0, math.pi/2, n=4)
I2 = gauss_legendre(f2, 0.0, 1.0, n=2)

print(I1, I2)

Output

∫₀^{π/2} cos(x) dx ≈ 0.9999999772
∫₀¹ x² dx ≈ 0.3333333333


---

📊 Hasil & Analisis Gaussian Quadrature

n	Aproksimasi 	Galat Absolut	Fungsi 

1	1.1107207345	1.107×10⁻¹	cos x, [0, π/2]
2	0.9984726134	1.527×10⁻³	cos x
3	1.0000081216	8.12×10⁻⁶	cos x
4	0.9999999772	2.28×10⁻⁸	cos x
1	0.2500000000	8.33×10⁻²	x², [0, 1]
2	0.3333333333	≈ 0	x²
3	0.3333333333	≈ 0	x²


Analisis:

Untuk fungsi halus (), konvergensi sangat cepat; galat < 10⁻⁸ pada n = 4.

Untuk polinomial (), hasil eksak pada n = 2 karena derajat ≤ 2n − 1.

Gaussian Quadrature memberikan efisiensi tinggi dengan evaluasi fungsi minimal.



---

📚 Referensi

Burden & Faires, Numerical Analysis, 9th Ed.

Chapra & Canale, Numerical Methods for Engineers, 7th Ed.

NumPy Docs: numpy.polynomial.legendre.leggauss
