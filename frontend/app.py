import os
import sys
import builtins
import io
import time
import tkinter as tk
from tkinter import ttk

# tambahkan root project dan folder backend ke sys.path supaya import aman dari mana saja
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if os.path.exists(os.path.join(ROOT_DIR, "data")):
    os.chdir(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "backend"))
sys.path.insert(0, BASE_DIR)

import m1_pesanan
import m2_antrean
import m3_laporan


class Aplikasi2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("750x550")

        # inisialisasi modul M1, M2, dan M3
        self.arr_m1 = m1_pesanan.Array()
        self.ll_m1 = m1_pesanan.LinkedList()
        self.sistem_m2 = m2_antrean.SistemAntrean()
        self.data_m3 = m3_laporan.csv_data()
        self.data_m3_oid_urut = None

        # buat tab untuk masing-masing file m1, m2, m3
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_m1 = ttk.Frame(self.notebook)
        self.tab_m2 = ttk.Frame(self.notebook)
        self.tab_m3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_m1, text="M1 - Pesanan")
        self.notebook.add(self.tab_m2, text="M2 - Antrean & Undo")
        self.notebook.add(self.tab_m3, text="M3 - Laporan (Sort & Search)")

        self.buat_ui_m1()
        self.buat_ui_m2()
        self.buat_ui_m3()

    def jalankan_fungsi_m1(self, fungsi, nilai_input):
        # tangkap input() dan print() bawaan dari m1_pesanan.py tanpa mengubah filenya
        input_asli = builtins.input
        stdout_asli = sys.stdout
        penampung = io.StringIO()

        builtins.input = lambda prompt="": str(nilai_input)
        sys.stdout = penampung
        try:
            hasil = fungsi()
            if hasil is not None:
                print(hasil)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            builtins.input = input_asli
            sys.stdout = stdout_asli

        return penampung.getvalue()

    def tulis_layar(self, widget_teks, pesan):
        widget_teks.delete("1.0", tk.END)
        widget_teks.insert(tk.END, pesan)

    # ================= TAB M1 =================
    def buat_ui_m1(self):
        frame_input = ttk.Frame(self.tab_m1)
        frame_input.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_input, text="Masukkan ID (6 digit angka, misal 000001):").pack(side="left")
        self.entry_id_m1 = ttk.Entry(frame_input, width=15)
        self.entry_id_m1.pack(side="left", padx=5)
        self.entry_id_m1.insert(0, "000001")

        frame_tombol = ttk.Frame(self.tab_m1)
        frame_tombol.pack(fill="x", padx=10, pady=5)

        # baris tombol Array
        f_arr = ttk.LabelFrame(frame_tombol, text="Array")
        f_arr.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Button(f_arr, text="melihat_pesanan", command=self.m1_arr_lihat).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_arr, text="menambah_pesanan", command=self.m1_arr_tambah).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_arr, text="menghapus_pesanan", command=self.m1_arr_hapus).pack(fill="x", padx=5, pady=2)

        # baris tombol LinkedList
        f_ll = ttk.LabelFrame(frame_tombol, text="LinkedList")
        f_ll.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Button(f_ll, text="melihat_pesanan", command=self.m1_ll_lihat).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_ll, text="menambah_pesanan", command=self.m1_ll_tambah).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_ll, text="menghapus_pesanan", command=self.m1_ll_hapus).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_ll, text="cetak_antrian", command=self.m1_ll_cetak).pack(fill="x", padx=5, pady=2)

        self.out_m1 = tk.Text(self.tab_m1, height=16)
        self.out_m1.pack(fill="both", expand=True, padx=10, pady=10)

    def m1_arr_lihat(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.arr_m1.melihat_pesanan, self.entry_id_m1.get())
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[Array.melihat_pesanan - {dt:.2f} ms]\n{out}")

    def m1_arr_tambah(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.arr_m1.menambah_pesanan, self.entry_id_m1.get())
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[Array.menambah_pesanan - {dt:.2f} ms]\n{out}")

    def m1_arr_hapus(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.arr_m1.menghapus_pesanan, self.entry_id_m1.get())
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[Array.menghapus_pesanan - {dt:.2f} ms]\n{out}")

    def m1_ll_lihat(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.ll_m1.melihat_pesanan, self.entry_id_m1.get())
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[LinkedList.melihat_pesanan - {dt:.2f} ms]\n{out}")

    def m1_ll_tambah(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.ll_m1.menambah_pesanan, self.entry_id_m1.get())
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[LinkedList.menambah_pesanan - {dt:.2f} ms]\n{out}")

    def m1_ll_hapus(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.ll_m1.menghapus_pesanan, self.entry_id_m1.get())
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[LinkedList.menghapus_pesanan - {dt:.2f} ms]\n{out}")

    def m1_ll_cetak(self):
        t0 = time.perf_counter()
        out = self.jalankan_fungsi_m1(self.ll_m1.cetak_antrian, "")
        dt = (time.perf_counter() - t0) * 1000
        self.tulis_layar(self.out_m1, f"[LinkedList.cetak_antrian - {dt:.2f} ms]\n{out}")

    # ================= TAB M2 =================
    def buat_ui_m2(self):
        # Bagian Kasir (Infix -> Postfix -> Hitung)
        f_kasir = ttk.LabelFrame(self.tab_m2, text="Mesin Kasir (Stack)")
        f_kasir.pack(fill="x", padx=10, pady=5)

        ttk.Label(f_kasir, text="Struk Infix:").pack(side="left", padx=5)
        self.entry_infix = ttk.Entry(f_kasir, width=30)
        self.entry_infix.pack(side="left", padx=5)
        self.entry_infix.insert(0, "(3 * 12000) + (2 * 8500) - 5000")
        ttk.Button(f_kasir, text="ke_postfix & hitung", command=self.m2_hitung_kasir).pack(side="left", padx=5, pady=5)

        # Bagian Antrean & Undo/Redo
        f_antrean = ttk.LabelFrame(self.tab_m2, text="Antrean (Queue) & Undo/Redo (Stack)")
        f_antrean.pack(fill="x", padx=10, pady=5)

        baris1 = ttk.Frame(f_antrean)
        baris1.pack(fill="x", padx=5, pady=3)
        ttk.Label(baris1, text="Nama Pelanggan:").pack(side="left")
        self.entry_pelanggan_m2 = ttk.Entry(baris1, width=18)
        self.entry_pelanggan_m2.pack(side="left", padx=5)
        self.entry_pelanggan_m2.insert(0, "Pelanggan Baru")
        ttk.Button(baris1, text="enqueue", command=self.m2_enqueue).pack(side="left", padx=3)

        baris2 = ttk.Frame(f_antrean)
        baris2.pack(fill="x", padx=5, pady=3)
        ttk.Label(baris2, text="Jumlah Dequeue:").pack(side="left")
        self.entry_jml_deq = ttk.Entry(baris2, width=8)
        self.entry_jml_deq.pack(side="left", padx=5)
        self.entry_jml_deq.insert(0, "1")
        ttk.Button(baris2, text="dequeue (Naif)", command=self.m2_deq_naif).pack(side="left", padx=3)
        ttk.Button(baris2, text="dequeue (Circular)", command=self.m2_deq_circular).pack(side="left", padx=3)
        ttk.Button(baris2, text="undo_last", command=self.m2_undo).pack(side="left", padx=3)
        ttk.Button(baris2, text="redo_last", command=self.m2_redo).pack(side="left", padx=3)

        self.out_m2 = tk.Text(self.tab_m2, height=16)
        self.out_m2.pack(fill="both", expand=True, padx=10, pady=10)

    def info_stats_m2(self):
        len_n, len_c, kap, geser, u_len, r_len = self.sistem_m2.stats()
        return f"Panjang antrean -> Naif: {len_n} | Circular: {len_c} (Kapasitas: {kap})\nTotal geseran Naif: {geser} | Undo tersisa: {u_len} | Redo tersisa: {r_len}"

    def m2_hitung_kasir(self):
        ekspresi = self.entry_infix.get()
        t0 = time.perf_counter()
        pf = m2_antrean.ke_postfix(ekspresi)
        total = m2_antrean.hitung(pf)
        dt = (time.perf_counter() - t0) * 1000
        teks = f"[Stack Kasir - {dt:.2f} ms]\nInfix   : {ekspresi}\nPostfix : {pf}\nTOTAL   : Rp {total:,}"
        self.tulis_layar(self.out_m2, teks)

    def m2_enqueue(self):
        nama = self.entry_pelanggan_m2.get()
        t0 = time.perf_counter()
        pesanan = self.sistem_m2.enqueue(nama)
        dt = (time.perf_counter() - t0) * 1000
        teks = f"[enqueue - {dt:.2f} ms]\nPesanan {pesanan[0]} ({pesanan[1]}) masuk ke belakang KEDUA antrean.\n\n{self.info_stats_m2()}"
        self.tulis_layar(self.out_m2, teks)

    def m2_deq_naif(self):
        jml = int(self.entry_jml_deq.get() or 1)
        t0 = time.perf_counter()
        keluar, geseran = self.sistem_m2.dequeue_naif(jml)
        dt = (time.perf_counter() - t0) * 1000
        daftar_oid = [x[0] for x in keluar[:10]]
        teks = (f"[dequeue_naif ({jml}) - {dt:.2f} ms]\n"
                f"{len(keluar)} pesanan keluar dari depan antrean naif.\n"
                f"Elemen digeser pada aksi ini: {geseran}\n"
                f"Contoh yang keluar: {daftar_oid}\n\n{self.info_stats_m2()}")
        self.tulis_layar(self.out_m2, teks)

    def m2_deq_circular(self):
        jml = int(self.entry_jml_deq.get() or 1)
        t0 = time.perf_counter()
        keluar = self.sistem_m2.dequeue_circular(jml)
        dt = (time.perf_counter() - t0) * 1000
        daftar_oid = [x[0] for x in keluar[:10]]
        teks = (f"[dequeue_circular ({jml}) - {dt:.2f} ms]\n"
                f"{len(keluar)} pesanan keluar dari depan antrean circular.\n"
                f"Tidak ada elemen yang digeser (front={self.sistem_m2.circular.front}, rear={self.sistem_m2.circular.rear}).\n"
                f"Contoh yang keluar: {daftar_oid}\n\n{self.info_stats_m2()}")
        self.tulis_layar(self.out_m2, teks)

    def m2_undo(self):
        t0 = time.perf_counter()
        hasil = self.sistem_m2.undo_last()
        dt = (time.perf_counter() - t0) * 1000
        if hasil is None:
            teks = "Tumpukan undo kosong, tidak ada aksi yang dibatalkan."
        else:
            aksi, data = hasil
            teks = f"[undo_last - {dt:.2f} ms]\nMembatalkan aksi: {aksi}\n\n{self.info_stats_m2()}"
        self.tulis_layar(self.out_m2, teks)

    def m2_redo(self):
        t0 = time.perf_counter()
        hasil = self.sistem_m2.redo_last()
        dt = (time.perf_counter() - t0) * 1000
        if hasil is None:
            teks = "Tumpukan redo kosong, tidak ada aksi yang diulang."
        else:
            aksi, data = hasil
            teks = f"[redo_last - {dt:.2f} ms]\nMengerjakan ulang aksi: {aksi}\n\n{self.info_stats_m2()}"
        self.tulis_layar(self.out_m2, teks)

    # ================= TAB M3 =================
    def buat_ui_m3(self):
        # Bagian Sort
        f_sort = ttk.LabelFrame(self.tab_m3, text="Pengurutan (Sort)")
        f_sort.pack(fill="x", padx=10, pady=5)

        ttk.Label(f_sort, text="Jumlah baris:").pack(side="left", padx=5)
        self.entry_jml_m3 = ttk.Entry(f_sort, width=10)
        self.entry_jml_m3.pack(side="left", padx=5)
        self.entry_jml_m3.insert(0, "1000")

        ttk.Label(f_sort, text="Kunci:").pack(side="left", padx=5)
        self.combo_kunci_m3 = ttk.Combobox(f_sort, values=["oid", "harga", "selesai"], width=10, state="readonly")
        self.combo_kunci_m3.pack(side="left", padx=5)
        self.combo_kunci_m3.set("harga")

        ttk.Button(f_sort, text="insertion_sort", command=self.m3_insertion).pack(side="left", padx=5, pady=5)
        ttk.Button(f_sort, text="merge_sort", command=self.m3_merge).pack(side="left", padx=5, pady=5)

        # Bagian Search
        f_search = ttk.LabelFrame(self.tab_m3, text="Pencarian (Search)")
        f_search.pack(fill="x", padx=10, pady=5)

        ttk.Label(f_search, text="Target OID:").pack(side="left", padx=5)
        self.entry_oid_m3 = ttk.Entry(f_search, width=15)
        self.entry_oid_m3.pack(side="left", padx=5)
        self.entry_oid_m3.insert(0, "O-000010")

        ttk.Button(f_search, text="linear_search", command=self.m3_linear).pack(side="left", padx=5, pady=5)
        ttk.Button(f_search, text="binary_search", command=self.m3_binary).pack(side="left", padx=5, pady=5)

        self.out_m3 = tk.Text(self.tab_m3, height=16)
        self.out_m3.pack(fill="both", expand=True, padx=10, pady=10)

    def m3_insertion(self):
        n = int(self.entry_jml_m3.get() or 10)
        kunci = self.combo_kunci_m3.get()
        potongan = self.data_m3[:n]

        t0 = time.perf_counter()
        terurut, banding, pindah = m3_laporan.insertion_sort(potongan, kunci)
        dt = (time.perf_counter() - t0) * 1000

        if terurut is None:
            self.tulis_layar(self.out_m3, "DITOLAK: batas insertion_sort adalah 20.000 baris. Gunakan merge_sort untuk data penuh.")
            return

        contoh = "\n".join([f"{i+1}. {r[0]} | {r[1]} | Rp{r[4]} | selesai: {r[7] or '-'}" for i, r in enumerate(terurut[:10])])
        teks = (f"[insertion_sort - {dt:.2f} ms]\n"
                f"{len(terurut)} pesanan diurutkan menurut '{kunci}'.\n"
                f"{banding:,} perbandingan, {pindah:,} pemindahan.\n\n"
                f"10 Baris Pertama:\n{contoh}")
        self.tulis_layar(self.out_m3, teks)

    def m3_merge(self):
        n = int(self.entry_jml_m3.get() or 10)
        kunci = self.combo_kunci_m3.get()
        potongan = self.data_m3[:n]

        t0 = time.perf_counter()
        terurut, banding, pindah = m3_laporan.merge_sort(potongan, kunci)
        dt = (time.perf_counter() - t0) * 1000

        contoh = "\n".join([f"{i+1}. {r[0]} | {r[1]} | Rp{r[4]} | selesai: {r[7] or '-'}" for i, r in enumerate(terurut[:10])])
        teks = (f"[merge_sort - {dt:.2f} ms]\n"
                f"{len(terurut)} pesanan diurutkan menurut '{kunci}'.\n"
                f"{banding:,} perbandingan, {pindah:,} pemindahan.\n\n"
                f"10 Baris Pertama:\n{contoh}")
        self.tulis_layar(self.out_m3, teks)

    def m3_linear(self):
        target = self.entry_oid_m3.get().strip()
        t0 = time.perf_counter()
        idx, baris, banding = m3_laporan.linear_search(self.data_m3, target)
        dt = (time.perf_counter() - t0) * 1000

        if idx == -1:
            teks = f"[linear_search - {dt:.2f} ms]\nOID {target} tidak ditemukan.\n{banding:,} perbandingan."
        else:
            teks = (f"[linear_search - {dt:.2f} ms]\n"
                    f"Ditemukan pada indeks {idx} ({banding:,} perbandingan).\n\n"
                    f"Detail Pesanan:\n{baris}")
        self.tulis_layar(self.out_m3, teks)

    def m3_binary(self):
        target = self.entry_oid_m3.get().strip()
        info_urut = ""
        if self.data_m3_oid_urut is None:
            t_urut = time.perf_counter()
            self.data_m3_oid_urut, _, _ = m3_laporan.merge_sort(self.data_m3, "oid")
            dt_urut = (time.perf_counter() - t_urut) * 1000
            info_urut = f"Daftar terurut oid dibangun sekali dengan merge_sort ({dt_urut:.2f} ms).\n"

        t0 = time.perf_counter()
        idx, baris, banding = m3_laporan.binary_search(self.data_m3_oid_urut, target)
        dt = (time.perf_counter() - t0) * 1000

        if idx == -1:
            teks = f"[binary_search - {dt:.2f} ms]\n{info_urut}OID {target} tidak ditemukan.\n{banding:,} perbandingan."
        else:
            teks = (f"[binary_search - {dt:.2f} ms]\n"
                    f"{info_urut}Ditemukan pada indeks {idx} ({banding:,} perbandingan).\n\n"
                    f"Detail Pesanan:\n{baris}")
        self.tulis_layar(self.out_m3, teks)


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikasi2EZ4U(root)
    root.mainloop()