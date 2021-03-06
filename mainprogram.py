
import csv
from tabulate import tabulate
import datetime as dt
import locale as lc
import modul
import ast

lc.setlocale(lc.LC_TIME, 'IND') #mengubah format tanggal ke indonesia
no = 0

def menucek(): #apang, odi
    print("""
===============================================
                Cek Pesanan Anda
===============================================
    """) 
    print("Masukkan Nomor Pesanan")
    nopesanan = input(">> ")
    with open ('data.csv','r') as filedata :
        readdata = csv.reader(filedata)
        listdata = list(readdata)

    #index merupakan tuple berisi index no pesanan dalam csv
    index = modul.nestedlistindex(listdata,nopesanan)
    print()
    print("Detail Pesanan:")
    print()
    print("No Pesanan: ", listdata[index[0]][0])
    print()
    pesanan = ast.literal_eval(listdata[index[0]][7])
    print(tabulate(pesanan,headers=["Pesanan","Jumlah","Harga"],tablefmt="pretty"))
    print("Total Harga: ",modul.displayrupiah(float(listdata[index[0]][8])))
    print("Ongkir: ",modul.displayrupiah(float(listdata[index[0]][9])))
    print('Jumlah yang Harus dibayar: ',modul.displayrupiah(float(int(listdata[index[0]][8])+int(listdata[index[0]][9]))))
    print()

    jamsampai = listdata[index[0]][6] #memanggil jamsampai dari list
    jamsampai = dt.datetime.strptime(jamsampai,'%Y-%m-%d %H:%M:%S.%f') #mengubah jam sampai dari string ke format waktu
    waktusampai = jamsampai - dt.datetime.now() #menghitung waktu hingga pesanan tiba
    if int(waktusampai.total_seconds()) < 0:
        print("Pesanan Anda Seharusnya Sudah Sampai, Jika Belum Sampai Silahkan Hubungi Restoran")
        print("==================================================================================")
    display = modul.strfdelta(waktusampai, '{H:2} Jam, {M:02} Menit') #membuat format penampilan waktu
    print("Pesanan anda akan tiba dalam", display)
    print("===============================================")

    print("Tekan ENTER untuk kembali ke menu awal")
    inputvar = input(">> ")
    if inputvar == "":
        main()

def menuexit(): #konfirmasi exit (apang)
    print("""
==========================================
            Yakin untuk Keluar?
==========================================
1. Tidak
2. Keluar                
================TERIMAKASIH===============
    """)
    pilihan = int(input(">> "))
    if pilihan == 1 :
        main()
    elif pilihan == 2:
        quit()
    else:
        menuexit()

def generatenopesan():
    global no
    with open ('data.csv','r') as filedata :
        readdata = csv.reader(filedata)
        listdata = list(readdata)
    #nopesan berupa tanggal dan no urut
    date = dt.date.today()
    date = date.strftime("%Y%m%d")
    #jika ada pesanan di tanggal yang sama sebelumnnya no urut akan menyesuaikan
    if date in listdata[-1][0]:
        no = int(listdata[-1][0][-3:])
    
    no = no + 1
    nopesan = date + str(no).zfill(3)
    return nopesan
    
def kecamatan():
    global ongkir
    global lamakirim

    try:
        print("""
Pilih Kecamatan:
1. Laweyan
2. Serengan
3. Jebres
4. Banjarsari
5. Pasar Kliwon""")

        kecamatan = int(input(">> "))
        if kecamatan == 1:
            ongkir = 3000
            lamakirim = dt.timedelta(minutes=5) 
        elif kecamatan == 2:
            ongkir = 5000
            lamakirim = dt.timedelta(minutes=10) 
        elif kecamatan == 3:
            ongkir = 10000
            lamakirim = dt.timedelta(minutes=19) 
        elif kecamatan == 4:
            ongkir = 9000
            lamakirim = dt.timedelta(minutes=18) 
        elif kecamatan == 5:
            ongkir = 7000
            lamakirim = dt.timedelta(minutes=17) 
        else:
            print("Input tidak valid, silahkan coba lagi")
            kecamatan()

    except ValueError:
        print("Input tidak valid, silahkan coba lagi")
        kecamatan()

def timeygmana():
    with open ('data.csv','r') as filedata:
        readdata = csv.reader(filedata)
        listdata = list(readdata)
    try:
        #menghitung selisih waktu pemesanan dengan waktu pesanan sebelumnya selesai dibuat
        #untuk menentukan estimasi lama pembuatan
        waktuantre = dt.datetime.strptime(listdata[-1][5],'%Y-%m-%d %H:%M:%S.%f')
        selisih = waktuantre - timepesan
        if int(selisih.total_seconds()) < 0:
            return len(listdata[-1][5])
        else:
            return timepesan
    
    except ValueError:
        return timepesan
    
    except TypeError:
        return timepesan

    except IndexError :
        return timepesan

