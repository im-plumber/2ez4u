import csv
import os
import time

# Indeks Kolom Data Pesanan (Pengganti dict agar patuh aturan proyek)
IDX_OID = 0
IDX_PELANGGAN = 1
IDX_RESTO = 2
IDX_MENU = 3
IDX_HARGA = 4
IDX_PRIORITAS = 5
IDX_MASUK = 6
IDX_SELESAI = 7
IDX_STATUS = 8


def format_waktu(detik):
    if detik is None or detik == "" or detik < 0:
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


# stack
class Tumpukan:
    def __init__(self, kapasitas_awal=16):
        self.kapasitas = kapasitas_awal
        self.data = [None] * self.kapasitas
        self.ukuran = 0

    def _perbesar(self):
        kapasitas_baru = self.kapasitas * 2
        data_baru = [None] * kapasitas_baru
        for i in range(self.ukuran):
            data_baru[i] = self.data[i]
        self.data = data_baru
        self.kapasitas = kapasitas_baru

    def push(self, x):
        if self.ukuran == self.kapasitas:
            self._perbesar()
        self.data[self.ukuran] = x
        self.ukuran += 1

    def pop(self):
        if self.kosong():
            return None
        self.ukuran -= 1
        item = self.data[self.ukuran]
        self.data[self.ukuran] = None
        return item

    def peek(self):
        if self.kosong():
            return None
        return self.data[self.ukuran - 1]

    def kosong(self):
        return self.ukuran == 0

    def clear(self):
        self.data = [None] * self.kapasitas
        self.ukuran = 0

    def ke_list(self):
        hasil = []
        for i in range(self.ukuran):
            hasil.append(self.data[i])
        return hasil


# ==========================================
# 2. MESIN KASIR: INFIX KE POSTFIX & EVALUASI
# ==========================================
def pecah_token(ekspresi):
    """Memecah string ekspresi matematika menjadi token angka dan operator."""
    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        ch = ekspresi[i]
        if ch == ' ' or ch == '\t':
            i += 1
            continue
        elif ch in ('+', '-', '*', '/', '(', ')'):
            tokens.append(ch)
            i += 1
        elif '0' <= ch <= '9':
            angka = ""
            while i < n and ('0' <= ekspresi[i] <= '9'):
                angka += ekspresi[i]
                i += 1
            tokens.append(angka)
        else:
            raise ValueError(f"Karakter tidak dikenal pada struk: '{ch}'")
    return tokens


def tingkat_operator(op):
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0


def ke_postfix(ekspresi):
    """Mengubah ekspresi infix menjadi list token postfix memakai Tumpukan."""
    tokens = pecah_token(ekspresi)
    stack = Tumpukan()
    keluaran = []
    langkah_konversi = []
    no = 1

    for token in tokens:
        if '0' <= token[0] <= '9':
            keluaran.append(token)
            tindakan = "operand, langsung ke output"
        elif token == '(':
            stack.push(token)
            tindakan = "push ( ke stack"
        elif token == ')':
            while not stack.kosong() and stack.peek() != '(':
                keluaran.append(stack.pop())
            if not stack.kosong() and stack.peek() == '(':
                stack.pop()
            tindakan = "pop sampai (, lalu buang ("
        else:
            terpop = []
            while (not stack.kosong() and stack.peek() != '(' and
                   tingkat_operator(stack.peek()) >= tingkat_operator(token)):
                terpop.append(stack.pop())
                keluaran.append(terpop[-1])
            stack.push(token)
            if len(terpop) > 0:
                tindakan = f"pop {' '.join(terpop)}, lalu push {token}"
            else:
                tindakan = f"push {token}"

        isi_stack = " ".join(stack.ke_list()) if not stack.kosong() else "kosong"
        isi_out = " ".join(keluaran)
        langkah_konversi.append((f"1.{no}", token, tindakan, isi_stack, isi_out))
        no += 1

    sisa = []
    while not stack.kosong():
        op = stack.pop()
        sisa.append(op)
        keluaran.append(op)

    tindakan_akhir = f"pop sisa stack: {' '.join(sisa)}" if sisa else "pop sisa stack"
    langkah_konversi.append(("1.akhir", "", tindakan_akhir, "kosong", " ".join(keluaran)))

    return keluaran, langkah_konversi


