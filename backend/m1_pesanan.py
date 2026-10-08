import csv
class Array:
    def __init__(self):
        with open('data/pesanan.csv',newline='') as pesanan:
            reader = csv.DictReader(pesanan)
            self.reader = list(reader)
            # print(int(self.reader[0]['prioritas']))
    def append(self):
        M = []
        for row in self.reader:
            if row['prioritas'] == '1':
                M.append(row['pelanggan'])
                print(M)
    def insert(self):
        pass
    def get(self):
        pass

test = Array()
test.append()
