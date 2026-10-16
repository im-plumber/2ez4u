import csv

def csv_data():
    with open('data/pesanan.csv', newline='') as list_data:
        reader = csv.DictReader(list_data)
        reader = list(reader)
        return reader        # data berupa dict

def cetak(antrian):
    antrian = [(pelanggan['pelanggan'], pelanggan['oid']) for pelanggan in antrian]
    return print(antrian)

class Array:
    def __init__(self):
        self.reader = csv_data()

        self.antrian = []

        self.history = []

    def melihat_pesanan(self):
        cek_id = int(input("Masukkan id (harus 6 digit) : "))
        
        print(self.reader[cek_id - 1])

        return self.reader[cek_id - 1]

        
    def menambah_pesanan(self):

        # data berupa dict
        data = self.melihat_pesanan()
        if data is None:
            return

        data['prioritas'] = int(data['prioritas'])

        for row in self.history:
            if row == data['pelanggan']:
                raise InterruptedError("data sudah tersedia!")

            else:
                # cek nama-nama yang sudah pernah ditambahkan
                self.history.append(data['pelanggan'])
                print(self.history)
                
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


        # sekadar check prioritasnya sudah benar atau belum
        cetak(self.antrian)


    def menghapus_pesanan(self):

        data = self.melihat_pesanan()
        if data is None:
            return

        for index, row in enumerate(self.antrian):
            if data['pelanggan'] == row['pelanggan']:
                self.antrian.pop(index)
                
                for row in self.history:
                    if row == data['pelanggan']:
                        self.history.pop(row)
                        break
                break

        cetak(self.antrian)


class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.reader = csv_data()
        self.head = None

    def cetak_antrian(self):
        hasil = []
        pointer = self.head
        while pointer:
            hasil.append((pointer.data['pelanggan'], pointer.data['oid']))
            pointer = pointer.next
        print(f"Antrian saat ini: {hasil}")

    def melihat_pesanan(self):
        cek_id = input("Masukkan id (harus 6 digit) : ")
        cek_id = 'O-' + cek_id

        for row in self.reader:
            if cek_id == row['oid']:
                return row
                break

    def menambah_pesanan(self):
        data = self.melihat_pesanan()

        new_node = Node(data)

        prioritas = int(data['prioritas'])

        if self.head is None or prioritas < int(self.head.data['prioritas']):
            new_node.next = self.head
            self.head = new_node

        else:
            pointer = self.head
            while pointer.next and int(pointer.next.data['prioritas']) <= prioritas:
                pointer = pointer.next
            
            new_node.next = pointer.next
            pointer.next = new_node

        self.cetak_antrian()

    def menghapus_pesanan(self):
        data = self.melihat_pesanan()
        if data is None or self.head is None:
            print("Antrian kosong atau data tidak ditemukan.")
            return

        target_pelanggan = data['pelanggan']

        # Kasus jika node target berada di head
        if self.head.data['pelanggan'] == target_pelanggan:
            self.head = self.head.next
            self.cetak_antrian()
            return

        # Telusuri untuk mencari simpul target
        pointer = self.head
        while pointer.next and pointer.next.data['pelanggan'] != target_pelanggan:
            pointer = pointer.next

        if pointer.next is not None:
            pointer.next = pointer.next.next
        else:
            print("Data pesanan tidak ditemukan di dalam antrian.")

        self.cetak_antrian()

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
            arr.melihat_pesanan()
            print(link.melihat_pesanan())

        if aku_mau == 2:
            arr.menambah_pesanan()
            link.menambah_pesanan()

        if aku_mau == 3:
            arr.menghapus_pesanan()
            link.menghapus_pesanan()

        if aku_mau == len(m1):
            break

if __name__ == "__main__":
    start()