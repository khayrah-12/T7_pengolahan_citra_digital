# Mini Project Integrasi Pengolahan Citra Digital
## Verifikasi Nomor Ijazah dan Deteksi Keberadaan Tanda Tangan


## Mata Kuliah
Pengolahan Citra Digital


## Semester
5


---

# 1. Deskripsi Project

Mini Project ini merupakan implementasi integrasi pengolahan citra digital pada dokumen ijazah.

Sistem dibuat untuk melakukan proses verifikasi dokumen ijazah secara otomatis dengan dua fungsi utama:

1. Membaca nomor ijazah menggunakan Optical Character Recognition (OCR).
2. Mendeteksi keberadaan tanda tangan pada dokumen ijazah menggunakan metode pengolahan citra.

Input sistem berupa citra ijazah hasil pemindaian, sedangkan output sistem berupa nomor ijazah hasil OCR, nilai Character Error Rate (CER), serta status keberadaan tanda tangan.


Contoh:

### Input

```
01_HighQuality_Enhanced.jpg
```


### Output

```
Nomor Ijazah : 571012022000056

CER          : 0.0

Tanda Tangan : SIGNATURE PRESENT
```


---

# 2. Tujuan Sistem

Tujuan dari pembuatan prototype ini adalah:

- Mengimplementasikan proses preprocessing citra digital pada dokumen ijazah.
- Melakukan ekstraksi nomor ijazah menggunakan OCR.
- Mengukur performa OCR menggunakan Character Error Rate (CER).
- Melakukan deteksi keberadaan tanda tangan berdasarkan karakteristik citra.
- Mengintegrasikan proses OCR dan signature detection dalam satu sistem.


---

# 3. Dataset

Dataset yang digunakan terdiri dari sembilan variasi citra ijazah yang berasal dari dokumen yang sama dengan kondisi degradasi berbeda.

Data yang digunakan:

```
01_HighQuality_Enhanced.jpg
02_LowContrast.jpg
03_Blurred.jpg
04_HighNoise.jpg
05_LowResolution_Upsampled.jpg
06_Faded_Underexposed.jpg
07_ColorShift_WarmTint.jpg
08_JPEGCompression_Artifacts.jpg
09_CombinedDegradation.jpg
```


---

# 4. Pipeline Sistem

Alur kerja sistem:

```
                Citra Ijazah
                     |
                     v
                 Grayscale
                     |
                     v
             Image Enhancement
                     |
        -----------------------------
        |                           |
        v                           v
  Area Nomor Ijazah          Area Tanda Tangan
        |                           |
        v                           v
  Enhancement              Thresholding
        |                           |
        v                           v
       OCR                   Morphology
        |                           |
        v                           v
 Nomor Ijazah             Signature Detection
        |                           |
        -----------------------------
                     |
                     v
            Hasil Verifikasi
```


---

# 5. Metode Pengolahan Citra


## 5.1 Grayscale

Tahap pertama adalah mengubah citra berwarna menjadi citra grayscale.

Grayscale digunakan karena proses analisis selanjutnya lebih mudah dilakukan menggunakan satu kanal intensitas keabuan.


---

## 5.2 Image Enhancement

Image enhancement digunakan untuk meningkatkan kualitas citra sebelum proses OCR.

Metode enhancement yang digunakan adalah:


## CLAHE (Contrast Limited Adaptive Histogram Equalization)

CLAHE digunakan untuk:

- meningkatkan kontras lokal citra,
- memperjelas karakter nomor ijazah,
- membantu proses pembacaan OCR.


Tahapan enhancement:

```
Citra asli
     |
     v
Grayscale
     |
     v
CLAHE
     |
     v
Citra enhanced
```


---

# 6. Proses OCR Nomor Ijazah

Area nomor ijazah dipotong menggunakan Region of Interest (ROI).

Koordinat ROI diperoleh dari proses sebelumnya pada Tugas 5.


Tahapan OCR:

1. Mengambil area nomor ijazah.
2. Melakukan rotasi ROI karena orientasi hasil scan.
3. Memperbesar citra sebanyak 3 kali.
4. Melakukan OCR menggunakan Tesseract.


Konfigurasi OCR:

```
--psm 7
tessedit_char_whitelist=0123456789
```


Nomor ijazah acuan:

```
571012022000056
```


---

# 7. Evaluasi OCR Menggunakan CER


Character Error Rate (CER) digunakan untuk mengetahui tingkat kesalahan pembacaan OCR.

Rumus:

```
CER = (Substitution + Deletion + Insertion) / Jumlah Karakter
```


Interpretasi:

- CER = 0 berarti hasil OCR sama dengan nomor referensi.
- Semakin kecil CER maka semakin baik performa OCR.


