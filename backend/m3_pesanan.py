import csv
import os
import time

# Indeks Kolom Data Pesanan
IDX_OID = 0
IDX_PELANGGAN = 1
IDX_RESTO = 2
IDX_MENU = 3
IDX_HARGA = 4
IDX_PRIORITAS = 5
IDX_MASUK = 6
IDX_SELESAI = 7
IDX_STATUS = 8

BATAS_INSERTION_SORT = 20000

 # Agar pesanan belum selesai diletakkan di akhir saat diurutkan
NILAI_KOSONG_SELESAI = 999999999

def format_waktu(detik):
    if detik is None or detik == "" or detik < 0 or detik >= NILAI_KOSONG_SELESAI:
        return "-"
    jam = int(detik) // 3600
    sisa = int(detik) % 3600
    menit = sisa // 60
    dtk = sisa % 60
    return f"{jam:02d}:{menit:02d}:{dtk:02d}"


def cari_path_csv(default_path="data/pesanan.csv"):
    if os.path.exists(default_path):
        return default_path
    if os.path.exists("pesanan.csv"):
        return "pesanan.csv"
    return default_path


def ambil_kunci(baris, kunci):
    """Mengambil nilai kolom yang menjadi kunci pengurutan."""
    if kunci == "oid":
        return baris[IDX_OID]
    elif kunci == "harga":
        return baris[IDX_HARGA]
    elif kunci == "selesai":
        return baris[IDX_SELESAI]
    return baris[IDX_OID]


# ==========================================
# 1. ALGORITMA PENGURUTAN (SORTING)
# ==========================================
def insertion_sort(larik, kunci="harga"):
    n = len(larik)
    if n > BATAS_INSERTION_SORT:
        raise ValueError(f"DITOLAK: batasnya {BATAS_INSERTION_SORT:,} baris, pakai merge sort untuk data penuh")

    # Salin larik agar data asli tidak rusak saat diadu dengan merge sort
    A = [baris for baris in larik]
    perbandingan = 0
    pemindahan = 0

    for i in range(1, n):
        elemen_sekarang = A[i]
        nilai_sekarang = ambil_kunci(elemen_sekarang, kunci)
        j = i - 1

        while j >= 0:
            perbandingan += 1
            if ambil_kunci(A[j], kunci) > nilai_sekarang:
                A[j + 1] = A[j]
                pemindahan += 1
                j -= 1
            else:
                break

        A[j + 1] = elemen_sekarang
        pemindahan += 1

    return A, perbandingan, pemindahan


def merge_sort(larik, kunci="oid"):
    pencacah = [0, 0]  

    def _urutkan(arr):
        n = len(arr)
        if n <= 1:
            return arr
        mid = n // 2
        kiri = _urutkan(arr[:mid])
        kanan = _urutkan(arr[mid:])
        return _gabung(kiri, kanan)

    def _gabung(kiri, kanan):
        hasil = []
        i = 0
        j = 0
        len_kiri = len(kiri)
        len_kanan = len(kanan)

        while i < len_kiri and j < len_kanan:
            pencacah[0] += 1
            if ambil_kunci(kiri[i], kunci) <= ambil_kunci(kanan[j], kunci):
                hasil.append(kiri[i])
                pencacah[1] += 1
                i += 1
            else:
                hasil.append(kanan[j])
                pencacah[1] += 1
                j += 1

        # Salin sisa elemen kiri atau kanan
        while i < len_kiri:
            hasil.append(kiri[i])
            pencacah[1] += 1
            i += 1

        while j < len_kanan:
            hasil.append(kanan[j])
            pencacah[1] += 1
            j += 1

        return hasil

    terurut = _urutkan(larik)
    return terurut, pencacah[0], pencacah[1]

# Search Algorithm
def linear_search(larik, target_oid):
    perbandingan = 0
    for i in range(len(larik)):
        perbandingan += 1
        if larik[i][IDX_OID] == target_oid:
            return i, larik[i], perbandingan
    return -1, None, perbandingan


