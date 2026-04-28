#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║     SIMULASI QUEUE — APLIKASI DESKTOP INTERAKTIF                     ║
║     =============================================                     ║
║                                                                       ║
║     NAMA  : FARID AHMAD SANTOSO                                       ║
║     NIM   : 25091397050                                               ║
║     KELAS : 2025B                                                     ║
║     MATA KULIAH : Struktur Data & Algoritma                           ║
║     SEMESTER : 2 (Genap)                                              ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║  CARA MENJALANKAN:                                                    ║
║    python queue_simulation_farid.py                                   ║
║                                                                       ║
║  REQUIREMENTS:                                                        ║
║    Python 3.8+  +  Tkinter (sudah built-in)                           ║
╚═══════════════════════════════════════════════════════════════════════╝

5 SIMULASI QUEUE YANG TERSEDIA:
  1. Antrian Printer      → FIFO Queue (First In First Out)
  2. Hot Potato           → Circular Queue (Permainan Eliminasi)
  3. Antrian Rumah Sakit  → Priority Queue (Prioritas Pasien)
  4. BFS Traversal        → Queue untuk Graph (Breadth First Search)
  5. Loket Bandara        → Multi-Server Queue (2 Loket)
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import heapq
from collections import deque
import random
import math


# ═══════════════════════════════════════════════════════════════════════
#  KONFIGURASI WARNA & FONT
# ═══════════════════════════════════════════════════════════════════════

WARNA = {
    # Background utama
    "bg_dark"       : "#0A0E27",    # biru sangat gelap
    "bg_medium"     : "#1A1F3E",    # panel medium
    "bg_light"      : "#252A4A",    # panel lebih terang
    "bg_card"       : "#2D3258",    # card element
    "bg_hover"      : "#3B4180",    # hover state
    
    # Warna aksen
    "primary"       : "#6366F1",    # indigo
    "success"       : "#10B981",    # hijau
    "danger"        : "#EF4444",    # merah
    "warning"       : "#F59E0B",    # kuning
    "info"          : "#3B82F6",    # biru
    "purple"        : "#8B5CF6",    # ungu
    
    # Warna teks
    "text_white"    : "#F8FAFC",
    "text_gray"     : "#94A3B8",
    "text_dark"     : "#CBD5E1",
    
    # Prioritas RS
    "critical"      : "#DC2626",
    "emergency"     : "#F97316",
    "normal"        : "#22C55E",
    "standard"      : "#3B82F6",
    
    # Status loket
    "loket_free"    : "#10B981",
    "loket_busy"    : "#F59E0B",
}

FONT = {
    "title"     : ("Poppins", 20, "bold"),
    "subtitle"  : ("Poppins", 14, "bold"),
    "heading"   : ("Segoe UI", 12, "bold"),
    "normal"    : ("Segoe UI", 10),
    "small"     : ("Segoe UI", 9),
    "mono"      : ("Consolas", 10),
    "badge"     : ("Segoe UI", 11, "bold"),
}

# Konstanta
LEBAR_APP = 1200
TINGGI_APP = 720
ANIMASI_DELAY = 550  # milidetik


# ═══════════════════════════════════════════════════════════════════════
#  KOMPONEN UI KUSTOM
# ═══════════════════════════════════════════════════════════════════════

class CustomButton(tk.Canvas):
    """Tombol modern dengan efek hover dan animasi."""
    
    def __init__(self, parent, text, color, command, width=140, height=36, icon="", **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=WARNA["bg_medium"])
        self.command = command
        self.text = text
        self.color = color
        self.icon = icon
        self.width = width
        self.height = height
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self._draw_button(self.color)
        
    def _draw_button(self, bg_color):
        self.delete("all")
        # Shadow
        self.create_rounded_rect(2, 2, self.width, self.height, 8, "#0A0E27", outline="")
        # Main button
        self.create_rounded_rect(0, 0, self.width-2, self.height-2, 8, bg_color, outline="")
        # Text
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.create_text(self.width//2, self.height//2 - 1, 
                        text=display_text, fill="white", 
                        font=FONT["normal"], anchor="center")
        
    def create_rounded_rect(self, x1, y1, x2, y2, r, fill, outline=""):
        self.create_polygon(
            x1+r, y1, x2-r, y1,
            x2, y1, x2, y1+r,
            x2, y2-r, x2, y2,
            x2-r, y2, x1+r, y2,
            x1, y2, x1, y2-r,
            x1, y1+r, x1, y1,
            fill=fill, outline=outline, smooth=True
        )
        
    def _on_click(self, event):
        if self.command:
            self.command()
            
    def _on_enter(self, event):
        self._draw_button(self._lighten_color(self.color))
        
    def _on_leave(self, event):
        self._draw_button(self.color)
        
    def _lighten_color(self, hex_color):
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02X}{g:02X}{b:02X}"


