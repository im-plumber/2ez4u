import csv
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

        for index, row in enumerate(self.antrian):
            if data['pelanggan'] == row['pelanggan']:
                self.antrian.pop(index)

        aku_mau_print = [id['oid'] for id in self.antrian]
        print(aku_mau_print)

def start_arr():
    arr = Array()
    while(True):
        print("mau ngelakuin apa sekarang? ")
        m1 = ("melihat pesanan", "menambah pesanan", "menghapus pesanan","exit")
        for i in range(len(m1)):
            print(f"{i+1}.", m1[i])

        aku_mau = int(input(f"Masukkan angka 1 - {len(m1)} : "))
        if aku_mau == 1:
            print(arr.melihat_pesanan())

        if aku_mau == 2:
            arr.menambah_pesanan()

        if aku_mau == 3:
            arr.menghapus_pesanan()

        if aku_mau == len(m1):
            break

class LinkedList:
    def __init__(self,data):
            with open('data/pesanan.csv',newline='') as list_data:
                reader = csv.DictReader(list_data)
                self.reader = list(reader)
    
            self.data = data
            self.next = None   
 
            
def start_linked():
    link = LinkedList()
    while(True):
        print("mau ngelakuin apa sekarang? ")
        m1 = ("melihat pesanan", "menambah pesanan", "menghapus pesanan","exit")
        for i in range(len(m1)):
            print(f"{i+1}.", m1[i])

        aku_mau = int(input(f"Masukkan angka 1 - {len(m1)} : "))
        if aku_mau == 1:
            print(link.melihat_pesanan())

        if aku_mau == 2:
            link.menambah_pesanan()

        if aku_mau == 3:
            link.menghapus_pesanan()

        if aku_mau == len(m1):
            break
