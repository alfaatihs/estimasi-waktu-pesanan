import csv
from tabulate import tabulate
import datetime
import time

def listconversion(list,column,func):
    for i in range (len(list)):
        list[i][column] = func(list[i][column])
    
    return list

def displayrupiah(value):
    str_value = str(value)
    separate_decimal = str_value.split(".")
    after_decimal = separate_decimal[0]
    before_decimal = separate_decimal[1]

    reverse = after_decimal[::-1]
    temp_reverse_value = ""

    for index, val in enumerate(reverse):
        if (index + 1) % 3 == 0 and index + 1 != len(reverse):
            temp_reverse_value = temp_reverse_value + val + "."
        else:
            temp_reverse_value = temp_reverse_value + val

    temp_result = temp_reverse_value[::-1]

    return "Rp " + temp_result

def menucek(): #apang, odi
    print("""
    ==========================================
                Cek Pesanan Anda
    ==========================================
    """) 
    print("Masukkan Nomor Pesanan")
    nopesanan = int(input(">> "))
    
    '''
    print("""
    ==========================================
        Estimasi Waktu Pesanan Anda 
    ==========================================
    """)
    

    '''
            
def menuexit(): #konfirmasi exit (apang)
    print("""
    ==========================================
                Yakin untuk Keluar?
    ==========================================
    1. Tidak
    2. Keluar                
    ================TERIMAKASIH===============
    """)
    pilihan = int(input("Yakin untuk Keluar?"))
    if pilihan == 1 :
        menuawal()
    elif pilihan == 2:
        quit()
    else:
        menuexit()

def inputdatadiri():
    print("""
    ==========================================
                Masukkan Data Diri
    """)
    nama = input("Nama = ")
    notelp = input("No Telp = ")
    print("""
    ==========================================
                Pilih Kecamatan
    ==========================================
    1. Laweyan
    2. Serengan
    3. Jebres
    4. Banjarsari
    5. Pasar Kliwon
    """)
    
    kecamatan = int(input(">> "))
    if kecamatan == 1:
        ongkir = 6000
    elif kecamatan ==2:
        ongkir = 10000
    elif kecamatan == 3:
        ongkir = 8000
    elif kecamatan == 4:
        ongkir = 9000
    elif kecamatan == 5:
        ongkir = 7000
    else:
        print("Input tidak valid, silahkan coba lagi")
        inputdatadiri()
    
    print("Masukkan alamat lengkap =")
    alamat = input(">> ")

def konfirmasi():
    try:    
        print(tabulate(listpesanan,headers=["Pesanan","Jumlah","Harga"],tablefmt="pretty"))
    
        print("Total harga = ", displayrupiah(totalharga))
    
        print("""
        ==========================================
              Apakah Pesanan Sudah Sesuai?
        ==========================================
        1. Ya
        2. Tidak              
        ================TERIMAKASIH===============
        """)
        jawaban = int(input(">> "))
        if jawaban == 1 :
            inputdatadiri()
        elif jawaban == 2 :
            print("Pesanan anda telah direset")
            menupesan()
        else :
            print("\nInput tidak valid. silahkan coba lagi")
            konfirmasi()

    except ValueError:
        print("\nInput tidak valid. Silahkan Coba Lagi")
        konfirmasi()

def hitungkonfirmasi():
    global totalharga
    totalharga = 0
    for i in range(len(listpesanan)):
        totalharga = totalharga + listpesanan[i][2]
    
    totalharga = float(totalharga)

    listconversion(listpesanan,2,float)
    listconversion(listpesanan,2,displayrupiah)
    konfirmasi()

def inputmenupesan():
    #input pesanan & menambahkan pesanan ke list
    try:
        print("\nPilih Menu Roti Bakar (1-15), 0 Jika selesai memilih")
        pilihan = int(input(">> "))
        if pilihan == 0:
            hitungkonfirmasi()
        elif pilihan in range (1,16):
            listpilihan = []
            print()
            print(displaymenu[pilihan][1])
            print(displaymenu[pilihan][2])
            jumlah = int(input("Jumlah: "))
            totalpilihan = float(listmenu[pilihan][2]*jumlah)
            print("Total harga: ",displayrupiah(totalpilihan))
            listpilihan.append(listmenu[pilihan][1])
            listpilihan.append(jumlah)
            listpilihan.append(listmenu[pilihan][2]*jumlah)
            listpesanan.append(listpilihan)
            inputmenupesan()
        else:
            print("Input tidak valid. Silahkan coba lagi")
            inputmenupesan()

    except ValueError:
        print("Input tidak valid, silahkan coba lagi")
        inputmenupesan()

def menupesan(): #faatih, jihan (odi buat csv)
    
    global displaymenu
    global listmenu
    
    #parsing dan konversi csv menjadi list
    #listmenu untuk perhitungan, displaymenu untuk display
    with open ('Menu.csv','r') as filemenu: 
        readmenu = csv.reader(filemenu)
        listmenu = list(readmenu)

    with open ('Menu.csv','r') as filemenu: 
        readmenu = csv.reader(filemenu)
        displaymenu = list(readmenu)

    listconversion(listmenu[1:],2,int)
    listconversion(displaymenu[1:],2,float)
    listconversion(displaymenu[1:],2,displayrupiah)
    
    #print menu
    titlemenupesan = "DAFTAR MENU ROTI BAKAR 12"
    print(titlemenupesan.center(45,' '))
    print(tabulate(displaymenu[1:],headers=displaymenu[0],tablefmt="pretty"))
    
    global listpesanan
    listpesanan = []
    inputmenupesan()    

def menuawal(): #display awal (jihan)
    print("""
    =================SELAMAT DATANG===================
                      Roti Bakar 12
    Jl Kebangkitan No. 38, Kec. Laweyan, Kota Surakarta
                  Telp. (0271) 765331
    ==================================================
    1. Pesan
    2. Cek Pesanan
    3. Exit
    ==================================================""")

def main(): #alur program (faatih)
    menuawal()
    pilihan = int(input(">> "))
    if pilihan == 1 :
        menupesan()
    elif pilihan == 2 :
        menucek()
    elif pilihan == 3 :
        menuexit()
    else :
        menuawal()

main()
