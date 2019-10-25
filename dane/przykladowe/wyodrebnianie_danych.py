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

def wykresy_timestamp_FFT(czas,dane):
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


def wykresy_probki_FFT(dane,ile_probek = -1):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)
    
    dane_do_wykresu = [os_x,os_y,os_z]
    dziedzina = [list( range( len( os_x ) ) ),list( range( len( os_y ) ) ),list( range( len( os_z ) ) )]

    for i in range(3):
        (fft_sygnalu,czestotliwosc) = FFT_sygnalu(dane_do_wykresu[i])
        modul_fft_sygnalu = abs(fft_sygnalu)
        dane_do_wykresu.append(modul_fft_sygnalu[1:])
        dziedzina.append(czestotliwosc[1:])

    x_label = ["Probki","Probki","Probki","f [Hz]","f [Hz]","f [Hz]"]
    y_label = ["OS X","OS Y","OS Z","|X|","|Y|","|Z|"]
    tytuly = ["FUNKCJA CZASU", " MODUL FFT BEZ DC"]
    rysuj_wykres_3_na_2(dane_do_wykresu,dziedzina,x_label,y_label,tytuly)


def wykresy_FFT(decyzja,czas,dane):
    while(True):
        print("WYKRESY:\n")
        decyzja = input("1.TIMESTAMP\n2.NUMER PROBKI\n3.N srodkowych probek \nELSE - wyjscie\n")
        if decyzja == '1' :
            wykresy_timestamp_FFT(czas,dane)
        elif decyzja == '2':
            wykresy_probki_FFT(dane)
        elif decyzja == '3':
            wykresy_probki_FFT(dane,int(input("Ile probek? ")))
        else :
            break
    
def wykresy_2_pliki(nazwa_pliku,typ_pliku,dane):
    dane_akc = []
    dane_gyr = []
    if typ_pliku == "Accelerometer" :
        dane_akc = dane
        nazwa_pliku_tokeny = nazwa_pliku.split('_') # dzielimy na tokeny po znaku '_'
        nazwa_drugiego_pliku = nazwa_pliku_tokeny[0] + "Gyroscope.csv"
        dane_gyr,czas = f.wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku,1) # etykieta nie jest tutaj wazna
        dane_gyr = np.asarray(dane_gyr).astype('float32')
    else :
        dane_gyr = dane
        nazwa_pliku_tokeny = nazwa_pliku.split('_') # dzielimy na tokeny po znaku '_'
        nazwa_drugiego_pliku = nazwa_pliku_tokeny[0] + "Accelerometer.csv"
        dane_akc,czas = f.wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku,1) # etykieta nie jest tutaj wazna
        dane_akc = np.asarray(dane_akc).astype('float32')
    
    os_x_akc = f.wyodrebnij_os_z_tablicy(dane_akc,0)
    os_y_akc = f.wyodrebnij_os_z_tablicy(dane_akc,1)
    os_z_akc = f.wyodrebnij_os_z_tablicy(dane_akc,2)

    
    os_x_gyr = f.wyodrebnij_os_z_tablicy(dane_gyr,0)
    os_y_gyr = f.wyodrebnij_os_z_tablicy(dane_gyr,1)
    os_z_gyr = f.wyodrebnij_os_z_tablicy(dane_gyr,2)
    
    dane_do_wykresu = [os_x_akc,os_y_akc,os_z_akc,os_x_gyr,os_y_gyr,os_z_gyr]
    print(dane_do_wykresu[5][:20])
    dziedzina = [list( range( len( os_x_akc ) ) ),list( range( len( os_y_akc ) ) ),list( range( len( os_z_akc ) ) ),list( range( len( os_x_gyr ) ) ),list( range( len( os_y_gyr ) ) ),list( range( len( os_z_gyr ) ) )]
    x_label = ["Probki","Probki","Probki","Probki","Probki","Probki"]
    y_label = ["OS X","OS Y","OS Z","OS X","OS Y","OS Z"]
    tytuly = ["AKCELEROMETR","ZYROSKOP"]

    rysuj_wykres_3_na_2(dane_do_wykresu,dziedzina,x_label,y_label,tytuly)
    
    
def rysuj_wykres_3_na_2(dane, dziedzina ,x_label,y_label, tytuly, ile_probek = -1):
    """RYSUJE WYKRES 3X2"""
    
    fig, ax = plt.subplots(3, 2)

    for i in range(3): # pierwsza kolumna
        indeks_poczatkowy = 0
        indeks_koncowy = len(dziedzina[i])
    
        liczba_probek = list(range( indeks_koncowy ) )
        if ile_probek != -1 :
            srodek = len(liczba_probek) //2
            liczba_probek = liczba_probek[srodek : srodek + ile_probek]
            indeks_poczatkowy = srodek
            indeks_koncowy = srodek + ile_probek
        ax[i,0].plot(liczba_probek,dane[i][indeks_poczatkowy : indeks_koncowy],'b')
        ax[i,0].set_xlabel(x_label[i])
        ax[i,0].set_ylabel(y_label[i])
    ax[0,0].set_title(tytuly[0])

    for i in range(3): # druga kolumna
        indeks_poczatkowy = 0
        indeks_koncowy = len(dziedzina[i+3])
    
        liczba_probek = list(range( indeks_koncowy ) )
        if ile_probek != -1 :
            srodek = len(liczba_probek) //2
            liczba_probek = liczba_probek[srodek : srodek + ile_probek]
            indeks_poczatkowy = srodek
            indeks_koncowy = srodek + ile_probek
        ax[i,1].plot(liczba_probek,dane[i+3][indeks_poczatkowy : indeks_koncowy],'r')
        ax[i,1].set_xlabel(x_label[i+3])
        ax[i,1].set_ylabel(y_label[i+3])
    ax[0,1].set_title(tytuly[1])

    plt.show()
   
def obrobka_danych_z_pliku(nazwa_pliku):
    """ Wczytujemy dane z plikow i je analizujemy"""
    with ( open(nazwa_pliku,"r")) as plik:
        typ_pliku = 0
        if(plik.name.find("Accelerometer.csv") != (-1)):
            typ_pliku = "Accelerometer"
        elif (plik.name.find("Gyroscope.csv") != (-1)):
            typ_pliku = "Gyroscope"
        else:
            typ_pliku = 0
            print("Bledna nazwa pliku " + nazwa_pliku)
        if typ_pliku != 0 :
            print("Plik " + nazwa_pliku + " pomyslnie otwarty\n\n")
            dane, czas = f.wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku,1) # etykieta nie jest tutaj wazna
            dane,czas = np.asarray(dane).astype('float32') , np.asarray(czas).astype('float32')
            print("Dane pomyslnie wczytane. Co teraz?\n")
            while(True):
                print("Co chcesz zrobic?\n")
                print("1.Wykresy czas i FFT\n2.Wykresy czasowe akcelerometr i zyroskop\n")
                decyzja = input("q - wyjscie\n")
                if decyzja =='1' : wykresy_FFT(decyzja,czas,dane)
                elif decyzja =='2' :
                    wykresy_2_pliki(nazwa_pliku,typ_pliku,dane)
                elif decyzja =="q" : break
                else : print("BLAD!")
                

################################################################################



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
