# LIS Tree Visualizer  
**Largest (Longest) Increasing Subsequence Visualization**

<img width="877" height="651" alt="image" src="https://github.com/user-attachments/assets/6970ab60-26a3-4f4b-b570-d2510c68cb20" />

## Judul
Visualisasi Longest Increasing Subsequence (LIS) menggunakan Struktur Graf DAG dan Tree Murni (Memenuhi Teorema 2-1)

---

## Deskripsi Masalah
Permasalahan *Longest Increasing Subsequence (LIS)* adalah mencari subsekuens terpanjang dari suatu deret bilangan yang tersusun secara menaik, dengan tetap mempertahankan urutan elemen aslinya.

Dalam pendekatan graf, setiap elemen direpresentasikan sebagai simpul (node), dan hubungan antar elemen yang memenuhi syarat menaik direpresentasikan sebagai sisi (edge). Namun, representasi ini secara alami membentuk *Directed Acyclic Graph (DAG)*, bukan sebuah tree, sehingga satu simpul dapat memiliki lebih dari satu parent dan melanggar Teorema 2-1 pada teori graf tree.

Oleh karena itu, diperlukan dua pendekatan visualisasi:
1. Visualisasi DAG untuk menampilkan seluruh kemungkinan subsekuens menaik
2. Visualisasi tree murni yang memenuhi Teorema 2-1 dengan membatasi satu parent per simpul

---

## Tujuan Program
Program ini dibuat untuk:
- Memvisualisasikan proses pembentukan Longest Increasing Subsequence
- Menunjukkan perbedaan antara struktur DAG dan tree murni
- Memverifikasi pemenuhan Teorema 2-1 pada struktur tree
- Menyediakan antarmuka GUI agar proses dapat diamati secara visual

---

## Proses Penyelesaian
1. Pengguna memasukkan deret bilangan melalui GUI
2. Pengguna memilih mode visualisasi:
   - **Mode DAG**: semua hubungan subsekuens menaik ditampilkan
   - **Mode Pure Tree**: hanya satu jalur terbaik untuk setiap simpul
3. Program membangun struktur graf sesuai mode yang dipilih
4. Struktur divisualisasikan dalam bentuk tree bertingkat
5. Panjang LIS maksimum dihitung menggunakan pendekatan Dynamic Programming
6. Status pemenuhan Teorema 2-1 ditampilkan pada GUI

---

## Algoritma yang Digunakan

### 1. Longest Increasing Subsequence (Dynamic Programming)
Panjang LIS dihitung menggunakan relasi:

LIS(i) = 1 + max(LIS(j)) untuk semua j < i dan a[j] < a[i]

Jika tidak ada elemen sebelumnya yang lebih kecil, maka:

LIS(i) = 1


Kompleksitas waktu:
- O(n²)

---

### 2. Representasi DAG
Pada mode DAG:
- Setiap node terhubung ke seluruh node setelahnya yang memiliki nilai lebih besar
- Satu node dapat memiliki lebih dari satu parent
- Struktur ini membentuk Directed Acyclic Graph (DAG)
- Tidak memenuhi Teorema 2-1

---

### 3. Representasi Pure Tree (Teorema 2-1)
Pada mode tree murni:
- Setiap node hanya memiliki satu parent
- Parent dipilih berdasarkan jalur LIS terpanjang
- Struktur yang terbentuk adalah tree
- Memenuhi Teorema 2-1 pada teori graf

---

## Teorema 2-1 (Tree Property)
Suatu graf disebut tree apabila:
1. Terhubung
2. Tidak memiliki siklus
3. Setiap simpul (kecuali root) memiliki tepat satu parent

Mode *Pure Tree* pada program ini memenuhi seluruh kondisi tersebut.

---

## Teknologi yang Digunakan
- Python 3
- Tkinter (GUI)
- Git & GitHub

---

## Cara Menjalankan Program
```bash
python lis_visualizer.py




