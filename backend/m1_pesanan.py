import csv
class Array:
    def __init__(self):
        with open('data/pesanan.csv',newline='') as list_data:
            reader = csv.DictReader(list_data)
            self.reader = list(reader)

        self.data = []

    def melihat_pesanan(self):
        cek_id = input("Masukkan id (harus 6 digit) : ")
        cek_id = 'O-' + cek_id

        for row in self.reader:
            if cek_id == row["oid"]:
                print(row)
                break

        else:
            print("mungkin ada spasi atau salah ketik, coba koreksi kembali.")
            
arr = Array()

while(True):
    print("mau ngelakuin apa sekarang? ")
    m1 = ("melihat pesanan", "menambah pesanan reguler", "menambah pesanan prioritas", "menambah pesanan VIP", "menghapus pesanan","exit")
    for i in range(len(m1)):
        print(f"{i+1}.", m1[i])

    aku_mau = int(input(f"Masukkan angka 1 - {len(m1)} : "))
    if aku_mau == 1:
        arr.melihat_pesanan()

    if aku_mau == 6:
        break