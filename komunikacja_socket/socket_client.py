# KOMUNIKACJA KLIENT - SERWER
# PROCES KLIENTA

fs = 52
klasyfikuj_co_n_s = 1

import socket
def wczytaj_dane_z_pliku_csv(nazwa_pliku_csv, offset ):
    lista_na_dane = []
    with open(nazwa_pliku_csv,"r") as plik :
        licznik_linii = 0
        for linia in plik:
            licznik_linii += 1
            if licznik_linii > offset :
                linia_tokeny = linia.split(',') # dzielimy stringa po ','
                wartosci = linia_tokeny[-4:-1]
                lista_na_dane.append(wartosci)

    return lista_na_dane

def wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_csv, offset ):
    lista_na_dane = []
    result = []
    with open(nazwa_pliku_csv,"r") as plik :
        licznik_linii = 0
        for linia in plik:
            licznik_linii += 1
            if licznik_linii > offset :
                linia_tokeny = linia.split(',') # dzielimy stringa po ','
                wartosci = linia_tokeny[-6:-5] + linia_tokeny[-4:-1] # [-6] Node Timestamp
                lista_na_dane.append(wartosci)# dane o ksztalcie (shape) np.(1243,3)
       # lista_na_dane.sort() # sortujemy po Timestamp'ie
        
        #for i in range(len(lista_na_dane)): # usuwamy Timestamp z rezultatu
        #    result.append(lista_na_dane[i][1:])
    #return result
    return lista_na_dane


def usun_ostatnie_N_rekordow(lista,N):
    licznik = 1
    while(licznik <= N):
        del(lista[(-1) * licznik])
        licznik += 1

def dopasuj_rozmiar_listy(lista, fs = fs,klasyfikuj_co_n_s = klasyfikuj_co_n_s):
    N = (klasyfikuj_co_n_s * fs) 
    if len(lista) % N:
        liczba_paczek = len(lista) // N
        liczba_rekordow_do_usuniecia = len(lista) - (liczba_paczek * N)
        usun_ostatnie_N_rekordow(lista,liczba_rekordow_do_usuniecia)

def polacz_liste_w_1D(lista):
    result = []
    for i in range(len(lista)):
        result.append(lista[i][0] +" " + lista[i][1]+ " " + lista[i][2])
    return result

def usun_timestamp(lista_probek_timestamp):
    result = []
    for probka in lista_probek_timestamp:
        result.append(probka[1:])
    return result

#############################################################################################

lista_akc_bieganie = wczytaj_dane_z_pliku_csv_Timestamp("Bieg1_Accelerometer.csv",5)
lista_gyr_bieganie = usun_timestamp( wczytaj_dane_z_pliku_csv_Timestamp("Bieg1_Gyroscope.csv",5) )
lista_akc_trucht   = wczytaj_dane_z_pliku_csv_Timestamp("Trucht3_Accelerometer.csv",5)
lista_gyr_trucht   = usun_timestamp( wczytaj_dane_z_pliku_csv_Timestamp("Trucht3_Gyroscope.csv",5) )

#usun_ostatnie_N_rekordow(lista_gyr_bieganie,1)# usune 1 linie z pliku...
dopasuj_rozmiar_listy(lista_akc_bieganie)
dopasuj_rozmiar_listy(lista_gyr_bieganie)
dopasuj_rozmiar_listy(lista_akc_trucht)
dopasuj_rozmiar_listy(lista_gyr_trucht)

dane_ack = lista_akc_bieganie + lista_akc_trucht
dane_gyr = lista_gyr_bieganie + lista_gyr_trucht

IP_SERWERA = "192.168.8.102" # IP serwera
PORT = 5005 # liczba 16-bitowa, wiekszta niz 1024
BUFOR_ROZMIAR = 4096

licznik = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# AF_INET - IPv4
# SOCK_STREAM - TCP
    s.connect((IP_SERWERA,PORT))
    while True:
        decyzja = input("Czy nadac porcje danych? T/N \n")
        if (decyzja == "T" or decyzja =="t" ) : decyzja = True
        else : decyzja = False

        if decyzja :
            probka_danych = []
            do_nadania = "Klasyfikacja " + input("Podaj ID zawodnika: \n") # Klasyfikuj aktywnosc zawodnika o zadanym ID 
            for i in range(fs * klasyfikuj_co_n_s):
                probka_danych.append(dane_ack[i + (licznik * fs * klasyfikuj_co_n_s )])
                probka_danych.append(dane_gyr[i + (licznik * fs * klasyfikuj_co_n_s )])
                do_nadania = do_nadania + " " + " ".join(probka_danych[2*i]) + " " + " ".join(probka_danych[(2*i) + 1])

            licznik = licznik+1
            if licznik == (len(dane_ack)//fs) : licznik = 0
            s.send(do_nadania.encode())
            data = s.recv(BUFOR_ROZMIAR)
            dane = data.decode()
        else : break
        if dane == "END" : break
        print("Odebrane dane to: \n",dane)
    
    #s.close()