class StatusLabel(tk.Label):
    """Label status dengan animasi teks."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=WARNA["bg_card"], fg=WARNA["text_gray"],
                        font=FONT["normal"], anchor="w", padx=12, pady=8,
                        relief="flat", **kwargs)
        
    def update_status(self, message, color=None):
        self.config(text=f"● {message}", fg=color or WARNA["text_gray"])
        self.after(3000, lambda: self.config(fg=WARNA["text_gray"] 
                  if self.cget("fg") != WARNA["danger"] else None))


class QueueVisualizer(tk.Canvas):
    """Visualisasi antrian dengan box vertikal/horizontal."""
    
    BOX_WIDTH = 100
    BOX_HEIGHT = 60
    SPACING = 12
    
    def __init__(self, parent, height=120, **kwargs):
        super().__init__(parent, bg=WARNA["bg_medium"], height=height,
                        highlightthickness=0, **kwargs)
        
    def draw_queue(self, items, colors=None, start_idx=0):
        """Menggambar antrian dalam bentuk box horizontal."""
        self.delete("all")
        
        if not items:
            self.create_text(self.winfo_width()//2, self.BOX_HEIGHT//2 + 10,
                           text="[ ANTRIAN KOSONG ]", fill=WARNA["text_gray"],
                           font=FONT["small"])
            return
            
        colors = colors or {}
        total_width = len(items) * (self.BOX_WIDTH + self.SPACING)
        start_x = max(10, (self.winfo_width() - total_width) // 2)
        
        for i, item in enumerate(items):
            x1 = start_x + i * (self.BOX_WIDTH + self.SPACING)
            y1 = 15
            x2 = x1 + self.BOX_WIDTH
            y2 = y1 + self.BOX_HEIGHT
            
            # Box color
            fill_color = colors.get(i, WARNA["primary"])
            if fill_color == WARNA["success"]:
                border = WARNA["success"]
            else:
                border = WARNA["bg_light"]
                
            # Draw rounded box
            self._draw_rounded_box(x1, y1, x2, y2, 8, fill_color, border)
            
            # Item text
            item_text = str(item)[:10] + ".." if len(str(item)) > 12 else str(item)
            self.create_text((x1+x2)//2, (y1+y2)//2 - 5, text=item_text,
                            fill="white", font=FONT["heading"])
            
            # Index badge
            self.create_text((x1+x2)//2, y2-8, text=f"[{i+1}]",
                            fill=WARNA["text_gray"], font=FONT["small"])
        
        # Labels FRONT & REAR
        if items:
            self.create_text(start_x + self.BOX_WIDTH//2, y2 + 12,
                           text="↑ FRONT", fill=WARNA["warning"], font=FONT["small"])
            self.create_text(start_x + (len(items)-1)*(self.BOX_WIDTH+self.SPACING) + self.BOX_WIDTH//2,
                           y2 + 12, text="REAR ↑", fill=WARNA["warning"], font=FONT["small"])
            
    def _draw_rounded_box(self, x1, y1, x2, y2, r, fill, outline):
        """Menggambar kotak dengan sudut membulat."""
        points = [
            x1+r, y1, x2-r, y1,
            x2, y1, x2, y1+r,
            x2, y2-r, x2, y2,
            x2-r, y2, x1+r, y2,
            x1, y2, x1, y2-r,
            x1, y1+r, x1, y1
        ]
        self.create_polygon(points, fill=fill, outline=outline, smooth=True, width=2)


# ═══════════════════════════════════════════════════════════════════════
#  SIMULASI 1: ANTRIAN PRINTER (FIFO QUEUE)
# ═══════════════════════════════════════════════════════════════════════

class PrinterQueuePanel(tk.Frame):
    """Panel simulasi antrian printer."""
    
    CONTOH_DOKUMEN = [
        "Laporan_TA_Final.pdf", "Praktikum_StrukturData.docx", 
        "Data_Mahasiswa.xlsx", "Presentation_Slides.pptx",
        "KRS_Semester_2.pdf", "Tugas_Besar.pdf"
    ]
    
    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_light"])
        self.queue = deque()
        self.item_colors = {}
        self.is_animating = False
        self.doc_counter = 0
        self._setup_ui()
        self._load_initial_data()
        
    def _setup_ui(self):
        # Header
        header = tk.Frame(self, bg=WARNA["bg_light"])
        header.pack(fill="x", padx=20, pady=(15, 5))
        
        tk.Label(header, text="🖨️", font=("Segoe UI", 28), bg=WARNA["bg_light"]).pack(side="left")
        tk.Label(header, text="Antrian Printer", font=FONT["subtitle"], 
                fg=WARNA["text_white"], bg=WARNA["bg_light"]).pack(side="left", padx=10)
        
        desc = tk.Label(self, text="Sistem antrian FIFO (First In First Out) — Dokumen dicetak sesuai urutan masuk",
                       bg=WARNA["bg_light"], fg=WARNA["text_gray"], font=FONT["small"])
        desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Queue visualizer
        queue_frame = tk.LabelFrame(self, text="📋 Antrian Dokumen", bg=WARNA["bg_medium"],
                                   fg=WARNA["text_white"], font=FONT["normal"])
        queue_frame.pack(fill="x", padx=20, pady=5)
        
        self.queue_canvas = QueueVisualizer(queue_frame, height=110)
        self.queue_canvas.pack(fill="x", padx=10, pady=10)
        
        # Printer status
        printer_frame = tk.Frame(self, bg=WARNA["bg_light"])
        printer_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(printer_frame, text="🖨️ Printer Status:", font=FONT["heading"],
                bg=WARNA["bg_light"], fg=WARNA["text_white"]).pack(side="left")
        
        self.printer_status = tk.Label(printer_frame, text="● IDLE - Menunggu dokumen",
                                       bg=WARNA["bg_card"], fg=WARNA["success"],
                                       font=FONT["normal"], padx=15, pady=5)
        self.printer_status.pack(side="left", padx=15)
        
        # Status log
        self.status_log = StatusLabel(self)
        self.status_log.pack(fill="x", padx=20, pady=8)
        
        # Input controls
        controls = tk.Frame(self, bg=WARNA["bg_light"])
        controls.pack(pady=15)
        
        self.doc_entry = tk.Entry(controls, width=35, font=FONT["normal"],
                                  bg=WARNA["bg_card"], fg=WARNA["text_white"],
                                  insertbackground="white", relief="flat", bd=5)
        self.doc_entry.insert(0, self.CONTOH_DOKUMEN[0])
        self.doc_entry.pack(side="left", padx=5, ipady=4)
        
        CustomButton(controls, "Tambah", WARNA["success"], self._enqueue,
                    width=100, icon="📄").pack(side="left", padx=5)
        CustomButton(controls, "Cetak", WARNA["danger"], self._dequeue,
                    width=100, icon="🖨️").pack(side="left", padx=5)
        CustomButton(controls, "Auto Print", WARNA["info"], self._auto_print,
                    width=120, icon="⚡").pack(side="left", padx=5)
        CustomButton(controls, "Reset", WARNA["text_gray"], self._reset,
                    width=100, icon="🔄").pack(side="left", padx=5)
        
        # Legend
        self._add_legend()
        
    def _add_legend(self):
        legend = tk.Frame(self, bg=WARNA["bg_light"])
        legend.pack(anchor="w", padx=20, pady=(10, 5))
        
        for color, label in [(WARNA["primary"], "Menunggu"),
                            (WARNA["success"], "Baru Ditambahkan"),
                            (WARNA["warning"], "Sedang Dicetak")]:
            tk.Label(legend, text="■", bg=WARNA["bg_light"], fg=color,
                    font=("Segoe UI", 12)).pack(side="left")
            tk.Label(legend, text=f" {label}  ", bg=WARNA["bg_light"],
                    fg=WARNA["text_gray"], font=FONT["small"]).pack(side="left")
            
    def _load_initial_data(self):
        for doc in self.CONTOH_DOKUMEN[:4]:
            self.queue.append(doc)
        self._refresh_display()
        
    def _refresh_display(self):
        self.queue_canvas.draw_queue(list(self.queue), self.item_colors)
        
    def _enqueue(self):
        if self.is_animating:
            return
        doc = self.doc_entry.get().strip()
        if not doc:
            self.status_log.update_status("Masukkan nama dokumen terlebih dahulu!", WARNA["danger"])
            return
            
        self.queue.append(doc)
        idx = len(self.queue) - 1
        self.item_colors[idx] = WARNA["success"]
        self._refresh_display()
        self.status_log.update_status(f"📄 '{doc}' masuk antrian (posisi #{len(self.queue)})", WARNA["success"])
        
        self.doc_counter = (self.doc_counter + 1) % len(self.CONTOH_DOKUMEN)
        self.doc_entry.delete(0, "end")
        self.doc_entry.insert(0, self.CONTOH_DOKUMEN[self.doc_counter])
        
        self.after(800, lambda: self._normalize_colors())
        
    def _normalize_colors(self):
        for i in range(len(self.queue)):
            if self.item_colors.get(i) == WARNA["success"]:
                self.item_colors[i] = WARNA["primary"]
        self._refresh_display()
        
    def _dequeue(self):
        if self.is_animating or not self.queue:
            if not self.queue:
                self.status_log.update_status("Antrian kosong! Tidak ada dokumen.", WARNA["danger"])
            return
            
        self.is_animating = True
        self.item_colors[0] = WARNA["warning"]
        self._refresh_display()
        self.printer_status.config(text="● PRINTING - Sedang mencetak...", fg=WARNA["warning"])
        self.status_log.update_status("🖨️ Mencetak dokumen...", WARNA["warning"])
        self.after(ANIMASI_DELAY, self._complete_dequeue)
        
    def _complete_dequeue(self):
        if not self.queue:
            self.is_animating = False
            return
        doc = self.queue.popleft()
        self.item_colors = {i: self.item_colors.get(i+1, WARNA["primary"]) 
                           for i in range(len(self.queue))}
        self._refresh_display()
        self.printer_status.config(text=f"✅ Selesai: {doc}", fg=WARNA["success"])
        self.status_log.update_status(f"✅ '{doc}' selesai dicetak!", WARNA["success"])
        self.is_animating = False
        
        self.after(1500, lambda: self.printer_status.config(
            text="● IDLE - Menunggu dokumen", fg=WARNA["success"]))
        
    def _auto_print(self):
        if self.is_animating or not self.queue:
            return
        self._dequeue()
        if self.queue:
            self.after(ANIMASI_DELAY + 300, self._auto_print)
            
    def _reset(self):
        self.queue.clear()
        self.item_colors.clear()
        self.is_animating = False
        self._refresh_display()
        self.printer_status.config(text="● IDLE - Menunggu dokumen", fg=WARNA["success"])
        self.status_log.update_status("🔄 Reset antrian! Memuat data awal...")
        self._load_initial_data()


# ═══════════════════════════════════════════════════════════════════════
#  SIMULASI 2: HOT POTATO (CIRCULAR QUEUE)
# ═══════════════════════════════════════════════════════════════════════

class HotPotatoPanel(tk.Frame):
    """Panel simulasi permainan Hot Potato."""
    
    PEMAIN_DEFAULT = ["Ahmad", "Bella", "Citra", "Dian", "Eko", "Fina", "Gilang"]
    ITERASI = 5
    
    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_light"])
        self.players = deque(self.PEMAIN_DEFAULT.copy())
        self.current_holder = 0
        self.eliminated = []
        self.is_passing = False
        self.round_num = 1
        self._setup_ui()
        self._draw_circle()
        
    def _setup_ui(self):
        # Header
        header = tk.Frame(self, bg=WARNA["bg_light"])
        header.pack(fill="x", padx=20, pady=(15, 5))
        
        tk.Label(header, text="🥔", font=("Segoe UI", 28), bg=WARNA["bg_light"]).pack(side="left")
        tk.Label(header, text="Hot Potato Game", font=FONT["subtitle"],
                fg=WARNA["text_white"], bg=WARNA["bg_light"]).pack(side="left", padx=10)
        
        desc = tk.Label(self, text="Permainan sirkular menggunakan Queue — Pemain dieliminasi setiap putaran",
                       bg=WARNA["bg_light"], fg=WARNA["text_gray"], font=FONT["small"])
        desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Canvas untuk lingkaran pemain
        canvas_frame = tk.LabelFrame(self, text="🎮 Arena Permainan", bg=WARNA["bg_medium"],
                                    fg=WARNA["text_white"], font=FONT["normal"])
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.circle_canvas = tk.Canvas(canvas_frame, bg=WARNA["bg_medium"],
                                       highlightthickness=0)
        self.circle_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.circle_canvas.bind("<Configure>", lambda e: self._draw_circle())
        
        # Game info
        info_frame = tk.Frame(self, bg=WARNA["bg_light"])
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.round_label = tk.Label(info_frame, text=f"Ronde: {self.round_num}",
                                    font=FONT["subtitle"], fg=WARNA["warning"],
                                    bg=WARNA["bg_light"])
        self.round_label.pack(side="left", padx=20)
        
        self.remaining_label = tk.Label(info_frame, text=f"Pemain Tersisa: {len(self.players)}",
                                        font=FONT["normal"], fg=WARNA["text_white"],
                                        bg=WARNA["bg_light"])
        self.remaining_label.pack(side="left", padx=20)
        
        self.eliminated_label = tk.Label(info_frame, text="Tersingkir: -",
                                         font=FONT["normal"], fg=WARNA["danger"],
                                         bg=WARNA["bg_light"])
        self.eliminated_label.pack(side="left", padx=20)
        
        # Status log
        self.status_log = StatusLabel(self)
        self.status_log.pack(fill="x", padx=20, pady=8)
        
        # Controls
        controls = tk.Frame(self, bg=WARNA["bg_light"])
        controls.pack(pady=15)
        
        CustomButton(controls, "Lempar Kentang", WARNA["info"], self._start_passing,
                    width=140, icon="🥔").pack(side="left", padx=5)
        CustomButton(controls, "Eliminasi", WARNA["danger"], self._eliminate,
                    width=120, icon="💀").pack(side="left", padx=5)
        CustomButton(controls, "Reset Game", WARNA["text_gray"], self._reset,
                    width=120, icon="🔄").pack(side="left", padx=5)
        
    def _draw_circle(self):
        """Menggambar lingkaran pemain di canvas."""
        self.circle_canvas.delete("all")
        w = self.circle_canvas.winfo_width() or 500
        h = self.circle_canvas.winfo_height() or 300
        cx, cy = w // 2, h // 2
        radius = min(cx, cy) - 60
        
        if radius < 50:
            radius = 50
            
        n = len(self.players)
        if n == 0:
            self.circle_canvas.create_text(cx, cy, text="GAME OVER!",
                                          fill=WARNA["danger"], font=FONT["title"])
            return
            
        for i, player in enumerate(self.players):
            angle = (2 * math.pi * i / n) - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            is_holder = (i == self.current_holder)
            node_color = WARNA["danger"] if is_holder else WARNA["primary"]
            node_radius = 32 if is_holder else 28
            
            self.circle_canvas.create_oval(x - node_radius, y - node_radius,
                                           x + node_radius, y + node_radius,
                                           fill=node_color, outline=WARNA["bg_light"], width=2)
            
            self.circle_canvas.create_text(x, y - 5, text=player[:6],
                                           fill="white", font=FONT["heading"])
            
            if is_holder:
                self.circle_canvas.create_text(x, y + 15, text="🥔",
                                               font=("Segoe UI", 16))
                
    def _start_passing(self):
        if self.is_passing or len(self.players) <= 1:
            if len(self.players) <= 1:
                self._show_winner()
            return
            
        self.is_passing = True
        self.pass_count = 0
        self._do_pass()
        
    def _do_pass(self):
        if self.pass_count >= self.ITERASI:
            self.is_passing = False
            holder = self.players[self.current_holder]
            self.status_log.update_status(f"⏹️ Musik berhenti! {holder} memegang kentang!", WARNA["warning"])
            return
            
        # Rotate
        self.players.append(self.players.popleft())
        self.current_holder = 0
        self.pass_count += 1
        
        self._draw_circle()
        holder = self.players[self.current_holder]
        self.status_log.update_status(f"🔄 Operan ke-{self.pass_count}/{self.ITERASI}: {holder} memegang", WARNA["info"])
        self.after(ANIMASI_DELAY // 2, self._do_pass)
        
    def _eliminate(self):
        if len(self.players) <= 1:
            self._show_winner()
            return
            
        if self.is_passing:
            self.status_log.update_status("Tunggu hingga lemparan selesai!", WARNA["danger"])
            return
            
        eliminated_player = self.players.popleft()
        self.eliminated.append(eliminated_player)
        
        if self.current_holder >= len(self.players):
            self.current_holder = 0
            
        self.round_num += 1
        self.round_label.config(text=f"Ronde: {self.round_num}")
        self.remaining_label.config(text=f"Pemain Tersisa: {len(self.players)}")
        self.eliminated_label.config(text=f"Tersingkir: {', '.join(self.eliminated[-3:])}")
        
        self.status_log.update_status(f"💀 {eliminated_player} tersingkir!", WARNA["danger"])
        self._draw_circle()
        
        if len(self.players) == 1:
            self._show_winner()
            
    def _show_winner(self):
        if len(self.players) == 1:
            winner = self.players[0]
            messagebox.showinfo("🏆 Pemenang!", f"Selamat! {winner} adalah pemenang Hot Potato!")
            self.status_log.update_status(f"🏆 {winner} keluar sebagai pemenang!", WARNA["success"])
            
    def _reset(self):
        self.players = deque(self.PEMAIN_DEFAULT.copy())
        self.current_holder = 0
        self.eliminated = []
        self.is_passing = False
        self.round_num = 1
        
        self.round_label.config(text="Ronde: 1")
        self.remaining_label.config(text=f"Pemain Tersisa: {len(self.players)}")
        self.eliminated_label.config(text="Tersingkir: -")
        self.status_log.update_status("🔄 Game direset! Mulai permainan baru.")
        self._draw_circle()


# ═══════════════════════════════════════════════════════════════════════
#  SIMULASI 3: ANTRIAN RUMAH SAKIT (PRIORITY QUEUE)
# ═══════════════════════════════════════════════════════════════════════

class HospitalQueuePanel(tk.Frame):
    """Panel simulasi antrian rumah sakit dengan prioritas."""
    
    PRIORITIES = {
        1: ("🚨 KRITIS", WARNA["critical"]),
        2: ("⚠️ DARURAT", WARNA["emergency"]),
        3: ("✅ NORMAL", WARNA["normal"]),
        4: ("📋 STANDAR", WARNA["standard"]),
    }
    
    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_light"])
        self.heap = []
        self.counter = 0
        self._setup_ui()
        self._load_sample()
        
    def _setup_ui(self):
        # Header
        header = tk.Frame(self, bg=WARNA["bg_light"])
        header.pack(fill="x", padx=20, pady=(15, 5))
        
        tk.Label(header, text="🏥", font=("Segoe UI", 28), bg=WARNA["bg_light"]).pack(side="left")
        tk.Label(header, text="Antrian Rumah Sakit", font=FONT["subtitle"],
                fg=WARNA["text_white"], bg=WARNA["bg_light"]).pack(side="left", padx=10)
        
        desc = tk.Label(self, text="Priority Queue — Pasien dengan prioritas tertinggi dilayani terlebih dahulu",
                       bg=WARNA["bg_light"], fg=WARNA["text_gray"], font=FONT["small"])
        desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Queue display
        queue_frame = tk.LabelFrame(self, text="📋 Daftar Antrian Pasien", bg=WARNA["bg_medium"],
                                   fg=WARNA["text_white"], font=FONT["normal"])
        queue_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Treeview for queue
        columns = ("No", "Nama Pasien", "Kondisi", "Prioritas")
        self.tree = ttk.Treeview(queue_frame, columns=columns, show="headings", height=8)
        
        self.tree.heading("No", text="No")
        self.tree.heading("Nama Pasien", text="Nama Pasien")
        self.tree.heading("Kondisi", text="Kondisi")
        self.tree.heading("Prioritas", text="Prioritas")
        
        self.tree.column("No", width=50)
        self.tree.column("Nama Pasien", width=150)
        self.tree.column("Kondisi", width=200)
        self.tree.column("Prioritas", width=120)
        
        scrollbar = ttk.Scrollbar(queue_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Style for treeview
        style = ttk.Style()
        style.configure("Treeview", background=WARNA["bg_card"], foreground="white",
                       fieldbackground=WARNA["bg_card"], font=FONT["normal"])
        style.configure("Treeview.Heading", background=WARNA["bg_dark"], foreground="white",
                       font=FONT["heading"])
        
        # Doctor status
        doctor_frame = tk.Frame(self, bg=WARNA["bg_light"])
        doctor_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(doctor_frame, text="👨‍⚕️ Dokter:", font=FONT["heading"],
                bg=WARNA["bg_light"], fg=WARNA["text_white"]).pack(side="left")
        
        self.doctor_status = tk.Label(doctor_frame, text="Menunggu pasien...",
                                      bg=WARNA["bg_card"], fg=WARNA["success"],
                                      font=FONT["normal"], padx=15, pady=5)
        self.doctor_status.pack(side="left", padx=15)
        
        # Status log
        self.status_log = StatusLabel(self)
        self.status_log.pack(fill="x", padx=20, pady=8)
        
        # Input controls
        controls = tk.Frame(self, bg=WARNA["bg_light"])
        controls.pack(pady=15)
        
        tk.Label(controls, text="Nama:", bg=WARNA["bg_light"],
                fg=WARNA["text_white"]).pack(side="left", padx=5)
        self.name_entry = tk.Entry(controls, width=15, font=FONT["normal"],
                                   bg=WARNA["bg_card"], fg="white",
                                   insertbackground="white", relief="flat", bd=5)
        self.name_entry.insert(0, "Pasien Baru")
        self.name_entry.pack(side="left", padx=5, ipady=4)
        
        tk.Label(controls, text="Prioritas:", bg=WARNA["bg_light"],
                fg=WARNA["text_white"]).pack(side="left", padx=5)
        
        self.prio_var = tk.IntVar(value=2)
        for prio in [1, 2, 3, 4]:
            tk.Radiobutton(controls, text=self.PRIORITIES[prio][0], variable=self.prio_var,
                          value=prio, bg=WARNA["bg_light"], fg=self.PRIORITIES[prio][1],
                          selectcolor=WARNA["bg_medium"], activebackground=WARNA["bg_light"],
                          font=FONT["small"]).pack(side="left", padx=3)
            
        CustomButton(controls, "Tambah Pasien", WARNA["success"], self._enqueue,
                    width=130, icon="➕").pack(side="left", padx=10)
        CustomButton(controls, "Panggil Pasien", WARNA["info"], self._dequeue,
                    width=130, icon="👨‍⚕️").pack(side="left", padx=5)
        CustomButton(controls, "Reset", WARNA["text_gray"], self._reset,
                    width=100, icon="🔄").pack(side="left", padx=5)
        
    def _load_sample(self):
        samples = [("Budi Santoso", "Sakit Kepala", 3),
                   ("Siti Aminah", "Demam Tinggi", 2),
                   ("Joko Widodo", "Serangan Jantung", 1),
                   ("Dewi Lestari", "Patah Kaki", 2),
                   ("Agus Salim", "Kontrol Rutin", 4)]
        for nama, kondisi, prio in samples:
            heapq.heappush(self.heap, (prio, self.counter, nama, kondisi))
            self.counter += 1
        self._refresh_table()
        
    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not self.heap:
            return
            
        sorted_queue = sorted(self.heap)
        for idx, (prio, _, nama, kondisi) in enumerate(sorted_queue, 1):
            prio_text, prio_color = self.PRIORITIES[prio]
            self.tree.insert("", "end", values=(idx, nama, kondisi, prio_text),
                           tags=(prio_text,))
            
        # Color tags
        for prio_text, color in self.PRIORITIES.values():
            self.tree.tag_configure(prio_text, foreground=color)
            
    def _enqueue(self):
        nama = self.name_entry.get().strip()
        if not nama:
            self.status_log.update_status("Masukkan nama pasien!", WARNA["danger"])
            return
            
        prio = self.prio_var.get()
        kondisi = {1: "Gawat Darurat", 2: "Perlu Penanganan", 3: "Umum", 4: "Ringan"}[prio]
        
        heapq.heappush(self.heap, (prio, self.counter, nama, kondisi))
        self.counter += 1
        
        prio_text, prio_color = self.PRIORITIES[prio]
        self.status_log.update_status(f"➕ {nama} ({prio_text}) masuk antrian!", prio_color)
        self._refresh_table()
        
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, f"Pasien #{self.counter + 1}")
        
    def _dequeue(self):
        if not self.heap:
            self.status_log.update_status("Antrian kosong! Tidak ada pasien.", WARNA["danger"])
            return
            
        prio, _, nama, kondisi = heapq.heappop(self.heap)
        prio_text, prio_color = self.PRIORITIES[prio]
        
        self.doctor_status.config(text=f"Menangani: {nama} ({prio_text})", fg=prio_color)
        self.status_log.update_status(f"👨‍⚕️ {nama} ({prio_text}) dipanggil ke dokter!", prio_color)
        self._refresh_table()
        
        self.after(3000, lambda: self.doctor_status.config(
            text="Menunggu pasien...", fg=WARNA["success"]))
        
    def _reset(self):
        self.heap = []
        self.counter = 0
        self._refresh_table()
        self.doctor_status.config(text="Menunggu pasien...", fg=WARNA["success"])
        self.status_log.update_status("🔄 Reset antrian! Memuat data sampel...")
        self._load_sample()


# ═══════════════════════════════════════════════════════════════════════
#  SIMULASI 4: BFS TRAVERSAL
# ═══════════════════════════════════════════════════════════════════════

class BFSPanel(tk.Frame):
    """Panel simulasi BFS traversal pada graph."""
    
    GRAPH = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['B'],
        'E': ['B', 'H'],
        'F': ['C', 'H'],
        'G': ['C'],
        'H': ['E', 'F']
    }
    
    NODE_POS = {
        'A': (0.5, 0.15),
        'B': (0.25, 0.38),
        'C': (0.75, 0.38),
        'D': (0.12, 0.68),
        'E': (0.38, 0.68),
        'F': (0.62, 0.68),
        'G': (0.88, 0.68),
        'H': (0.5, 0.88),
    }
    
    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_light"])
        self._reset_state()
        self._setup_ui()
        self._draw_graph()
        
    def _reset_state(self):
        self.queue = deque()
        self.visited = set()
        self.order = []
        self.node_colors = {node: WARNA["text_gray"] for node in self.GRAPH}
        self.current_step = 0
        self.is_bfs_running = False
        
    def _setup_ui(self):
        # Header
        header = tk.Frame(self, bg=WARNA["bg_light"])
        header.pack(fill="x", padx=20, pady=(15, 5))
        
        tk.Label(header, text="🔍", font=("Segoe UI", 28), bg=WARNA["bg_light"]).pack(side="left")
        tk.Label(header, text="BFS Graph Traversal", font=FONT["subtitle"],
                fg=WARNA["text_white"], bg=WARNA["bg_light"]).pack(side="left", padx=10)
        
        desc = tk.Label(self, text="Breadth First Search menggunakan Queue — Menjelajah level demi level",
                       bg=WARNA["bg_light"], fg=WARNA["text_gray"], font=FONT["small"])
        desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Canvas untuk graph
        graph_frame = tk.LabelFrame(self, text="🕸️ Graph Representation", bg=WARNA["bg_medium"],
                                   fg=WARNA["text_white"], font=FONT["normal"])
        graph_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.graph_canvas = tk.Canvas(graph_frame, bg=WARNA["bg_medium"], highlightthickness=0)
        self.graph_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.graph_canvas.bind("<Configure>", lambda e: self._draw_graph())
        
        # Info panel
        info_frame = tk.Frame(self, bg=WARNA["bg_light"])
        info_frame.pack(fill="x", padx=20, pady=10)
        
        left_info = tk.Frame(info_frame, bg=WARNA["bg_light"])
        left_info.pack(side="left", expand=True, fill="both")
        
        tk.Label(left_info, text="Queue BFS:", font=FONT["heading"],
                bg=WARNA["bg_light"], fg=WARNA["text_white"]).pack(anchor="w")
        self.queue_label = tk.Label(left_info, text="[ ]", bg=WARNA["bg_card"],
                                   fg=WARNA["warning"], font=FONT["mono"], padx=10, pady=5)
        self.queue_label.pack(fill="x", pady=5)
        
        right_info = tk.Frame(info_frame, bg=WARNA["bg_light"])
        right_info.pack(side="right", expand=True, fill="both")
        
        tk.Label(right_info, text="Hasil Traversal:", font=FONT["heading"],
                bg=WARNA["bg_light"], fg=WARNA["text_white"]).pack(anchor="w")
        self.order_label = tk.Label(right_info, text="-", bg=WARNA["bg_card"],
                                   fg=WARNA["success"], font=FONT["mono"], padx=10, pady=5)
        self.order_label.pack(fill="x", pady=5)
        
        # Status log
        self.status_log = StatusLabel(self)
        self.status_log.pack(fill="x", padx=20, pady=8)
        
        # Controls
        controls = tk.Frame(self, bg=WARNA["bg_light"])
        controls.pack(pady=15)
        
        CustomButton(controls, "Step by Step", WARNA["info"], self._step_bfs,
                    width=130, icon="▶").pack(side="left", padx=5)
        CustomButton(controls, "Auto BFS", WARNA["success"], self._auto_bfs,
                    width=120, icon="⚡").pack(side="left", padx=5)
        CustomButton(controls, "Reset", WARNA["text_gray"], self._reset_bfs,
                    width=100, icon="🔄").pack(side="left", padx=5)
        
    def _draw_graph(self):
        w = self.graph_canvas.winfo_width() or 500
        h = self.graph_canvas.winfo_height() or 300
        self.graph_canvas.delete("all")
        
        # Draw edges
        for node, neighbors in self.GRAPH.items():
            x1, y1 = self.NODE_POS[node][0] * w, self.NODE_POS[node][1] * h
            for neighbor in neighbors:
                x2, y2 = self.NODE_POS[neighbor][0] * w, self.NODE_POS[neighbor][1] * h
                if node < neighbor:
                    self.graph_canvas.create_line(x1, y1, x2, y2, fill="#4B5563", width=2)
                    
        # Draw nodes
        for node in self.GRAPH:
            x, y = self.NODE_POS[node][0] * w, self.NODE_POS[node][1] * h
            color = self.node_colors.get(node, WARNA["primary"])
            
            self.graph_canvas.create_oval(x - 25, y - 25, x + 25, y + 25,
                                         fill=color, outline=WARNA["bg_light"], width=2)
            self.graph_canvas.create_text(x, y, text=node, fill="white",
                                         font=("Segoe UI", 14, "bold"))
            
    def _step_bfs(self):
        if self.is_bfs_running:
            self.status_log.update_status("BFS sedang berjalan!", WARNA["danger"])
            return
            
        # Initialize BFS
        if self.current_step == 0:
            self._reset_state()
            self.queue.append('A')
            self.visited.add('A')
            self.node_colors['A'] = WARNA["warning"]
            self._update_info()
            self.status_log.update_status("ENQUEUE 'A' → BFS dimulai!", WARNA["info"])
            self.current_step += 1
            self._draw_graph()
            return
            
        if not self.queue:
            result = " → ".join(self.order)
            self.status_log.update_status(f"✅ BFS Selesai! Urutan: {result}", WARNA["success"])
            self.is_bfs_running = True
            return
            
        # Dequeue current node
        node = self.queue.popleft()
        self.order.append(node)
        self.node_colors[node] = WARNA["success"]
        
        # Enqueue unvisited neighbors
        new_neighbors = []
        for neighbor in self.GRAPH[node]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.queue.append(neighbor)
                self.node_colors[neighbor] = WARNA["warning"]
                new_neighbors.append(neighbor)
                
        self._update_info()
        msg = f"Kunjungi '{node}'"
        if new_neighbors:
            msg += f" → Enqueue: {new_neighbors}"
        self.status_log.update_status(msg, WARNA["primary"])
        self._draw_graph()
        self.current_step += 1
        
    def _update_info(self):
        self.queue_label.config(text=str(list(self.queue)))
        self.order_label.config(text=" → ".join(self.order) if self.order else "-")
        
    def _auto_bfs(self):
        if self.is_bfs_running:
            return
        self._step_bfs()
        if self.queue or self.current_step <= 1:
            self.after(ANIMASI_DELAY, self._auto_bfs)
        else:
            self.is_bfs_running = True
            
    def _reset_bfs(self):
        self._reset_state()
        self.current_step = 0
        self.is_bfs_running = False
        self._update_info()
        self._draw_graph()
        self.status_log.update_status("🔄 Reset BFS! Tekan 'Step by Step' untuk memulai.")


# ═══════════════════════════════════════════════════════════════════════
#  SIMULASI 5: LOKET BANDARA (MULTI-SERVER QUEUE)
# ═══════════════════════════════════════════════════════════════════════

class AirportPanel(tk.Frame):
    """Panel simulasi multi-server queue bandara."""
    
    PENUMPANG = [
        ("Budi", "CGK"), ("Siti", "SUB"), ("Joko", "DPS"),
        ("Dewi", "MDN"), ("Rudi", "BPN"), ("Ani", "UPG"),
        ("Cahyo", "YIA"), ("Linda", "LOP")
    ]
    
    def __init__(self, parent):
        super().__init__(parent, bg=WARNA["bg_light"])
        self.queue = deque()
        self.counters = {"Loket 1": None, "Loket 2": None}
        self.served_count = 0
        self.passenger_idx = 0
        self._setup_ui()
        self._load_initial()
        
    def _setup_ui(self):
        # Header
        header = tk.Frame(self, bg=WARNA["bg_light"])
        header.pack(fill="x", padx=20, pady=(15, 5))
        
        tk.Label(header, text="✈️", font=("Segoe UI", 28), bg=WARNA["bg_light"]).pack(side="left")
        tk.Label(header, text="Loket Bandara", font=FONT["subtitle"],
                fg=WARNA["text_white"], bg=WARNA["bg_light"]).pack(side="left", padx=10)
        
        desc = tk.Label(self, text="Multi-Server Queue — Satu antrian, dua loket pelayanan",
                       bg=WARNA["bg_light"], fg=WARNA["text_gray"], font=FONT["small"])
        desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Two columns layout
        main_frame = tk.Frame(self, bg=WARNA["bg_light"])
        main_frame.pack(fill="both", expand=True, padx=20)
        
        # Left: Queue
        left_frame = tk.Frame(main_frame, bg=WARNA["bg_light"])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        queue_title = tk.Label(left_frame, text="📋 Antrian Penumpang", font=FONT["heading"],
                              bg=WARNA["bg_light"], fg=WARNA["text_white"])
        queue_title.pack(anchor="w")
        
        self.queue_canvas = QueueVisualizer(left_frame, height=120)
        self.queue_canvas.pack(fill="x", pady=5)
        
        # Right: Counters
        right_frame = tk.Frame(main_frame, bg=WARNA["bg_light"])
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        counters_title = tk.Label(right_frame, text="🪧 Status Loket", font=FONT["heading"],
                                 bg=WARNA["bg_light"], fg=WARNA["text_white"])
        counters_title.pack(anchor="w")
        
        self.counters_frame = tk.Frame(right_frame, bg=WARNA["bg_medium"])
        self.counters_frame.pack(fill="both", expand=True, pady=5)
        
        # Statistics
        stat_frame = tk.Frame(self, bg=WARNA["bg_light"])
        stat_frame.pack(fill="x", padx=20, pady=10)
        
        self.stat_label = tk.Label(stat_frame, text="Total Dilayani: 0 penumpang",
                                   font=FONT["normal"], bg=WARNA["bg_light"],
                                   fg=WARNA["success"])
        self.stat_label.pack(side="left")
        
        # Status log
        self.status_log = StatusLabel(self)
        self.status_log.pack(fill="x", padx=20, pady=8)
        
        # Controls
        controls = tk.Frame(self, bg=WARNA["bg_light"])
        controls.pack(pady=15)
        
        CustomButton(controls, "Tambah Penumpang", WARNA["success"], self._enqueue,
                    width=150, icon="➕").pack(side="left", padx=5)
        CustomButton(controls, "Layani Ke Loket", WARNA["info"], self._dispatch,
                    width=150, icon="✈️").pack(side="left", padx=5)
        CustomButton(controls, "Auto Run", WARNA["warning"], self._auto_run,
                    width=120, icon="⚡").pack(side="left", padx=5)
        CustomButton(controls, "Reset", WARNA["text_gray"], self._reset,
                    width=100, icon="🔄").pack(side="left", padx=5)
        
    def _load_initial(self):
        for nama, tujuan in self.PENUMPANG[:5]:
            self.queue.append((nama, tujuan))
        self._refresh_display()
        
    def _refresh_display(self):
        # Refresh queue canvas
        items = [f"{p[0]}\n→{p[1]}" for p in self.queue]
        self.queue_canvas.draw_queue(items)
        
        # Refresh counters
        for widget in self.counters_frame.winfo_children():
            widget.destroy()
            
        for name, passenger in self.counters.items():
            frame = tk.Frame(self.counters_frame, bg=WARNA["bg_card"], pady=10, padx=10)
            frame.pack(fill="x", pady=4)
            
            is_busy = passenger is not None
            status_color = WARNA["loket_busy"] if is_busy else WARNA["loket_free"]
            status_text = f"🔴 {passenger[0]} → {passenger[1]}" if is_busy else "🟢 Kosong"
            
            tk.Label(frame, text=f"🪧 {name}", bg=WARNA["bg_card"],
                    fg=status_color, font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(frame, text=status_text, bg=WARNA["bg_card"],
                    fg=WARNA["text_gray"], font=FONT["small"]).pack(anchor="w")
            
            if is_busy:
                tk.Button(frame, text="✅ Selesai",
                         command=lambda l=name: self._complete_service(l),
                         bg=WARNA["success"], fg="white", font=FONT["small"],
                         relief="flat", padx=10, pady=3).pack(anchor="w", pady=(5, 0))
                
    def _enqueue(self):
        if self.passenger_idx >= len(self.PENUMPANG):
            self.passenger_idx = 0
            
        nama, tujuan = self.PENUMPANG[self.passenger_idx]
        self.passenger_idx += 1
        self.queue.append((nama, tujuan))
        self.status_log.update_status(f"➕ {nama} ({tujuan}) masuk antrian!", WARNA["success"])
        self._refresh_display()
        
    def _dispatch(self):
        free_counter = next((c for c, p in self.counters.items() if p is None), None)
        if not free_counter:
            self.status_log.update_status("Semua loket sedang sibuk!", WARNA["danger"])
            return
            
        if not self.queue:
            self.status_log.update_status("Antrian kosong!", WARNA["danger"])
            return
            
        passenger = self.queue.popleft()
        self.counters[free_counter] = passenger
        self.status_log.update_status(f"✈️ {passenger[0]} diarahkan ke {free_counter}", WARNA["info"])
        self._refresh_display()
        
    def _complete_service(self, counter):
        passenger = self.counters[counter]
        if passenger:
            self.counters[counter] = None
            self.served_count += 1
            self.stat_label.config(text=f"Total Dilayani: {self.served_count} penumpang")
            self.status_log.update_status(f"✅ {passenger[0]} selesai check-in di {counter}!", WARNA["success"])
            self._refresh_display()
            
    def _auto_run(self):
        self._dispatch()
        if self.queue or any(p is not None for p in self.counters.values()):
            self.after(ANIMASI_DELAY, self._auto_run)
            
    def _reset(self):
        self.queue = deque()
        self.counters = {"Loket 1": None, "Loket 2": None}
        self.served_count = 0
        self.passenger_idx = 0
        self.stat_label.config(text="Total Dilayani: 0 penumpang")
        self.status_log.update_status("🔄 Reset sistem!")
        self._refresh_display()
        self._load_initial()


# ═══════════════════════════════════════════════════════════════════════
#  APLIKASI UTAMA
# ═══════════════════════════════════════════════════════════════════════

class QueueSimulationApp(tk.Tk):
    """Aplikasi utama dengan navigasi sidebar."""
    
    MENU_ITEMS = [
        ("🖨️", "Printer Queue", PrinterQueuePanel),
        ("🥔", "Hot Potato", HotPotatoPanel),
        ("🏥", "Rumah Sakit", HospitalQueuePanel),
        ("🔍", "BFS Traversal", BFSPanel),
        ("✈️", "Loket Bandara", AirportPanel),
    ]
    
    def __init__(self):
        super().__init__()
        self.title("Queue Simulation Studio - FARID AHMAD SANTOSO")
        self.geometry(f"{LEBAR_APP}x{TINGGI_APP}")
        self.minsize(1000, 650)
        self.configure(bg=WARNA["bg_dark"])
        
        self.panels = {}
        self.current_panel = None
        
        self._setup_ui()
        self._show_panel(0)
        
    def _setup_ui(self):
        # Top bar with identity
        top_bar = tk.Frame(self, bg=WARNA["bg_medium"], height=60)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text="📊 QUEUE SIMULATION STUDIO", font=FONT["title"],
                fg=WARNA["text_white"], bg=WARNA["bg_medium"]).pack(side="left", padx=20)
        
        identity = tk.Frame(top_bar, bg=WARNA["bg_medium"])
        identity.pack(side="right", padx=20)
        
        tk.Label(identity, text="FARID AHMAD SANTOSO | 25091397050 | 2025B",
                font=FONT["small"], fg=WARNA["text_gray"], bg=WARNA["bg_medium"]).pack()
        
        # Separator
        tk.Frame(self, bg=WARNA["primary"], height=2).pack(fill="x")
        
        # Main content
        main_frame = tk.Frame(self, bg=WARNA["bg_dark"])
        main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_frame, bg=WARNA["bg_medium"], width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="MENU SIMULASI", font=FONT["heading"],
                fg=WARNA["text_white"], bg=WARNA["bg_medium"]).pack(pady=(20, 10))
        
        for idx, (icon, title, panel_class) in enumerate(self.MENU_ITEMS):
            btn = tk.Button(sidebar, text=f"  {icon}  {title}",
                           command=lambda i=idx: self._show_panel(i),
                           bg=WARNA["bg_medium"], fg=WARNA["text_gray"],
                           font=FONT["normal"], relief="flat", anchor="w",
                           padx=10, pady=12, width=18, cursor="hand2")
            btn.pack(fill="x", padx=5, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=WARNA["bg_hover"], fg="white"))
            btn.bind("<Leave>", lambda e, b=btn, i=idx: 
                    b.config(bg=WARNA["bg_medium"], fg=WARNA["text_gray"])
                    if self.current_panel != i else None)
            setattr(self, f"btn_{idx}", btn)
            
        tk.Label(sidebar, text="\nFIFO | Priority | Circular\nMulti-Server | BFS",
                font=FONT["small"], fg=WARNA["text_gray"], bg=WARNA["bg_medium"]).pack(side="bottom", pady=20)
        
        # Content area
        self.content_frame = tk.Frame(main_frame, bg=WARNA["bg_light"])
        self.content_frame.pack(side="right", fill="both", expand=True)
        
    def _show_panel(self, idx):
        if self.current_panel is not None:
            self.panels[self.current_panel].pack_forget()
            
        # Update button colors
        for i in range(len(self.MENU_ITEMS)):
            btn = getattr(self, f"btn_{i}")
            if i == idx:
                btn.config(bg=WARNA["primary"], fg="white")
            else:
                btn.config(bg=WARNA["bg_medium"], fg=WARNA["text_gray"])
        
        if idx not in self.panels:
            _, _, panel_class = self.MENU_ITEMS[idx]
            self.panels[idx] = panel_class(self.content_frame)
            
        self.panels[idx].pack(fill="both", expand=True)
        self.current_panel = idx


# ═══════════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QueueSimulationApp()
    app.mainloop()