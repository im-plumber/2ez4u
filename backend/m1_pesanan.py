import csv
import tkinter
class Array:
    def __init__(self):
        with open('data/pesanan.csv',newline='') as list_data:
            reader = csv.DictReader(list_data)
            self.reader = list(reader)
            
tes = Array()



