# 🧮 Numerical Integration — Metnum 2024

## 📘 Deskripsi Umum
Repositori ini berisi implementasi beberapa **metode integrasi numerik** dalam Python untuk membandingkan akurasi, efisiensi, dan kompleksitas perhitungan.  
Setiap metode diuji menggunakan dua fungsi uji standar:

\[
\int_0^{\pi/2} \cos(x)\,dx \quad \text{dan} \quad \int_0^1 x^2\,dx
\]

Semua kode dapat dijalankan langsung di **Google Colab** dan hanya membutuhkan **NumPy**.

---

## ⚙️ Dependencies
- Python ≥ 3.9  
- NumPy  

---

## 🔹 Metode 1 – Trapezoidal Rule
Metode paling dasar yang menghampiri luas di bawah kurva dengan **trapesium-trapesium kecil**.  
Sederhana namun hanya memiliki akurasi **orde O(h²)**.

---

## 🔹 Metode 2 – Romberg Integration (`extrapolation.py`)

### Deskripsi
Menggabungkan **Trapezoidal Rule** dan **Richardson Extrapolation** untuk menaikkan akurasi hingga **O(h⁶)**.  
Setiap kolom hasil memperbaiki estimasi integral dari kolom sebelumnya.

### Rumus Utama
\[
R_{n,m} = \frac{4^m R_{n,m-1} - R_{n-1,m-1}}{4^m - 1}
\]
Nilai \(R_{2,2}\) menjadi hasil dengan ketelitian tertinggi.

### Contoh Kode
```python
import numpy as np
def f1(x): return np.cos(x)
def f2(x): return x**2
