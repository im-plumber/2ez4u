import csv

def csv_data():
    # baca data pesanan dari csv tanpa pakai dict bawaan
    with open('data/pesanan.csv', newline='', encoding='utf-8') as list_data:
        reader = csv.reader(list_data)
        header = next(reader, None)
        return list(reader)


class Stack:
    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.kosong():
            return None
        return self.data.pop()

    def peek(self):
        if self.kosong():
            return None
        return self.data[-1]

    def kosong(self):
        return len(self.data) == 0

    def ukuran(self):
        return len(self.data)


def pecah_token(ekspresi):
    token_list = []
    angka = ""
    for char in ekspresi:
        if char.isdigit():
            angka += char
        else:
            if angka != "":
                token_list.append(angka)
                angka = ""
            if char in "+-*/()":
                token_list.append(char)
    if angka != "":
        token_list.append(angka)
    return token_list


def derajat_op(op):
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0


def ke_postfix(ekspresi):
    # ubah struk infix ke bentuk postfix pakai stack
    tokens = pecah_token(ekspresi)
    tumpukan = Stack()
    keluaran = []

    for t in tokens:
        if t.isdigit():
            keluaran.append(t)
        elif t == '(':
            tumpukan.push(t)
        elif t == ')':
            while not tumpukan.kosong() and tumpukan.peek() != '(':
                keluaran.append(tumpukan.pop())
            tumpukan.pop()  # buang kurung buka
        else:
            while (not tumpukan.kosong() and tumpukan.peek() != '(' and
                   derajat_op(tumpukan.peek()) >= derajat_op(t)):
                keluaran.append(tumpukan.pop())
            tumpukan.push(t)

    while not tumpukan.kosong():
        keluaran.append(tumpukan.pop())

    return " ".join(keluaran)


def hitung(postfix):
    # hitung hasil akhir dari postfix pakai stack angka
    if isinstance(postfix, str):
        tokens = postfix.split()
    else:
        tokens = postfix

    tumpukan = Stack()

    for t in tokens:
        if t.isdigit() or (len(t) > 1 and t[0] == '-' and t[1:].isdigit()):
            tumpukan.push(int(t))
        else:
            # pop kanan dulu baru kiri biar pengurangan & pembagian gak kebalik
            b = tumpukan.pop()
            a = tumpukan.pop()
            if a is None or b is None:
                return 0
            if t == '+':
                tumpukan.push(a + b)
            elif t == '-':
                tumpukan.push(a - b)
            elif t == '*':
                tumpukan.push(a * b)
            elif t == '/':
                tumpukan.push(a // b if b != 0 else 0)

    hasil = tumpukan.pop()
    return hasil if hasil is not None else 0


class AntreanNaif:
    def __init__(self):
        self.data = []
        self.total_geseran = 0

    def enqueue(self, x):
        self.data.append(x)

    def dequeue(self):
        if self.is_empty():
            return None
        keluar = self.data[0]
        n = len(self.data)
        # geser manual ke kiri buat ngitung jumlah geseran
        for i in range(n - 1):
            self.data[i] = self.data[i + 1]
        self.data.pop()
        if n > 1:
            self.total_geseran += (n - 1)
        return keluar

    def hapus_belakang(self):
        if self.is_empty():
            return None
        return self.data.pop()

    def masuk_depan(self, daftar_item):
        self.data = list(daftar_item) + self.data

    def is_empty(self):
        return len(self.data) == 0


class AntreanMelingkar:
    def __init__(self, kapasitas=32768):
        self.K = kapasitas
        self.data = [None] * self.K
        self.front = 0
        self.rear = 0
        self.count = 0

    def perbesar(self):
        # gandakan kapasitas kalau antrean penuh
        kapasitas_baru = self.K * 2
        data_baru = [None] * kapasitas_baru
        for i in range(self.count):
            data_baru[i] = self.data[(self.front + i) % self.K]
        self.data = data_baru
        self.front = 0
        self.rear = self.count
        self.K = kapasitas_baru

    def enqueue(self, x):
        if self.count == self.K:
            self.perbesar()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.K
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.K
        self.count -= 1
        return x

    def hapus_belakang(self):
        if self.is_empty():
            return None
        self.rear = (self.rear - 1 + self.K) % self.K
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x

    def masuk_depan(self, daftar_item):
        while self.count + len(daftar_item) > self.K:
            self.perbesar()
        for item in reversed(daftar_item):
            self.front = (self.front - 1 + self.K) % self.K
            self.data[self.front] = item
            self.count += 1

    def is_empty(self):
        return self.count == 0


class SistemAntrean:
    def __init__(self):
        self.naif = AntreanNaif()
        self.circular = AntreanMelingkar(32768)
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.nomor_baru = 200001
        self.muat_awal()

    def muat_awal(self):
        semua = csv_data()
        for baris in semua:
            # indeks 8 adalah kolom status
            if len(baris) > 8 and baris[8] == 'ANTRE':
                self.naif.enqueue(baris)
                self.circular.enqueue(baris)

    def enqueue(self, pelanggan):
        oid = f"O-{self.nomor_baru:06d}"
        self.nomor_baru += 1
        pesanan_baru = [oid, pelanggan, "kafe-teknik", "roti-bakar", "12000", "2", "28800", "", "ANTRE"]

        self.naif.enqueue(pesanan_baru)
        self.circular.enqueue(pesanan_baru)

        # catat ke undo dan kosongkan redo
        self.undo_stack.push(("ENQUEUE", pesanan_baru))
        self.redo_stack = Stack()
        return pesanan_baru

    def dequeue_naif(self, jumlah=1):
        keluar = []
        geser_awal = self.naif.total_geseran
        for _ in range(jumlah):
            item = self.naif.dequeue()
            if item is not None:
                keluar.append(item)
        geseran_aksi = self.naif.total_geseran - geser_awal
        if keluar:
            self.undo_stack.push(("DEQUEUE_NAIF", keluar))
            self.redo_stack = Stack()
        return keluar, geseran_aksi

    def dequeue_circular(self, jumlah=1):
        keluar = []
        for _ in range(jumlah):
            item = self.circular.dequeue()
            if item is not None:
                keluar.append(item)
        if keluar:
            self.undo_stack.push(("DEQUEUE_CIRCULAR", keluar))
            self.redo_stack = Stack()
        return keluar

    def undo_last(self):
        if self.undo_stack.kosong():
            return None
        aksi, data = self.undo_stack.pop()

        if aksi == "ENQUEUE":
            self.naif.hapus_belakang()
            self.circular.hapus_belakang()
        elif aksi == "DEQUEUE_NAIF":
            self.naif.masuk_depan(data)
        elif aksi == "DEQUEUE_CIRCULAR":
            self.circular.masuk_depan(data)

        self.redo_stack.push((aksi, data))
        return aksi, data

    def redo_last(self):
        if self.redo_stack.kosong():
            return None
        aksi, data = self.redo_stack.pop()

        if aksi == "ENQUEUE":
            self.naif.enqueue(data)
            self.circular.enqueue(data)
        elif aksi == "DEQUEUE_NAIF":
            for _ in range(len(data)):
                self.naif.dequeue()
        elif aksi == "DEQUEUE_CIRCULAR":
            for _ in range(len(data)):
                self.circular.dequeue()

        self.undo_stack.push((aksi, data))
        return aksi, data

    def history(self):
        return list(self.undo_stack.data)

    def stats(self):
        return (
            len(self.naif.data),
            self.circular.count,
            self.circular.K,
            self.naif.total_geseran,
            self.undo_stack.ukuran(),
            self.redo_stack.ukuran()
        )