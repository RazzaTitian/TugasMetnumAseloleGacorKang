# Penjelasan Kode Extrapolation

## Deskripsi Umum
Program ini mengimplementasikan **Romberg Integration** untuk menghitung integral numerik dengan akurasi tinggi. Metode ini menggunakan **Richardson Extrapolation** pada hasil **Trapezoidal Rule** untuk meningkatkan ketelitian.

## Struktur Program

### 1. Import Library
```python
import numpy as np
```
- Menggunakan NumPy untuk fungsi matematika seperti `cos()` dan konstanta `pi`

### 2. Fungsi Utama: `compute_R22(f, a, b)`

#### Parameter:
- `f`: Fungsi yang akan diintegralkan
- `a`: Batas bawah integral
- `b`: Batas atas integral

#### Proses Perhitungan:

##### **BAGIAN 1: Trapezoidal Rule (Kolom 1)**
Menghitung nilai integral dengan aturan trapesium pada berbagai tingkat pembagian:

**R_0,0 (n=1):**
```python
h0 = b - a
R00 = 0.5 * h0 * (f(a) + f(b))
```
- Menggunakan 1 interval (2 titik)
- Formula: `(b-a)/2 * [f(a) + f(b)]`

**R_1,0 (n=2):**
```python
h1 = h0 / 2.0
R10 = 0.5 * R00 + h1 * f(a + h1)
```
- Menggunakan 2 interval (3 titik)
- Efisien: menggunakan hasil R_0,0 dan menambahkan titik tengah

**R_2,0 (n=4):**
```python
h2 = h1 / 2.0
sum_f = f(a + h2) + f(a + 3*h2)
R20 = 0.5 * R10 + h2 * sum_f
```
- Menggunakan 4 interval (5 titik)
- Menambahkan 2 titik baru: pada h/4 dan 3h/4

##### **BAGIAN 2: Richardson Extrapolation (Kolom 2 & 3)**
Meningkatkan akurasi dengan menggabungkan hasil trapesium:

**Kolom 2 (m=1):**
```python
R11 = (4.0 * R10 - R00) / 3.0
R21 = (4.0 * R20 - R10) / 3.0
```
- Formula: `R(n,m) = (4^m * R(n,m-1) - R(n-1,m-1)) / (4^m - 1)`
- Untuk m=1: `(4*R(n,0) - R(n-1,0)) / 3`

**Kolom 3 (m=2) - TARGET:**
```python
R22 = (16.0 * R21 - R11) / 15.0
```
- Formula: `(16*R(2,1) - R(1,1)) / 15`
- Ini adalah hasil akhir dengan akurasi tertinggi (O(h^6))

### 3. Fungsi-Fungsi Soal

**Soal 1:**
```python
def f1(x):
    return np.cos(x)
```
- Integral: ∫cos(x)dx dari 0 sampai π/2
- Hasil analitik: sin(π/2) - sin(0) = 1

**Soal 2:**
```python
def f2(x):
    return x**2
```
- Integral: ∫x²dx