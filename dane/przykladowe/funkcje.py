""" MODUL DO PLIKU wczytanie_danych_TIMESTAMP.py
    zawiera funkcje wykorzystywane w tym skrypcie"""

import numpy as np
import matplotlib.pyplot as plt
offset = 4

normalizacja = True

##############################################################################################
fs = 52 # Hz
klasyfikuj_co_n_s = 1 # co ile chcemy klasyfikowac
##############################################################################################
#       ETYKIETY DANYCH :
marsz = 0
trucht = 1
bieg = 2
##############################################################################################
def wczytaj_dane_z_pliku_csv(nazwa_pliku_csv, offset, etykieta ):
    lista_na_dane = []
    with open(nazwa_pliku_csv,"r") as plik :
        licznik_linii = 0
        for linia in plik:
            licznik_linii += 1
            if licznik_linii > offset :
                linia_tokeny = linia.split(',') # dzielimy stringa po ','
                wartosci = linia_tokeny[-4:-1]
                wartosci.append(etykieta)
                lista_na_dane.append(wartosci)# dane o ksztalcie (shape) np.(1243,3)

    return lista_na_dane

# with -> zapewnia zamkniecie pliku w przypadku bledu

def wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_csv, offset, etykieta ):
    lista_na_dane = []
    result = []
    with open(nazwa_pliku_csv,"r") as plik :
        licznik_linii = 0
        for linia in plik:
            licznik_linii += 1
            if licznik_linii > offset :
                linia_tokeny = linia.split(',') # dzielimy stringa po ','
                wartosci = linia_tokeny[-6:-5] + linia_tokeny[-4:-1] # [-6] Node Timestamp
                wartosci.append(etykieta)
                lista_na_dane.append(wartosci)# dane o ksztalcie (shape) np.(1243,3)
        lista_na_dane.sort() # sortujemy po Timestamp'ie
        
        for i in range(len(lista_na_dane)): # usuwamy Timestamp z rezultatu
            result.append(lista_na_dane[i][1:])
    return result

# with -> zapewnia zamkniecie pliku w przypadku bledu



def wyodrebnij_os_z_tablicy(tablica, numer_osi):
    os = []
    licznik = 0
    for wiersz in tablica :
        os.append(tablica[licznik][numer_osi])
        licznik += 1

    return os

def normalizuj(x): # dokladniej standaryzacja - wartosc srednia 0 i odchylenie standardowe 1
    x -= x.mean()
    x /= x.std()

def rysuj_wykres(tablica_danych, fs,label,x_label,y_label):
    Ts = 1/fs
    t=np.arange(0,Ts*len(tablica_danych),Ts)
    plt.plot(t,tablica_danych,'b',label=label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()

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

def ustaw_w_losowej_kolejnosci(kolejnosc,tablica_oryginalna, tablica_docelowa,liczba_probek):
    licznik = 0
    while(licznik < liczba_probek):
        tablica_docelowa[licznik] = tablica_oryginalna[kolejnosc[licznik]]
        licznik += 1

def wyznacz_etykiete(etykieta_pliku):
    if ( etykieta_pliku.find("Bieg") !=(-1) ):
        return bieg
    elif (etykieta_pliku.find("Marsz") !=(-1)):
        return marsz
    elif ( etykieta_pliku.find("Trucht") !=(-1) ):
        return trucht
    else :
        return -1 # blad


def wczytaj_dane_z_plikow():
    import os # biblioteka do poruszania sie w systemie plikow
    lista_przetworzonych_plikow = [] # lista na nazwy plikow ktore byly juz przetwarzane
    oznaczenie_gyr = "_Gyroscope.csv"
    lista_akc = [] # lista na dane z akcelerometru
    lista_gyr = [] # lista na dane z zyroskopu

    with os.scandir(os.curdir) as katalog_roboczy:
        print("DANE WCZYTYWANE Z PLIKOW:")
        for plik in katalog_roboczy:
            if(plik.name.find("Accelerometer.csv") != (-1) and not ( plik.name in lista_przetworzonych_plikow ) ) : # szukamy plikow akcelerometru, ktore nie byly jeszcze przetwarzane
                print(plik.name)
                nazwa_pliku_tokeny = plik.name.split('_') # dzielimy po _
                etykieta_pliku = nazwa_pliku_tokeny[0]
                nazwa_pliku_gyr = etykieta_pliku + oznaczenie_gyr
                etykieta = wyznacz_etykiete(etykieta_pliku)
                if ( etykieta != (-1) ): # jezeli nazwa pliku zawiera etykiete danych
                    # WCZYTAJ DANE
                    lista_tmp_akc = wczytaj_dane_z_pliku_csv_Timestamp(plik.name,offset,etykieta)
                    lista_tmp_gyr = wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_gyr,offset,etykieta)
                    # DOPASUJ ROZMIAR
                    dopasuj_rozmiar_listy(lista_tmp_akc)
                    dopasuj_rozmiar_listy(lista_tmp_gyr)
                    # DODAJ DO BUFORA
                    lista_akc += lista_tmp_akc
                    lista_gyr += lista_tmp_gyr
                else :
                    print("\nZLY PLIK CSV!!!\n NAZWA : " + plik.name + "\n")
                lista_przetworzonych_plikow.append(plik.name)

    return (lista_akc,lista_gyr)
        
################################################################################################
