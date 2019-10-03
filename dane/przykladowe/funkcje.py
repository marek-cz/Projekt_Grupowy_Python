""" MODUL DO PLIKU wczytanie_danych_TIMESTAMP.py
    zawiera funkcje wykorzystywane w tym skrypcie"""

import numpy as np
import matplotlib.pyplot as plt


##############################################################################################

def wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_csv, etykieta, offset=4 ):
    """ Wczytuje dane z pliku csv i sortuje je po timestampie
        Parametr offset ma domyslna wartosc i okresla ile linii
        poczatkowych pliku csv jets pomijanych."""
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
                lista_na_dane.append(wartosci)
        lista_na_dane.sort() # sortujemy po Timestamp'ie
        
        for i in range(len(lista_na_dane)): # usuwamy Timestamp z rezultatu
            result.append(lista_na_dane[i][1:])
    return result

# with -> zapewnia zamkniecie pliku w przypadku bledu



def wyodrebnij_os_z_tablicy(tablica, numer_osi):
    """ Wybranie z listy danych o formacie :
        [os_x os_y os_z, os_x os_y os_z, os_x os_y os_z,...]
        jednej z osi. Zwraca liste w postaci np.:
        [os_x0, os_x1, os_x2, ...]"""
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

def dopasuj_rozmiar_listy(lista, liczba_probek_w_paczce):
    """ Usuwa z listy tyle ostatnich pozycji aby jej dlugosc byla wielokrotnoscia
        liczby probek w paczce danych, ktora wchodzi na wejscie klasyfikatora"""
    if len(lista) % liczba_probek_w_paczce:
        liczba_paczek = len(lista) // liczba_probek_w_paczce
        liczba_rekordow_do_usuniecia = len(lista) - (liczba_paczek * liczba_probek_w_paczce)
        usun_ostatnie_N_rekordow(lista,liczba_rekordow_do_usuniecia)

def ustaw_w_losowej_kolejnosci(kolejnosc,tablica_oryginalna, tablica_docelowa,liczba_probek):
    """ Ustawia tablica_docelowa wedlug kolejnosci podanej w liscie kolejnosc"""
    licznik = 0
    while(licznik < liczba_probek):
        tablica_docelowa[licznik] = tablica_oryginalna[kolejnosc[licznik]]
        licznik += 1

def wyznacz_etykiete(etykieta_pliku, slownik_etykiet_danych ):
    """ Na podstawie etykiety pliku (fragment nazwy pliku
        np. Bieg w Bieg1_Accelerometer.csv ) wyznacza ety-
        kiete danych. Zwraca -1 gdy blad."""
    if ( etykieta_pliku.find("Bieg") !=(-1) ):
        return slownik_etykiet_danych["Bieg"]
    elif (etykieta_pliku.find("Marsz") !=(-1)):
        return slownik_etykiet_danych["Marsz"]
    elif ( etykieta_pliku.find("Trucht") !=(-1) ):
        return slownik_etykiet_danych["Trucht"]
    else :
        return -1 # blad


def wczytaj_dane_z_plikow(liczba_probek_w_paczce, slownik_etykiet_danych):
    """ Wczytuje dane z WSZYSTKICH plikow csv znajdujacych sie
        w tym samym katalogu."""
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
                etykieta = wyznacz_etykiete(etykieta_pliku, slownik_etykiet_danych)
                if ( etykieta != (-1) ): # jezeli nazwa pliku zawiera etykiete danych
                    # WCZYTAJ DANE
                    lista_tmp_akc = wczytaj_dane_z_pliku_csv_Timestamp(plik.name,etykieta)
                    lista_tmp_gyr = wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_gyr,etykieta)
                    # DOPASUJ ROZMIAR
                    dopasuj_rozmiar_listy(lista_tmp_akc,liczba_probek_w_paczce)
                    dopasuj_rozmiar_listy(lista_tmp_gyr,liczba_probek_w_paczce)
                    # DODAJ DO BUFORA
                    lista_akc += lista_tmp_akc
                    lista_gyr += lista_tmp_gyr
                else :
                    print("\nZLY PLIK CSV!!!\n NAZWA : " + plik.name + "\n")
                lista_przetworzonych_plikow.append(plik.name)

    return (lista_akc,lista_gyr)
        
################################################################################################
