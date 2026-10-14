import csv
class Array:
    def __init__(self):
        with open('data/pesanan.csv',newline='') as list_data:
            reader = csv.DictReader(list_data)
            self.reader = list(reader)

        self.data = []
        print(len(self.data))
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
            self.data.insert(0,data)

        elif data['prioritas'] == 2:
            for index, row in enumerate(self.data):
                if int(row['prioritas']) == 3:
                    self.data.insert(index, data)
                    break

            else:
                self.data.append(data)

        elif data['prioritas'] == 3:
            self.data.append(data)

        self.history.append(data['pelanggan'])
        print(self.history)
        aku_mau_print = [prioritas['prioritas'] for prioritas in self.data]
        print(aku_mau_print)
            
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

    if aku_mau == len(m1):
        break