---

# 8. Deteksi Keberadaan Tanda Tangan


Deteksi tanda tangan dilakukan pada area ROI tanda tangan dokumen.


Tahapan:


## 8.1 Grayscale

ROI tanda tangan dikonversi menjadi citra grayscale.


## 8.2 Gaussian Blur

Gaussian Blur digunakan untuk mengurangi noise kecil.


## 8.3 Thresholding

Metode thresholding yang digunakan:

```
Otsu Thresholding
```


Tujuan:

- memisahkan tinta tanda tangan dari background dokumen,
- menghasilkan citra biner.


## 8.4 Morphology

Operasi morfologi yang digunakan:


### Opening

Digunakan untuk menghilangkan noise kecil.


### Closing

Digunakan untuk menyambungkan bagian garis tanda tangan yang terputus.


## 8.5 Signature Detection

Keputusan keberadaan tanda tangan dilakukan berdasarkan:

- nilai kontras ROI,
- rasio foreground,
- ukuran komponen terbesar.


Output:

```
SIGNATURE PRESENT
```

atau

```
SIGNATURE ABSENT
```


Pada dataset pengujian yang digunakan, seluruh citra ijazah memiliki tanda tangan pada area ROI yang dianalisis sehingga hasil deteksi seluruhnya menghasilkan status SIGNATURE PRESENT.


---

# 9. Hasil Pengujian


Pengujian dilakukan menggunakan 9 citra ijazah.

Seluruh citra pengujian merupakan dokumen ijazah yang memiliki tanda tangan pada area ROI yang telah ditentukan, sehingga evaluasi difokuskan pada kemampuan sistem dalam mendeteksi keberadaan tanda tangan.


| File | OCR Number | CER | Signature Status |
|---|---|---|---|
|01_HighQuality_Enhanced.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|02_LowContrast.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|03_Blurred.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|04_HighNoise.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|05_LowResolution_Upsampled.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|06_Faded_Underexposed.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|07_ColorShift_WarmTint.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|08_JPEGCompression_Artifacts.jpg|571012022000056|0.0|SIGNATURE PRESENT|
|09_CombinedDegradation.jpg|571012022000056|0.0|SIGNATURE PRESENT|


---

# 10. Analisis Metode Enhancement Berdasarkan CER


Berdasarkan hasil pengujian, seluruh variasi citra menghasilkan:

```
CER = 0.0
```


Hal ini menunjukkan bahwa metode enhancement yang digunakan berhasil mempertahankan informasi karakter nomor ijazah.


Pada seluruh kondisi degradasi:

- low contrast,
- blur,
- noise,
- perubahan warna,
- kompresi JPEG,


OCR tetap mampu membaca nomor ijazah dengan benar.


Sehingga metode enhancement yang digunakan dinilai efektif berdasarkan nilai CER karena menghasilkan tingkat kesalahan karakter sebesar 0.


---

# 11. Struktur Folder Repository


```
T7_Mini_Project_Integrasi/

│
├── data/
│   ├── 01_HighQuality_Enhanced.jpg
│   ├── 02_LowContrast.jpg
│   ├── ...
│   └── 09_CombinedDegradation.jpg
│
├── output/
│   ├── hasil_verifikasi.csv
│   ├── enhanced image
│   └── signature mask
│
├── main.py
│
├── README.md
│
└── requirements.txt
```


---

# 12. Cara Menjalankan Program


## Prasyarat

Selain library Python, sistem membutuhkan instalasi Tesseract OCR Engine.


## 1. Aktifkan Virtual Environment

Windows:

```
.venv\Scripts\activate
```


## 2. Install Library


```
pip install -r requirements.txt
```


Library yang digunakan:

- OpenCV
- NumPy
- Matplotlib
- Pytesseract


## 3. Jalankan Program


```
python main.py
```


---

# 13. Output Program


Setelah program selesai dijalankan, sistem menghasilkan:

```
output/hasil_verifikasi.csv
```


Isi file:

- nama citra,
- hasil OCR nomor ijazah,
- nilai CER,
- status tanda tangan.


---

# 14. Kesimpulan


Prototype verifikasi dokumen ijazah berhasil dibuat dengan mengintegrasikan metode pengolahan citra digital, OCR, dan signature detection.

Berdasarkan hasil pengujian:

- Sistem berhasil membaca nomor ijazah pada seluruh citra.
- Nilai CER yang diperoleh adalah 0.0.
- Sistem berhasil mendeteksi keberadaan tanda tangan pada seluruh citra pengujian.

Hasil tersebut menunjukkan bahwa pipeline pengolahan citra yang digunakan mampu melakukan proses verifikasi dokumen ijazah secara otomatis.