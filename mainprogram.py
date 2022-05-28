
def menuawal(): #display awal (jihan)
    print("""
    =================SELAMAT DATANG===================
                      Roti Bakar 12
    Jl Kebangkitan No. 38, Kec. Laweyan, Kota Surakarta
                  Telp. (0271) 765331
    ==================================================
    1. menu pesan
    2. cek pesanan
    3. exit
    ==================================================""")
    

def menupesan(): #faatih, jihan (odi buat csv)
    print()


def menucek(): #apang, odi
    print()

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

def main(): #alur program (faatih)
    menuawal()
    pilihan = int(input("Ingin ke menu apa?"))
    if pilihan == 1 :
        menupesan()
    elif pilihan == 2 :
        menucek()
    elif pilihan == 3 :
        menuexit()
    else :
        menuawal()

