import csv
import time

class Array:
    def __init__(self):
        with open('data/pesanan.csv',newline='') as list_data:
            reader = csv.DictReader(list_data)
            self.reader = list(reader)

        self.antrian = []
        print(len(self.antrian))
        self.history = []       

    def melihat_pesanan(self):
        cek_id = input("Masukkan id (harus 6 digit) : ")
        cek_id = 'O-' + cek_id

        for row in self.reader:
            if cek_id == row["oid"]:
                return row
                break

        else:
            print("mungkin ada spasi atau salah ketik, coba koreksi kembali.")


    def menambah_pesanan(self):

        # data berupa dict
        data = self.melihat_pesanan()

        data['prioritas'] = int(data['prioritas'])

        for row in self.history:
            if row == data['pelanggan']:
                raise InterruptedError("data sudah tersedia!")
                

        if data['prioritas'] == 1:
            self.antrian.insert(0,data)

        elif data['prioritas'] == 2:
            for index, row in enumerate(self.antrian):
                if int(row['prioritas']) == 3:
                    self.antrian.insert(index, data)
                    break

            else:
                self.antrian.append(data)

        elif data['prioritas'] == 3:
            self.antrian.append(data)

        self.history.append(data['pelanggan'])
        print(self.history)
        # aku_mau_print = [prioritas['prioritas'] for prioritas in self.antrian]
        # print(aku_mau_print)
        aku_mau_print = [id['oid'] for id in self.antrian]
        print(aku_mau_print)    


    def menghapus_pesanan(self):
        # data berupa dict
        data = self.melihat_pesanan()

        time_start = time.perf_counter()
        for index, row in enumerate(self.antrian):
            if data['pelanggan'] == row['pelanggan']:
                self.antrian.pop(index)

        aku_mau_print = [id['oid'] for id in self.antrian]
        print(aku_mau_print)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        with open('data/pesanan.csv', newline='') as list_data:
            reader = csv.DictReader(list_data)
            self.reader = list(reader)
            
        self.head = None
        self.tail = None
        self.history = []

    def melihat_pesanan(self):
        cek_id = input("Masukkan id (harus 6 digit) : ")
        cek_id = 'O-' + cek_id

        for row in self.reader:
            if cek_id == row["oid"]:
                return row
        else:
            print("mungkin ada spasi atau salah ketik, coba koreksi kembali.")
            return None

    def menambah_pesanan(self):
        data = self.melihat_pesanan()
        if data is None:
            return

        # jaga-jaga agar data di self.reader tidak berubah
        data = data.copy()
        data['prioritas'] = int(data['prioritas'])

        # Cek apakah pelanggan sudah ada di history
        for row in self.history:
            if row == data['pelanggan']:
                raise InterruptedError("data sudah tersedia!")

        new_node = Node(data)

        # kondisi prioritas
        if self.head is None:
            self.head = new_node
            self.tail = new_node

        elif data['prioritas'] == 1:
            new_node.next = self.head
            self.head = new_node

        elif data['prioritas'] == 2:
            if int(self.head.data['prioritas']) == 3:
                new_node.next = self.head
                self.head = new_node
            else:
                current = self.head
                while current.next is not None and int(current.next.data['prioritas']) != 3:
                    current = current.next
                
                new_node.next = current.next
                current.next = new_node
                
                if new_node.next is None:
                    self.tail = new_node

        # Kondisi 4: Prioritas 3 (Selalu masuk di paling belakang / menjadi tail baru)
        elif data['prioritas'] == 3:
            self.tail.next = new_node
            self.tail = new_node

        # Catat ke history dan cetak hasil antrian
        self.history.append(data['pelanggan'])
        print(self.history)
        self.cetak_antrian()

    def menghapus_pesanan(self):
        data = self.melihat_pesanan()
        if data is None or self.head is None:
            return

        current = self.head
        prev = None

        while current is not None:
            if current.data['pelanggan'] == data['pelanggan']:
                if prev is None:
                    self.head = current.next
                    if self.head is None:
                        self.tail = None
                
                else:
                    prev.next = current.next
                    if current.next is None:
                        self.tail = prev
                break
            
            prev = current
            current = current.next

        self.cetak_antrian()

    def cetak_antrian(self):
        aku_mau_print = []
        current = self.head
        while current is not None:
            aku_mau_print.append(current.data['oid'])
            current = current.next
        print(aku_mau_print)

def start():
    arr = Array()
    link = LinkedList()
    while(True):
        print("mau ngelakuin apa sekarang? ")
        m1 = ("melihat pesanan", "menambah pesanan", "menghapus pesanan","exit")
        for i in range(len(m1)):
            print(f"{i+1}.", m1[i])

        aku_mau = int(input(f"Masukkan angka 1 - {len(m1)} : "))
        if aku_mau == 1:
            print(arr.melihat_pesanan())
            print(link.melihat_pesanan())

        if aku_mau == 2:
            arr.menambah_pesanan()
            link.menambah_pesanan()

        if aku_mau == 3:
            arr.menghapus_pesanan()
            link.menghapus_pesanan()

        if aku_mau == len(m1):
            break

start()