def hitung(postfix):
    """Mengevaluasi token postfix memakai Tumpukan angka."""
    if isinstance(postfix, str):
        tokens = postfix.split()
    else:
        tokens = postfix

    stack = Tumpukan()
    langkah_evaluasi = []
    no = 1

    for token in tokens:
        if '0' <= token[0] <= '9':
            nilai = int(token)
            stack.push(nilai)
            tindakan = f"operand, push {nilai}"
            hasil_str = str(nilai)
        else:
            # Penting: Pop pertama adalah operand KANAN (b), kedua adalah KIRI (a)
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '/':
                res = a // b if a % b == 0 else a / b
            else:
                raise ValueError(f"Operator tidak valid: {token}")

            stack.push(res)
            tindakan = f"pop {b} dan {a} -> {a} {token} {b} = {res}"
            hasil_str = str(res)

        isi_stack = " ".join([str(x) for x in stack.ke_list()]) if not stack.kosong() else "kosong"
        langkah_evaluasi.append((f"2.{no}", token, tindakan, isi_stack, hasil_str))
        no += 1

    total = stack.pop() if not stack.kosong() else 0
    return total, langkah_evaluasi


# ==========================================
# 3. STRUKTUR DATA QUEUE NAIF VS MELINGKAR
# ==========================================
class AntreanNaif:
    """Queue di atas larik biasa: dequeue mengambil indeks 0 dan menggeser seluruh sisa elemen."""
    def __init__(self):
        self.data = []
        self.total_geseran = 0

    def enqueue(self, x):
        self.data.append(x)

    def dequeue(self):
        if self.is_empty():
            return None, 0
        item = self.data[0]
        geseran = len(self.data) - 1
        # Geser manual satu per satu ke kiri (O(n))
        for i in range(geseran):
            self.data[i] = self.data[i + 1]
        self.data.pop()
        self.total_geseran += geseran
        return item, geseran

    def pop_belakang(self):
        """Digunakan saat membatalkan (undo) enqueue."""
        if self.is_empty():
            return None
        return self.data.pop()

    def kembalikan_ke_depan(self, daftar_pesanan):
        """Digunakan saat membatalkan (undo) dequeue: dikembalikan ke DEPAN antrean."""
        data_baru = []
        for x in daftar_pesanan:
            data_baru.append(x)
        for x in self.data:
            data_baru.append(x)
        self.data = data_baru

    def is_empty(self):
        return len(self.data) == 0

    def ukuran(self):
        return len(self.data)


class AntreanMelingkar:
    """Circular Queue: dequeue hanya memajukan penunjuk front dengan operasi modulo O(1)."""
    def __init__(self, kapasitas=32768):
        self.kapasitas = kapasitas
        self.data = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0

    def _perbesar(self):
        kap_baru = self.kapasitas * 2
        data_baru = [None] * kap_baru
        for i in range(self.count):
            data_baru[i] = self.data[(self.front + i) % self.kapasitas]
        self.data = data_baru
        self.front = 0
        self.rear = self.count
        self.kapasitas = kap_baru

    def enqueue(self, x):
        if self.count == self.kapasitas:
            self._perbesar()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.kapasitas
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self.count -= 1
        return x

    def pop_belakang(self):
        """Digunakan saat membatalkan (undo) enqueue."""
        if self.is_empty():
            return None
        self.rear = (self.rear - 1 + self.kapasitas) % self.kapasitas
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x

    def kembalikan_ke_depan(self, daftar_pesanan):
        """Mengembalikan daftar pesanan ke DEPAN antrean melingkar secara terbalik agar urutan tetap utuh."""
        while self.count + len(daftar_pesanan) > self.kapasitas:
            self._perbesar()
        for i in range(len(daftar_pesanan) - 1, -1, -1):
            self.front = (self.front - 1 + self.kapasitas) % self.kapasitas
            self.data[self.front] = daftar_pesanan[i]
            self.count += 1

    def is_empty(self):
        return self.count == 0

    def ukuran(self):
        return self.count


