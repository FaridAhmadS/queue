# 🗂️ Queue Simulation Studio

## Aplikasi Simulasi Struktur Data Queue

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/tkinter-GUI-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 👨‍💻 IDENTITAS PEMBUAT

| Keterangan | Detail |
|------------|--------|
| **Nama** | FARID AHMAD SANTOSO |
| **NIM** | 25091397050 |
| **Kelas** | 2025B |
| **Mata Kuliah** | Struktur Data & Algoritma |
| **Semester** | 2 (Genap) |

---

## 📋 DESKRIPSI PROGRAM

Program ini merupakan aplikasi desktop interaktif untuk **mensimulasikan 5 konsep Queue** dalam Struktur Data:

| No | Simulasi | Konsep Queue | Deskripsi |
|----|----------|--------------|-----------|
| 1 | 🖨️ **Printer Queue** | FIFO Queue | Simulasi antrian dokumen pada printer |
| 2 | 🥔 **Hot Potato** | Circular Queue | Game eliminasi pemain dengan operan melingkar |
| 3 | 🏥 **Rumah Sakit** | Priority Queue | Antrian pasien berdasarkan tingkat prioritas |
| 4 | 🔍 **BFS Traversal** | Queue untuk Graph | Pencarian jalur breadth-first pada graph |
| 5 | ✈️ **Loket Bandara** | Multi-Server Queue | Antrian penumpang dengan 2 loket pelayanan |

---

## 🚀 CARA MENJALANKAN

### Prasyarat
- Python 3.8 atau lebih baru
- Tkinter (sudah termasuk dalam instalasi Python standar)

### Langkah-langkah

1. **Clone atau download** file `queue_simulation_farid.py`

2. **Jalankan program** melalui terminal/command prompt:
```bash
python queue_simulation_farid.py
Atau jika menggunakan Python 3 (Linux/Mac):

bash
python3 queue_simulation_farid.py
🎮 FITUR PROGRAM
1. Printer Queue (FIFO)
✅ Tambah dokumen ke antrian

✅ Cetak dokumen (dequeue)

✅ Auto print otomatis

✅ Visualisasi box antrian dengan warna berbeda

2. Hot Potato (Circular Queue)
✅ Lempar kentang secara melingkar

✅ Eliminasi pemain yang memegang kentang

✅ Visualisasi lingkaran pemain

✅ Tampilkan pemenang di akhir game

3. Antrian Rumah Sakit (Priority Queue)
✅ 4 level prioritas (Kritis → Darurat → Normal → Standar)

✅ Tambah pasien dengan prioritas tertentu

✅ Panggil pasien (prioritas tertinggi keluar pertama)

✅ Tabel antrian dengan warna prioritas

4. BFS Traversal (Queue untuk Graph)
✅ Step-by-step simulasi BFS

✅ Auto BFS traversal

✅ Visualisasi graph dengan perubahan warna node

✅ Tampilkan queue dan hasil traversal

5. Loket Bandara (Multi-Server Queue)
✅ Satu antrian umum untuk 2 loket

✅ Dispatch penumpang ke loket kosong

✅ Selesai layanan per loket

✅ Statistik total penumpang dilayani

🎨 TAMPILAN PROGRAM
text
┌─────────────────────────────────────────────────────────────────┐
│  📊 QUEUE SIMULATION STUDIO                    FARID | 25091397050 │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌─────────────────────────────────────────────────┐ │
│ │ MENU     │ │                                                 │ │
│ │ 🖨️ Printer│ │            SIMULASI AKTIF TAMPIL DI SINI        │ │
│ │ 🥔 HotPot │ │                                                 │ │
│ │ 🏥 RSakit │ │    ┌─────┐  ┌─────┐  ┌─────┐                   │ │
│ │ 🔍 BFS    │ │    │ A  │→│ B  │→│ C  │                   │ │
│ │ ✈️ Bandara│ │    └─────┘  └─────┘  └─────┘                   │ │
│ │          │ │              ↑ FRONT    REAR ↑                  │ │
│ └──────────┘ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
📁 STRUKTUR FILE
text
📂 project-queue-farid/
├── 📄 queue_simulation_farid.py   # File program utama
└── 📄 README.md                    # Dokumentasi program
🔧 KONSEP QUEUE YANG DIBAHAS
Konsep	Penjelasan
FIFO	First In First Out - elemen pertama masuk adalah pertama keluar
Enqueue	Operasi menambah elemen di belakang antrian
Dequeue	Operasi menghapus elemen dari depan antrian
Front	Posisi elemen terdepan dalam antrian
Rear/Back	Posisi elemen terakhir dalam antrian
Priority Queue	Antrian dengan prioritas (min-heap implementation)
Circular Queue	Antrian melingkar untuk game Hot Potato
Multi-Server	Satu antrian dilayani beberapa server/loket
💻 KOMPLEKSITAS OPERASI
Operasi	Kompleksitas	Keterangan
Enqueue	O(1)	Tambah elemen di belakang
Dequeue	O(1)	Hapus elemen dari depan
Peek/Front	O(1)	Lihat elemen depan
isEmpty	O(1)	Cek kekosongan
Priority Enqueue	O(log n)	Heap push operation
Priority Dequeue	O(log n)	Heap pop operation
📸 SCREENSHOT
[Sertakan screenshot program di sini setelah menjalankan]

📞 KONTAK
Nama: FARID AHMAD SANTOSO

NIM: 25091397050

Kelas: 2025B

📜 LICENSE
Copyright © 2025 - FARID AHMAD SANTOSO

Dibuat untuk memenuhi tugas mata kuliah Struktur Data & Algoritma Semester 2.
