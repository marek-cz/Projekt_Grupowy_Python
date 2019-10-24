""" Skrypt majacy na celu wyodrebnienie poprawnych danych z plikow csv
    Chodzi o sytuacje w ktorej np. wlaczymy czujniki a jeszcze przez
    2 sekundy stoimy w miejscu a potem zaczynamy bieganie
    Czlowiek ocenia poprawnosc danych..."""

# import bibliotek

import numpy as np
import matplotlib.pyplot as plt
import os # biblioteka do poruszania sie w systemie plikow
import funkcje as f

###############################################################################
def rysuj_wykres(czas,tablica_danych,y_label,label = 'dane',x_label = 'timestamp'):

    plt.clf()
    plt.plot(czas,tablica_danych,'b',label=label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()

def FFT_sygnalu(sygnal,Fs = 100):
    n = len(sygnal) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range

    frq = frq[range(int(n/2))] # one side frequency range

    Y = np.fft.fft(sygnal)/n # fft computing and normalization
    Y = Y[range(int(n/2))]

    return (Y,frq)


def usun_dane_z_przedzialu(od,do,lista):
    del(lista[od:do])

def wykresy_timestamp(czas,dane):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)

    fig, ax = plt.subplots(3, 2)
    ax[0,0].plot(czas,os_x,'b')
    ax[0,0].set_xlabel('Czas [ms]')
    ax[0,0].set_ylabel('OS X')
    ax[0,0].set_title('f(t)')
    ax[1,0].plot(czas,os_y,'r') 
    ax[1,0].set_xlabel('Czas [ms]')
    ax[1,0].set_ylabel('OS Y')
    ax[2,0].plot(czas,os_z,'g') 
    ax[2,0].set_xlabel('Czas [ms]')
    ax[2,0].set_ylabel('OS Z')
    
    (fft_sygnalu,czestotliwosc) = FFT_sygnalu(os_x)
    ax[0,1].plot(czestotliwosc[1:],abs(fft_sygnalu[1:]),'b')
    ax[0,1].set_xlabel('f')
    ax[0,1].set_ylabel('OS X')
    ax[0,1].set_title('FFT - bez DC')
    (fft_sygnalu,czestotliwosc) = FFT_sygnalu(os_y)
    ax[1,1].plot(czestotliwosc[1:],abs(fft_sygnalu[1:]),'r') 
    ax[1,1].set_xlabel('f')
    ax[1,1].set_ylabel('OS Y')
    (fft_sygnalu,czestotliwosc) = FFT_sygnalu(os_y)
    ax[2,1].plot(czestotliwosc[1:],abs(fft_sygnalu[1:]),'g') 
    ax[2,1].set_xlabel('f')
    ax[2,1].set_ylabel('OS Z')


    plt.show()


def wykresy_probki(dane,ile_probek = -1):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)

    indeks_poczatkowy = 0
    indeks_koncowy = len(os_x)
    
    liczba_probek = list(range(len(os_x)))
    if ile_probek != -1 :
        srodek = len(liczba_probek) //2
        liczba_probek = liczba_probek[srodek : srodek + ile_probek]
        indeks_poczatkowy = srodek
        indeks_koncowy = srodek + ile_probek
    
    fig, ax = plt.subplots(3, 2)
    ax[0,0].plot(liczba_probek,os_x[indeks_poczatkowy : indeks_koncowy],'b')
    ax[0,0].set_xlabel('Probka')
    ax[0,0].set_ylabel('OS X')
    ax[0,0].set_title('f(t)')
    ax[1,0].plot(liczba_probek,os_y[indeks_poczatkowy : indeks_koncowy],'r') 
    ax[1,0].set_xlabel('Probka')
    ax[1,0].set_ylabel('OS Y')
    ax[2,0].plot(liczba_probek,os_z[indeks_poczatkowy : indeks_koncowy],'g') 
    ax[2,0].set_xlabel('Probka')
    ax[2,0].set_ylabel('OS Z')
    
    (fft_sygnalu,czestotliwosc) = FFT_sygnalu(os_x)
    ax[0,1].plot(czestotliwosc[1:],abs(fft_sygnalu[1:]),'b')
    ax[0,1].set_xlabel('f')
    ax[0,1].set_ylabel('OS X')
    ax[0,1].set_title('FFT - bez DC')
    (fft_sygnalu,czestotliwosc) = FFT_sygnalu(os_y)
    ax[1,1].plot(czestotliwosc[1:],abs(fft_sygnalu[1:]),'r') 
    ax[1,1].set_xlabel('f')
    ax[1,1].set_ylabel('OS Y')
    (fft_sygnalu,czestotliwosc) = FFT_sygnalu(os_y)
    ax[2,1].plot(czestotliwosc[1:],abs(fft_sygnalu[1:]),'g') 
    ax[2,1].set_xlabel('f')
    ax[2,1].set_ylabel('OS Z')

    plt.show()

def wykresy(decyzja,czas,dane):
    while(True):
        print("WYKRESY:\n")
        decyzja = input("1.TIMESTAMP\n2.NUMER PROBKI\n3.N srodkowych probek \nELSE - wyjscie\n")
        if decyzja == '1' :
            wykresy_timestamp(czas,dane)
        elif decyzja == '2':
            wykresy_probki(dane)
        elif decyzja == '3':
            wykresy_probki(dane,int(input("Ile probek? ")))
        else :
            break
    


def obrobka_danych_z_pliku(nazwa_pliku):
    """ Wczytujemy dane z plikow i je analizujemy"""
    with ( open(nazwa_pliku,"r")) as plik:
        typ_pliku = 0
        if(plik.name.find("Accelerometer.csv") != (-1)):
            typ_pliku = "a_"
        elif (plik.name.find("Gyroscope.csv") != (-1)):
            typ_pliku = "z_"
        else:
            typ_pliku = 0
            print("Bledna nazwa pliku " + nazwa_pliku)
        if typ_pliku != 0 :
            print("Plik " + nazwa_pliku + " pomyslnie otwarty\n Analizujemy?\n")
            decyzja = input("t/n\n")
            if decyzja =='t' :
                dane, czas = f.wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku,1) # etykieta nie jest tutaj wazna
                dane,czas = np.asarray(dane).astype('float32') , np.asarray(czas).astype('float32')
                print("Dane pomyslnie wczytane. Co teraz?\n")
                while(True):
                    print("Co chcesz zrobic?\n")
                    decyzja = input("1.Wykresy\nq - wyjscie\n")
                    if decyzja =='1' : wykresy(decyzja,czas,dane)
                    #elif decyzja =='2' : 
                    elif decyzja =="q" : break
                    else : print("BLAD!")
                

################################################################################

#nazwa_pliku = "Bieg2_Accelerometer.csv" # input("Podaj nazwe pliku: ")

#obrobka_danych_z_pliku(nazwa_pliku)

with os.scandir(os.curdir) as katalog_roboczy:
        for plik in katalog_roboczy:
            if(plik.name.find(".csv") == (-1)):
               continue # TYLKO PLIKI CSV
            print("Plik : " + plik.name + "\n")
            print("1. Analiza pliku\n2. Pomin ten plik\nq - zamknij skrypt\n")
            odpowiedz = input()
            if odpowiedz == '1' :
                obrobka_danych_z_pliku(plik.name)
            elif odpowiedz == '2':
                continue
            else :
                break