# ==========================================
# 4. ENGINE BACKEND M2 & CLI INTERAKTIF
# ==========================================
class BackendM2:
    def __init__(self, path_csv="data/pesanan.csv"):
        self.path_csv = cari_path_csv(path_csv)
        self.naif = AntreanNaif()
        self.circular = AntreanMelingkar(32768)
        self.undo_stack = Tumpukan()
        self.redo_stack = Tumpukan()
        self.id_terakhir = 200000
        self.muat_data_antre()

    def muat_data_antre(self):
        """Memuat seluruh pesanan berstatus ANTRE ke dalam kedua antrean sekaligus."""
        with open(self.path_csv, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Lewati header
            for row in reader:
                if row[IDX_STATUS] == 'ANTRE':
                    pesanan = [
                        row[0], row[1], row[2], row[3],
                        int(row[4]), int(row[5]), int(row[6]),
                        int(row[7]) if row[7] != '' else -1,
                        row[8]
                    ]
                    self.naif.enqueue(pesanan)
                    self.circular.enqueue(pesanan)

    def kasir_postfix(self, ekspresi):
        t0 = time.perf_counter()
        postfix_tokens, langkah_1 = ke_postfix(ekspresi)
        total, langkah_2 = hitung(postfix_tokens)
        durasi_ms = (time.perf_counter() - t0) * 1000
        return " ".join(postfix_tokens), total, langkah_1 + langkah_2, durasi_ms

    def enqueue_pesanan_baru(self, pelanggan, resto="kafe-teknik", menu="roti-bakar", harga=12000, prioritas=2):
        t0 = time.perf_counter()
        self.id_terakhir += 1
        oid_baru = f"O-{self.id_terakhir:06d}"
        pesanan = [oid_baru, pelanggan, resto, menu, int(harga), int(prioritas), 28800, -1, "ANTRE"]

        self.naif.enqueue(pesanan)
        self.circular.enqueue(pesanan)

        # Catat ke undo & kosongkan redo sesuai spesifikasi
        self.undo_stack.push(("ENQUEUE", pesanan))
        self.redo_stack.clear()

        durasi_ms = (time.perf_counter() - t0) * 1000
        return pesanan, durasi_ms

    def dequeue_naif(self, jumlah=1):
        t0 = time.perf_counter()
        keluar = []
        geseran_aksi = 0
        for _ in range(jumlah):
            if self.naif.is_empty():
                break
            item, g = self.naif.dequeue()
            keluar.append(item)
            geseran_aksi += g

        if keluar:
            self.undo_stack.push(("DEQUEUE_NAIF", keluar))
            self.redo_stack.clear()

        durasi_ms = (time.perf_counter() - t0) * 1000
        return keluar, geseran_aksi, durasi_ms

    def dequeue_circular(self, jumlah=1):
        t0 = time.perf_counter()
        keluar = []
        for _ in range(jumlah):
            if self.circular.is_empty():
                break
            keluar.append(self.circular.dequeue())

        if keluar:
            self.undo_stack.push(("DEQUEUE_CIRCULAR", keluar))
            self.redo_stack.clear()

        durasi_ms = (time.perf_counter() - t0) * 1000
        return keluar, durasi_ms

    def dequeue_keduanya(self, jumlah=1):
        """Melayani kedua antrean sekaligus agar jumlah isi tetap sinkron saat diadu."""
        t0 = time.perf_counter()
        keluar_naif = []
        geseran_aksi = 0
        for _ in range(jumlah):
            if self.naif.is_empty():
                break
            item, g = self.naif.dequeue()
            keluar_naif.append(item)
            geseran_aksi += g
        waktu_naif = (time.perf_counter() - t0) * 1000

        t1 = time.perf_counter()
        keluar_circ = []
        for _ in range(jumlah):
            if self.circular.is_empty():
                break
            keluar_circ.append(self.circular.dequeue())
        waktu_circ = (time.perf_counter() - t1) * 1000

        if keluar_circ:
            self.undo_stack.push(("DEQUEUE_BOTH", keluar_circ))
            self.redo_stack.clear()

        return keluar_circ, geseran_aksi, waktu_naif, waktu_circ

    def undo_last(self):
        t0 = time.perf_counter()
        if self.undo_stack.kosong():
            return None, "Tumpukan undo kosong, tidak ada aksi yang bisa dibatalkan.", 0.0

        aksi, payload = self.undo_stack.pop()
        if aksi == "ENQUEUE":
            self.naif.pop_belakang()
            self.circular.pop_belakang()
            pesan = f"Pembatalan enqueue: {payload[IDX_OID]} dikeluarkan lagi dari belakang."
        elif aksi == "DEQUEUE_NAIF":
            self.naif.kembalikan_ke_depan(payload)
            pesan = f"{len(payload)} pesanan dikembalikan ke DEPAN antrean naif."
        elif aksi == "DEQUEUE_CIRCULAR":
            self.circular.kembalikan_ke_depan(payload)
            pesan = f"{len(payload)} pesanan dikembalikan ke DEPAN antrean circular."
        elif aksi == "DEQUEUE_BOTH":
            self.naif.kembalikan_ke_depan(payload)
            self.circular.kembalikan_ke_depan(payload)
            pesan = f"{len(payload)} pesanan dikembalikan ke DEPAN kedua antrean."

        self.redo_stack.push((aksi, payload))
        durasi_ms = (time.perf_counter() - t0) * 1000
        return (aksi, payload), pesan, durasi_ms

    def redo_last(self):
        t0 = time.perf_counter()
        if self.redo_stack.kosong():
            return None, "Tumpukan redo kosong, tidak ada yang diulang.", 0.0

        aksi, payload = self.redo_stack.pop()
        if aksi == "ENQUEUE":
            self.naif.enqueue(payload)
            self.circular.enqueue(payload)
            pesan = f"Enqueue dikerjakan lagi: {payload[IDX_OID]} masuk kembali ke belakang."
        elif aksi == "DEQUEUE_NAIF":
            for _ in range(len(payload)):
                self.naif.dequeue()
            pesan = f"{len(payload)} pesanan keluar lagi dari antrean naif."
        elif aksi == "DEQUEUE_CIRCULAR":
            for _ in range(len(payload)):
                self.circular.dequeue()
            pesan = f"{len(payload)} pesanan keluar lagi dari antrean circular."
        elif aksi == "DEQUEUE_BOTH":
            for _ in range(len(payload)):
                self.naif.dequeue()
                self.circular.dequeue()
            pesan = f"{len(payload)} pesanan keluar lagi dari kedua antrean."

        self.undo_stack.push((aksi, payload))
        durasi_ms = (time.perf_counter() - t0) * 1000
        return (aksi, payload), pesan, durasi_ms

    def stats(self):
        """Mengembalikan statistik antrean dan stack sesuai Langkah Kerja #9 M2."""
        return (
            ("queue_len_naif", self.naif.ukuran()),
            ("queue_len_circular", self.circular.ukuran()),
            ("queue_capacity", self.circular.kapasitas),
            ("total_geseran", self.naif.total_geseran),
            ("undo_depth", self.undo_stack.ukuran),
            ("redo_depth", self.redo_stack.ukuran),
        )


def start():
    print("Memuat pesanan berstatus ANTRE dari pesanan.csv...")
    m2 = BackendM2()
    print(f"Siap! {m2.naif.ukuran()} pesanan ANTRE masuk ke KEDUA antrean.\n")

    menu_opsi = (
        "Stack - Postfix (Mesin Kasir)",
        "Queue - Enqueue Pesanan Baru",
        "Queue - Dequeue Naif",
        "Queue - Dequeue Circular",
        "Stack - Undo Aksi Terakhir",
        "Stack - Redo Aksi Terakhir",
        "Lihat Statistik (stats)",
        "Exit"
    )

    while True:
        print("\n=== MENU BACKEND M2 (STACK & QUEUE) ===")
        for i in range(len(menu_opsi)):
            print(f"{i + 1}. {menu_opsi[i]}")

        pilih = input(f"Pilih menu (1-{len(menu_opsi)}): ").strip()
        if not pilih.isdigit():
            continue
        opsi = int(pilih)

        if opsi == 1:
            ekspresi = input("Masukkan struk belanja (infix), misal (3 * 12000) + (2 * 8500) - 5000 : ").strip()
            if not ekspresi:
                ekspresi = "(3 * 12000) + (2 * 8500) - 5000"
            postfix_str, total, langkah, ms = m2.kasir_postfix(ekspresi)
            print(f"\nStruk   : {ekspresi}")
            print(f"Postfix : {postfix_str}")
            print(f"TOTAL   : Rp {total:,}".replace(",", "."))
            print(f"Waktu   : {ms:.2f} ms\n")
            print(f"{'Langkah':<8} | {'Token':<7} | {'Tindakan':<32} | {'Stack':<18} | {'Output'}")
            print("-" * 95)
            for l in langkah:
                print(f"{l[0]:<8} | {l[1]:<7} | {l[2]:<32} | {l[3]:<18} | {l[4]}")

        elif opsi == 2:
            nama = input("Nama pelanggan baru: ").strip() or "Pelanggan Baru"
            pesanan, ms = m2.enqueue_pesanan_baru(nama)
            print(f"\n{pesanan[IDX_OID]} ({pesanan[IDX_PELANGGAN]}) masuk ke barisan paling belakang pada KEDUA antrean.")
            print(f"Panjang sekarang: naif {m2.naif.ukuran():,}, circular {m2.circular.ukuran():,} | Waktu: {ms:.2f} ms")

        elif opsi == 3:
            jml = int(input("Berapa kali dequeue naif? (misal 1 atau 100): ") or "1")
            keluar, geseran, ms = m2.dequeue_naif(jml)
            rata = geseran // len(keluar) if keluar else 0
            print(f"\n{len(keluar)} pesanan keluar dari depan antrean naif.")
            print(f"Total {geseran:,} elemen digeser, rata-rata {rata:,} geseran per dequeue.")
            print(f"Sisa antrean naif: {m2.naif.ukuran():,} | Waktu: {ms:.2f} ms")
            for idx, p in enumerate(keluar[:5]):
                print(f"  {idx+1}. {p[IDX_OID]} | {p[IDX_PELANGGAN]} | {p[IDX_RESTO]} | {p[IDX_MENU]} | {format_waktu(p[IDX_MASUK])}")

        elif opsi == 4:
            jml = int(input("Berapa kali dequeue circular? (misal 1 atau 100): ") or "1")
            keluar, ms = m2.dequeue_circular(jml)
            print(f"\n{len(keluar)} pesanan keluar dari depan antrean circular.")
            print(f"Tidak ada elemen yang digeser. front sekarang {m2.circular.front}, rear {m2.circular.rear}, kapasitas {m2.circular.kapasitas:,}.")
            print(f"Sisa antrean circular: {m2.circular.ukuran():,} | Waktu: {ms:.2f} ms")
            for idx, p in enumerate(keluar[:5]):
                print(f"  {idx+1}. {p[IDX_OID]} | {p[IDX_PELANGGAN]} | {p[IDX_RESTO]} | {p[IDX_MENU]} | {format_waktu(p[IDX_MASUK])}")

        elif opsi == 5:
            _, pesan, ms = m2.undo_last()
            print(f"\n{pesan}")
            print(f"Panjang antrean sekarang: naif {m2.naif.ukuran():,}, circular {m2.circular.ukuran():,}. "
                  f"Tumpukan undo {m2.undo_stack.ukuran}, redo {m2.redo_stack.ukuran} | Waktu: {ms:.2f} ms")

        elif opsi == 6:
            _, pesan, ms = m2.redo_last()
            print(f"\n{pesan}")
            print(f"Panjang antrean sekarang: naif {m2.naif.ukuran():,}, circular {m2.circular.ukuran():,}. "
                  f"Tumpukan undo {m2.undo_stack.ukuran}, redo {m2.redo_stack.ukuran} | Waktu: {ms:.2f} ms")

        elif opsi == 7:
            print("\n--- STATISTIK M2 ---")
            for k, v in m2.stats():
                print(f"{k:<22}: {v:,}")

        elif opsi == len(menu_opsi):
            break


if __name__ == "__main__":
    start()