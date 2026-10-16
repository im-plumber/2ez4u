import csv

def csv_data():
    # baca csv ke dalam list 2D biasa (tanpa dict)
    with open('data/pesanan.csv', newline='', encoding='utf-8') as list_data:
        reader = csv.reader(list_data)
        header = next(reader, None)
        return list(reader)


def ambil_nilai_kunci(baris, kunci):
    # urutan kolom: 0:oid, 1:pelanggan, 2:resto, 3:menu, 4:harga, 5:prioritas, 6:t_masuk, 7:t_selesai, 8:status
    if kunci == 'oid':
        return baris[0]
    elif kunci == 'harga':
        return int(baris[4]) if baris[4] != '' else 0
    elif kunci == 'selesai':
        # kalau belum selesai (kosong), taruh di paling belakang
        return int(baris[7]) if baris[7] != '' else 999999999
    return baris[0]


def insertion_sort(larik, kunci='oid'):
    # batas maksimal 20.000 baris biar aplikasi gak freeze
    if len(larik) > 20000:
        return None, -1, -1

    hasil = list(larik)
    perbandingan = 0
    pemindahan = 0

    for i in range(1, len(hasil)):
        item_sekarang = hasil[i]
        nilai_sekarang = ambil_nilai_kunci(item_sekarang, kunci)
        j = i - 1

        while j >= 0:
            perbandingan += 1
            # pakai > supaya tetap stabil
            if ambil_nilai_kunci(hasil[j], kunci) > nilai_sekarang:
                hasil[j + 1] = hasil[j]
                pemindahan += 1
                j -= 1
            else:
                break

        hasil[j + 1] = item_sekarang
        pemindahan += 1

    return hasil, perbandingan, pemindahan


def merge_sort(larik, kunci='oid'):
    pencacah = [0, 0]  # [perbandingan, pemindahan]

    def urutkan(data):
        if len(data) <= 1:
            return data

        tengah = len(data) // 2
        kiri = urutkan(data[:tengah])
        kanan = urutkan(data[tengah:])

        return gabung(kiri, kanan)

    def gabung(kiri, kanan):
        hasil = []
        i = 0
        j = 0

        while i < len(kiri) and j < len(kanan):
            pencacah[0] += 1
            # pakai <= supaya elemen kiri didahulukan kalau kuncinya sama (stabil)
            if ambil_nilai_kunci(kiri[i], kunci) <= ambil_nilai_kunci(kanan[j], kunci):
                hasil.append(kiri[i])
                pencacah[1] += 1
                i += 1
            else:
                hasil.append(kanan[j])
                pencacah[1] += 1
                j += 1

        # salin sisa elemen yang belum masuk
        while i < len(kiri):
            hasil.append(kiri[i])
            pencacah[1] += 1
            i += 1

        while j < len(kanan):
            hasil.append(kanan[j])
            pencacah[1] += 1
            j += 1

        return hasil

    terurut = urutkan(list(larik))
    return terurut, pencacah[0], pencacah[1]


def linear_search(larik, target):
    perbandingan = 0
    for i in range(len(larik)):
        perbandingan += 1
        if larik[i][0] == target:
            return i, larik[i], perbandingan
    return -1, None, perbandingan


def binary_search(larik_terurut, target):
    lo = 0
    hi = len(larik_terurut) - 1
    perbandingan = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        perbandingan += 1
        oid_tengah = larik_terurut[mid][0]

        if oid_tengah == target:
            return mid, larik_terurut[mid], perbandingan
        elif oid_tengah < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, None, perbandingan