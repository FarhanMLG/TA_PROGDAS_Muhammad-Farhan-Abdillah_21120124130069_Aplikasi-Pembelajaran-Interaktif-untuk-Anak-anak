
# Revisi:
# 1. Mengimplementasikan sistem difficulty pada setiap kategori soal. 
# 2. Mengimplementasikan sistem level maksimal pada perhitungan skor setiap soal.

import tkinter as tk
from tkinter import ttk, messagebox
import random

class Pertanyaan:
    def __init__(self, pertanyaan, opsi, opsi_benar, kategori, kesulitan):
        self.pertanyaan = pertanyaan
        self.opsi = opsi
        self.opsi_benar = opsi_benar
        self.kategori = kategori
        self.kesulitan = kesulitan

# REVISI
class User:
    def __init__(self, username, usia):
        self.username = username
        self.usia = usia
        self.skor = 0
        self.level = 1
        self.LEVEL_MAKSIMAL = 5

    # REVISI
    def update_skor(self, poins):
        if self.level < self.LEVEL_MAKSIMAL:
            self.skor += poins
            if self.skor >= self.level * 50:
                self.level += 1
                if self.level == self.LEVEL_MAKSIMAL:
                    return True  
        return False 


class BankPertanyaan:
    def __init__(self):
        self.pertanyaans = [
            # Matematika Easy
            Pertanyaan("2 + 2 = ?", ["3", "4", "5", "6"], "4", "matematika", "easy"),
            Pertanyaan("3 x 2 = ?", ["4", "5", "6", "7"], "6", "matematika", "easy"),
            Pertanyaan("10 - 5 = ?", ["3", "4", "5", "6"], "5", "matematika", "easy"),
            
            # Matematika Medium
            Pertanyaan("12 ÷ 3 = ?", ["2", "3", "4", "5"], "4", "matematika", "medium"),
            Pertanyaan("7 + 6 = ?", ["12", "13", "14", "15"], "13", "matematika", "medium"),
            Pertanyaan("9 x 3 = ?", ["24", "25", "26", "27"], "27", "matematika", "medium"),
            
            # Matematika Hard
            Pertanyaan("18 ÷ 3 + 5 = ?", ["6", "7", "8", "11"], "11", "matematika", "hard"),
            Pertanyaan("7 x 4 - 5 = ?", ["23", "24", "25", "26"], "23", "matematika", "hard"),
            Pertanyaan("15 + 8 x 2 = ?", ["31", "32", "33", "34"], "31", "matematika", "hard"),
            
            # Pengetahuan Umum Easy
            Pertanyaan("Warna pelangi?", ["Abu-abu", "Merah", "Warna-warni", "Putih"], "Warna-warni", "pengetahuan_umum", "easy"),
            Pertanyaan("Ibu Kota Indonesia?", ["Surabaya", "Bandung", "Jakarta", "Medan"], "Jakarta", "pengetahuan_umum", "easy"),
            Pertanyaan("Hewan berkaki 4?", ["Ayam", "Kucing", "Ikan", "Burung"], "Kucing", "pengetahuan_umum", "easy"),
            
            # Pengetahuan Umum Medium
            Pertanyaan("Planet terdekat dari Matahari?", ["Mars", "Venus", "Jupiter", "Merkurius"], "Merkurius", "pengetahuan_umum", "medium"),
            Pertanyaan("Benua terbesar di Dunia?", ["Eropa", "Afrika", "Asia", "Amerika"], "Asia", "pengetahuan_umum", "medium"),
            Pertanyaan("Alat musik gesek?", ["Gitar", "Piano", "Biola", "Drum"], "Biola", "pengetahuan_umum", "medium"),
            
            # Pengetahuan Umum Hard
            Pertanyaan("Ibu Kota Jepang?", ["Osaka", "Kyoto", "Tokyo", "Seoul"], "Tokyo", "pengetahuan_umum", "hard"),
            Pertanyaan("Sungai terpanjang di Dunia?", ["Amazon", "Mississippi", "Nil", "Yangtze"], "Nil", "pengetahuan_umum", "hard"),
            Pertanyaan("Tahun berakhirnya Perang Dunia II?", ["1943", "1944", "1945", "1946"], "1945", "pengetahuan_umum", "hard")
        ]

    def get_pertanyaans(self, kategori, kesulitan=None):
        if kesulitan:
            return [q for q in self.pertanyaans if q.kategori == kategori and q.kesulitan == kesulitan]
        return [q for q in self.pertanyaans if q.kategori == kategori]

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplikasi Pembelajaran")
        self.root.state('zoomed')
        self.root.configure(bg='lightblue')
        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style()
        style.configure('TButton', padding=10, font=('Helvetica', 14),)
        style.configure('TFrame', background='lightblue')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_frame(self):
        frame = ttk.Frame(self.root, style='TFrame')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        return frame

    def show_login(self):
        self.clear_window()
        frame = self.create_frame()
        
        ttk.Label(frame, text="Selamat Datang!", font=('Helvetica', 24, 'bold')).pack(pady=20)
        
        entries = {}
        for field in ['Username', 'Usia']:
            ttk.Label(frame, text=field+':', font=('Helvetica', 14)).pack()
            entries[field] = ttk.Entry(frame, font=('Helvetica', 14))
            entries[field].pack(pady=5)
        
        ttk.Button(frame, text="Masuk", command=lambda: self.login(
            entries['Username'].get(), entries['Usia'].get())).pack(pady=20)

    def login(self, username, usia):
        if not username or not usia:
            messagebox.showerror("Error", "Username dan usia harus diisi!")
            return
        
        try:
            usia = int(usia)
            if not 5 <= usia <= 12:
                messagebox.showerror("Error", "Usia harus antara 5-12 tahun!")
                return
        except ValueError:
            messagebox.showerror("Error", "Usia harus berupa angka!")
            return

        self.user = User(username, usia)
        self.bank_pertanyaan = BankPertanyaan()
        self.show_menu()

    def show_menu(self):
        self.clear_window()
        frame = self.create_frame()
        
        ttk.Label(frame, text=f"Halo, {self.user.username}!", 
                 font=('Helvetica', 24, 'bold')).pack(pady=20)
        
       
        menus = [
            ("Matematika", lambda: self.pilih_kesulitan("matematika")),
            ("Pengetahuan Umum", lambda: self.pilih_kesulitan("pengetahuan_umum")),
            ("Lihat Progress", self.tampil_progress),
            ("Keluar", self.show_login)
        ]
        
        for text, command in menus:
            ttk.Button(frame, text=text, command=command).pack(pady=10)

    def pilih_kesulitan(self, kategori):
        """Layar pemilihan tingkat kesulitan"""
        self.clear_window()
        frame = self.create_frame()
        
        ttk.Label(frame, text=f"Pilih Tingkat Kesulitan {kategori.replace('_', ' ').title()}", 
                 font=('Helvetica', 24, 'bold')).pack(pady=20)
        
        kesulitans = [
            ("Easy", lambda: self.mulai_belajar(kategori, "easy")),
            ("Medium", lambda: self.mulai_belajar(kategori, "medium")),
            ("Hard", lambda: self.mulai_belajar(kategori, "hard"))
        ]
        
        for text, command in kesulitans:
            ttk.Button(frame, text=text, command=command).pack(pady=10)

        ttk.Button(frame, text="Kembali ke Menu", command=self.show_menu).pack(pady=10)

    def mulai_belajar(self, kategori, kesulitan):
        self.clear_window()
        pertanyaans = self.bank_pertanyaan.get_pertanyaans(kategori, kesulitan)
        
        if not pertanyaans:
            messagebox.showerror("Error", "Tidak ada soal tersedia!")
            self.show_menu()
            return

        frame = self.create_frame()
        pertanyaan = random.choice(pertanyaans)
        
        ttk.Label(frame, text=pertanyaan.pertanyaan, font=('Helvetica', 16), 
                 wraplength=500).pack(pady=20)
        
        for opsi in pertanyaan.opsi:
            ttk.Button(frame, text=opsi, 
                      command=lambda o=opsi: self.cek_opsi(o, pertanyaan)).pack(pady=5)
        
        ttk.Button(frame, text="Kembali ke Menu", 
                  command=self.show_menu).pack(pady=20)

    # REVISI
    def cek_opsi(self, answer, pertanyaan):
        poin_lacak = {"easy": 10, "medium": 20, "hard": 30}
        poins = poin_lacak.get(pertanyaan.kesulitan, 10)
        
        if answer == pertanyaan.opsi_benar:
            level_maksimal_tercapai = self.user.update_skor(poins)
            
            if level_maksimal_tercapai:
                messagebox.showinfo("Selamat!", 
                    "Hore! Kamu sudah mencapai Level Maksimal, progress skor tidak akan berjalan lagi. " 
                    "Anda tetap bisa menggunakan aplikasi ini :D")
            else:
                messagebox.showinfo("Benar!", f"Jawaban kamu benar! +{poins} poin")
        else:
            messagebox.showinfo("Salah", 
                              f"Jawaban yang benar: {pertanyaan.opsi_benar}")
        self.show_menu()


    # REVISI
    def tampil_progress(self):
        self.clear_window()
        frame = self.create_frame()
        
        status_level = ("(Level Maksimal Tercapai!)" 
                        if self.user.level == self.user.LEVEL_MAKSIMAL 
                        else "")
        
        stats = f"""
        Username: {self.user.username}
        Level: {self.user.level} {status_level}
        Total Skor: {self.user.skor}
        """
        
        ttk.Label(frame, text="Statistik Pembelajaran", 
                 font=('Helvetica', 24, 'bold')).pack(pady=20)
        
        ttk.Label(frame, text=stats, font=('Helvetica', 14), 
                 justify='left').pack(pady=20)
        
        ttk.Button(frame, text="Kembali ke Menu", 
                  command=self.show_menu).pack(pady=20)

    def run(self):
        self.root.mainloop()

app = MainApp()
app.run()