def binary_search(larik_terurut, target_oid):
    lo = 0
    hi = len(larik_terurut) - 1
    perbandingan = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        perbandingan += 1
        oid_tengah = larik_terurut[mid][IDX_OID]

        if oid_tengah == target_oid:
            return mid, larik_terurut[mid], perbandingan
        elif oid_tengah < target_oid:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, None, perbandingan


class BackendM3:
    def __init__(self, path_csv="data/pesanan.csv"):
        self.path_csv = cari_path_csv(path_csv)
        self.semua_data = []
        self.daftar_terurut_oid = None
        self.waktu_bangun_oid_ms = 0.0
        self.muat_semua_data()

    def muat_semua_data(self):
        with open(self.path_csv, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Lewati header
            for row in reader:
                self.semua_data.append([
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    int(row[4]),
                    int(row[5]),
                    int(row[6]),
                    int(row[7]) if row[7] != '' else NILAI_KOSONG_SELESAI,
                    row[8]
                ])

    def jalankan_insertion_sort(self, jumlah_baris=10, kunci="harga"):
        potongan = self.semua_data[:jumlah_baris]
        t0 = time.perf_counter()
        hasil, comp, move = insertion_sort(potongan, kunci)
        ms = (time.perf_counter() - t0) * 1000
        return hasil, comp, move, ms

    def jalankan_merge_sort(self, jumlah_baris=4000, kunci="oid"):
        potongan = self.semua_data[:jumlah_baris]
        t0 = time.perf_counter()
        hasil, comp, move = merge_sort(potongan, kunci)
        ms = (time.perf_counter() - t0) * 1000
        return hasil, comp, move, ms

    def jalankan_linear_search(self, target_oid):
        if not target_oid.startswith("O-"):
            target_oid = "O-" + target_oid
        t0 = time.perf_counter()
        idx, ditemukan, comp = linear_search(self.semua_data, target_oid)
        ms = (time.perf_counter() - t0) * 1000
        return idx, ditemukan, comp, ms

    def jalankan_binary_search(self, target_oid):
        if not target_oid.startswith("O-"):
            target_oid = "O-" + target_oid

        # Bangun daftar terurut oid sekali saja dengan merge sort bila belum ada
        if self.daftar_terurut_oid is None:
            t_build = time.perf_counter()
            self.daftar_terurut_oid, _, _ = merge_sort(self.semua_data, "oid")
            self.waktu_bangun_oid_ms = (time.perf_counter() - t_build) * 1000

        t0 = time.perf_counter()
        idx, ditemukan, comp = binary_search(self.daftar_terurut_oid, target_oid)
        ms = (time.perf_counter() - t0) * 1000
        return idx, ditemukan, comp, ms, self.waktu_bangun_oid_ms


def cetak_tabel_pesanan(daftar, batas_tampil=10):
    print(f"{'#':<4} | {'oid':<9} | {'harga':<8} | {'selesai':<9} | {'resto':<15} | {'menu'}")
    print("-" * 68)
    for i in range(min(len(daftar), batas_tampil)):
        p = daftar[i]
        harga_str = f"{p[IDX_HARGA]:,}".replace(",", ".")
        selesai_str = format_waktu(p[IDX_SELESAI])
        print(f"{i+1:<4} | {p[IDX_OID]:<9} | {harga_str:<8} | {selesai_str:<9} | {p[IDX_RESTO]:<15} | {p[IDX_MENU]}")


def cetak_detail_pesanan(p):
    if p is None:
        print("Pesanan tidak ditemukan.")
        return
    harga_str = f"{p[IDX_HARGA]:,}".replace(",", ".")
    print(f"  oid       : {p[IDX_OID]}")
    print(f"  pelanggan : {p[IDX_PELANGGAN]}")
    print(f"  resto     : {p[IDX_RESTO]}")
    print(f"  menu      : {p[IDX_MENU]}")
    print(f"  harga     : {harga_str}")
    print(f"  prioritas : {p[IDX_PRIORITAS]}")
    print(f"  masuk     : {format_waktu(p[IDX_MASUK])}")
    print(f"  selesai   : {format_waktu(p[IDX_SELESAI])}")
    print(f"  status    : {p[IDX_STATUS]}")


def start():
    print("Memuat 200.000 baris pesanan.csv...")
    m3 = BackendM3()
    print(f"Siap! {len(m3.semua_data):,} baris berhasil dimuat.\n")

    menu_opsi = (
        "Sort - Insertion Sort O(n^2)",
        "Sort - Merge Sort O(n log n)",
        "Search - Linear Search O(n)",
        "Search - Binary Search O(log n)",
        "Exit"
    )

    while True:
        print("\n=== MENU BACKEND M3 (SORT & SEARCH) ===")
        for i in range(len(menu_opsi)):
            print(f"{i + 1}. {menu_opsi[i]}")

        pilih = input(f"Pilih menu (1-{len(menu_opsi)}): ").strip()
        if not pilih.isdigit():
            continue
        opsi = int(pilih)

        if opsi == 1:
            jml = int(input("Jumlah baris diurutkan (misal 10, 1000, 2000, 4000): ") or "10")
            kunci = input("Diurutkan menurut (oid / harga / selesai) [default: harga]: ").strip().lower() or "harga"
            try:
                hasil, comp, move, ms = m3.jalankan_insertion_sort(jml, kunci)
                print(f"\n{len(hasil):,} pesanan diurutkan menurut {kunci}.")
                print(f"{comp:,} perbandingan, {move:,} pemindahan | Waktu: {ms:.2f} ms\n")
                cetak_tabel_pesanan(hasil, 10)
            except ValueError as e:
                print(f"\n{e}")

        elif opsi == 2:
            jml = int(input("Jumlah baris diurutkan (misal 4000 atau 200000): ") or "4000")
            kunci = input("Diurutkan menurut (oid / harga / selesai) [default: oid]: ").strip().lower() or "oid"
            hasil, comp, move, ms = m3.jalankan_merge_sort(jml, kunci)
            print(f"\n{len(hasil):,} pesanan diurutkan menurut {kunci}.")
            print(f"{comp:,} perbandingan, {move:,} pemindahan | Waktu: {ms:.2f} ms\n")
            cetak_tabel_pesanan(hasil, 10)

        elif opsi == 3:
            target = input("Nomor pesanan (oid), misal O-137442 atau 137442: ").strip() or "O-137442"
            idx, item, comp, ms = m3.jalankan_linear_search(target)
            if idx != -1:
                print(f"\nDitemukan pada indeks {idx:,}. {comp:,} perbandingan | Waktu: {ms:.2f} ms")
                cetak_detail_pesanan(item)
            else:
                print(f"\nTidak ditemukan setelah {comp:,} perbandingan | Waktu: {ms:.2f} ms")

        elif opsi == 4:
            target = input("Nomor pesanan (oid), misal O-137442 atau 137442: ").strip() or "O-137442"
            idx, item, comp, ms, build_ms = m3.jalankan_binary_search(target)
            print(f"\nDaftar terurut oid dibangun sekali dengan merge sort, {build_ms:.2f} ms.")
            if idx != -1:
                print(f"Ditemukan pada baris ke-{idx + 1:,} dari {len(m3.semua_data):,} baris.")
                print(f"{comp:,} perbandingan, bandingkan dengan linear search | Waktu: {ms:.3f} ms")
                cetak_detail_pesanan(item)
            else:
                print(f"Tidak ditemukan setelah {comp:,} perbandingan | Waktu: {ms:.3f} ms")

        elif opsi == len(menu_opsi):
            break


if __name__ == "__main__":
    start()