def receipt():
    print("Pesanan Anda Telah dibuat!")
    print("============================================")
    print()
    print("Detail Pesanan:")
    print()
    print("No Pesanan: ", datapesan[0])
    #strftime untuk format waktu
    print("Tanggal Pesan: ",timepesan.strftime("%A, %d %B %Y"))
    print("Jam Pesan: ", timepesan.strftime("%H:%M"))
    print()
    print("Nama: ",datapesan[1])
    print("No. Telp: ",datapesan[2])
    print("Alamat: ",datapesan[3])
    print()
    print(tabulate(listpesanan,headers=["Pesanan","Jumlah","Harga"]))
    print()
    print("Total harga = ", modul.displayrupiah(float(totalharga)))
    print("Ongkir = ", modul.displayrupiah(float(ongkir)))
    print("Jumlah yang Harus dibayar: ", modul.displayrupiah(float(totalharga + ongkir)))
    print("============================================")    
    print()
    print("Tekan ENTER untuk kembali ke menu awal")
    inputvar = input(">> ")
    if inputvar == "":
        main()

def writedatapesan():
    #menambahkan list sementara ke csv
    with open ('data.csv','a',newline='') as filedata:
        writedata = csv.writer(filedata)
        writedata.writerow(datapesan)
        filedata.close()
    receipt()

def waktu():
    global timepesan

    timepesan = dt.datetime.now() #mencatat waktu sekarang
    lamabuat = dt.timedelta(minutes=4*modul.sumcolumn(listpesanan,2)) 
    #lamabuat = waktu pembuatan satu roti bakar dikali jumlah rotibakar yang dipesan
    #waktu pembuatan semua varian rotibakar = 4 menit
    timejadi = timeygmana() + lamabuat
    timesampai = timejadi + lamakirim
    datapesan.append(timepesan)
    datapesan.append(timejadi)
    datapesan.append(timesampai)
    datapesan.append(listpesanan)
    datapesan.append(totalharga)
    datapesan.append(ongkir)
    writedatapesan()

def inputdatadiri():
    global datapesan

    print("""
==========================================
            Masukkan Data Diri
==========================================    
    """)
    nama = input("Nama = ")
    notelp = input("No Telp = ")
    kecamatan()
    print()
    print("Masukkan alamat lengkap =")
    alamat = input(">> ")
    print("============================================")

    nopesan = generatenopesan()
    datapesan = []
    datapesan.append(nopesan)
    datapesan.append(nama)
    datapesan.append(notelp)
    datapesan.append(alamat)
    waktu()

def konfirmasi():
    try:    
        print("================================================")
        print(tabulate(listpesanan,headers=["Pesanan","Jumlah","Harga"],tablefmt="pretty"))
    
        print("Total harga = ", modul.displayrupiah(float(totalharga)))
    
        print("""
Apakah Pesanan Sudah Sesuai?
1. Ya
2. Tidak
================================================
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
    totalharga = modul.sumcolumn(listpesanan,3)
    #sumcolumn inputnya kolom, listconversion inputnya index kolom

    modul.listconversion(listpesanan,2,float)
    modul.listconversion(listpesanan,2,modul.displayrupiah)
    konfirmasi()

def inputmenupesan():
    #input pesanan & menambahkan pesanan ke list
    try:
        print("\nPilih Menu Roti Bakar (1-15), 0 Jika selesai memilih")
        pilihan = int(input(">> "))
        if pilihan == 0:
            hitungkonfirmasi()
        elif pilihan in range (1,16):
            #pilihan digunakan sebagai index
            #index 0 = header
            listpilihan = []
            #print menu dan harga
            print()
            print(displaymenu[pilihan][1])
            print(displaymenu[pilihan][2])
            jumlah = int(input("Jumlah: "))
            #totalpilihan = total harga satu menu yang dipilih
            totalpilihan = float(listmenu[pilihan][2]*jumlah)
            print("Total harga: ",modul.displayrupiah(totalpilihan))
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

def menupesan():
    
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
    
    #konversi kolom ke-2 (harga) menjadi format yang dibutuhkan
    #integer untuk keperluan perhitungan total harga
    #float untuk input fungsi displayrupiah
    #displayrupiah untuk menjadikan string yang rapi
    modul.listconversion(listmenu[1:],2,int)
    modul.listconversion(displaymenu[1:],2,float)
    modul.listconversion(displaymenu[1:],2,modul.displayrupiah)
    
    #print menu
    titlemenupesan = "DAFTAR MENU ROTI BAKAR 12"
    print(titlemenupesan.center(45,' '))
    print(tabulate(displaymenu[1:],headers=displaymenu[0],tablefmt="pretty"))
    
    global listpesanan
    #listpesanan di define disini supaya saat kembali ke menupesan listpesanan direset
    listpesanan = []
    inputmenupesan()    

def menuawal():
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

def main():
    try:
        menuawal()
        pilihan = int(input(">> "))
        if pilihan == 1 :
            menupesan()
        elif pilihan == 2 :
            menucek()
        elif pilihan == 3 :
            menuexit()
        else :
            main()
    except ValueError:
        main()

if __name__ == "__main__":
    main()