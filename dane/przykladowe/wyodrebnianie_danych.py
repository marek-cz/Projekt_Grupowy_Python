""" Skrypt majacy na celu wyodrebnienie poprawnych danych z plikow csv
    Chodzi o sytuacje w ktorej np. wlaczymy czujniki a jeszcze przez
    2 sekundy stoimy w miejscu a potem zaczynamy bieganie
    Czlowiek ocenia poprawnosc danych..."""

# import bibliotek

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os # biblioteka do poruszania sie w systemie plikow
import funkcje as f
from scipy.signal import kaiserord, lfilter, firwin, freqz

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


def wykresy_probki_FFT(dane,ile_probek = -1,osie_juz_podzielone = False,x = None,y = None ,z = None):
    if not osie_juz_podzielone :
        os_x = f.wyodrebnij_os_z_tablicy(dane,0)
        os_y = f.wyodrebnij_os_z_tablicy(dane,1)
        os_z = f.wyodrebnij_os_z_tablicy(dane,2)
    else :
        os_x = x
        os_y = y
        os_z = z
    
    dane_do_wykresu = [os_x,os_y,os_z]
    dziedzina = [list( range( len( os_x ) ) ),list( range( len( os_y ) ) ),list( range( len( os_z ) ) )]

    for i in range(3):
        (fft_sygnalu,czestotliwosc) = FFT_sygnalu(dane_do_wykresu[i])
        modul_fft_sygnalu = abs(fft_sygnalu)
        dane_do_wykresu.append(modul_fft_sygnalu[1:])
        dziedzina.append(czestotliwosc[1:])

    if ile_probek != (-1):
        dlugosc_os_x = len(os_x)
        dane_do_wykresu[0] = os_x[ dlugosc_os_x//2 : (dlugosc_os_x//2) + ile_probek ]
        dane_do_wykresu[1] = os_y[ dlugosc_os_x//2 : (dlugosc_os_x//2) + ile_probek ]
        dane_do_wykresu[2] = os_z[ dlugosc_os_x//2 : (dlugosc_os_x//2) + ile_probek ]
        dziedzina[0] = list( range((dlugosc_os_x//2),(dlugosc_os_x//2) + ile_probek  ) )
        dziedzina[1] = list( range((dlugosc_os_x//2),(dlugosc_os_x//2) + ile_probek  ) )
        dziedzina[2] = list( range((dlugosc_os_x//2),(dlugosc_os_x//2) + ile_probek  ) )
    
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
        ax[i,0].plot(dziedzina[i][indeks_poczatkowy : indeks_koncowy],dane[i][indeks_poczatkowy : indeks_koncowy],'b')
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
        ax[i,1].plot(dziedzina[i+3][indeks_poczatkowy : indeks_koncowy],dane[i+3][indeks_poczatkowy : indeks_koncowy],'r')
        ax[i,1].set_xlabel(x_label[i+3])
        ax[i,1].set_ylabel(y_label[i+3])
    ax[0,1].set_title(tytuly[1])

    plt.show()

def spektrogram(dane,fs):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)

    os_x = np.asarray(os_x).astype('float32')
    os_y = np.asarray(os_y).astype('float32')
    os_z = np.asarray(os_z).astype('float32')

    sygnaly = [os_x,os_y,os_z]
    
    spektrogramy = []
    frq = 0
    t = 0
    
    for i in range(3):
        frq, t, Sxx = signal.spectrogram(sygnaly[i], fs)
        spektrogramy.append(Sxx)

    fig, ax = plt.subplots(3, 2)
    ax[0,0].plot(list( range( len( os_x ))), os_x ,'b')
    ax[0,0].set_xlabel('Czas [ms]')
    ax[0,0].set_ylabel('X')
    ax[0,0].set_title('SYGNALY')
    ax[1,0].plot(list( range( len( os_x ))), os_y ,'b')
    ax[1,0].set_xlabel('Czas [ms]')
    ax[1,0].set_ylabel('Y')
    ax[2,0].plot(list( range( len( os_x ))), os_z ,'b')
    ax[2,0].set_xlabel('Czas [ms]')
    ax[2,0].set_ylabel('Z')
    ax[0,1].pcolormesh(t, frq, spektrogramy[0] )
    ax[0,1].set_xlabel('Czas [ms]')
    ax[0,1].set_ylabel('Czestotliwosc [Hz]')
    ax[0,1].set_title('SPEKTROGRAMY')
    ax[1,1].pcolormesh(t, frq, spektrogramy[1] )
    ax[1,1].set_xlabel('Czas [ms]')
    ax[1,1].set_ylabel('Czestotliwosc [Hz]')
    ax[2,1].pcolormesh(t, frq, spektrogramy[2] )
    ax[2,1].set_xlabel('Czas [ms]')
    ax[2,1].set_ylabel('Czestotliwosc [Hz]')

    plt.show()

def wczytanie_danych_z_dwoch_plikow(nazwa_pliku_akc,nazwa_pliku_gyr):
    dane_akc,czas = f.wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_akc,1) # etykieta nie jest tutaj wazna
    dane_akc = np.asarray(dane_akc).astype('float32')

    dane_gyr,czas = f.wczytaj_dane_z_pliku_csv_Timestamp(nazwa_pliku_gyr,1) # etykieta nie jest tutaj wazna
    dane_gyr = np.asarray(dane_gyr).astype('float32')
    
    os_x_akc,os_y_akc,os_z_akc = osie_z_danych_np_float32(dane_akc)
    os_x_gyr,os_y_gyr,os_z_gyr = osie_z_danych_np_float32(dane_gyr)
    
    return [os_x_akc,os_y_akc,os_z_akc,os_x_gyr,os_y_gyr,os_z_gyr]

def analza_statystyczna(nazwa_pliku_akc,nazwa_pliku_gyr,etykieta_pliku):
    dane_z_plikow = wczytanie_danych_z_dwoch_plikow(nazwa_pliku_akc,nazwa_pliku_gyr)
    opisy_osi = ["os_x_akc : " ,"os_y_akc : ","os_z_akc : ","os_x_gyr: ","os_y_gyr: ","os_z_gyr: "]
    print(etykieta_pliku + " ANALIZA PARAMETROW STATYSTYCZNYCH: \n")
    
    # wartosci srednie:
    print("1. Wartosci srednie :")
    for i in range( len(dane_z_plikow) ):
        print(opisy_osi[i] + str(np.mean(dane_z_plikow[i])))

    # Odchylenie std:
    print("2.Odchylenie standardowe:")
    for i in range( len(dane_z_plikow) ):
        print(opisy_osi[i] + str(np.std(dane_z_plikow[i])))
    # Wariancja:
    print("3 Wariancja:")
    for i in range( len(dane_z_plikow) ):
        print(opisy_osi[i] + str(np.var(dane_z_plikow[i])))
    # Mediana:
    print("4.Mediana:")
    for i in range( len(dane_z_plikow) ):
        print(opisy_osi[i] + str(np.median(dane_z_plikow[i])))

    # Czestotliwosc najwiekszego piku (bez DC!!!):
    print("Czestotliwosc maksymalnego piku :")
    for i in range( len(dane_z_plikow) ):
        fft_sygnalu, frq = FFT_sygnalu(dane_z_plikow[i])
        modul_fft = np.abs(fft_sygnalu[1:])
        maks_pik = max(modul_fft)
        indeks_maks_pik = np.where(modul_fft == maks_pik)
        frq = frq[1:]
        print(opisy_osi[i] + str( frq[indeks_maks_pik] ) + " Hz" )


def projekt_filtru_cyfrowego(fs,szerokosc_pasma_przejsciowego_Hz, czestotliwosc_odciecia_Hz,tlumienie_w_pasmie_zaporowym_db):
    # PARAMETRY FILTRU
    czestotliwosc_NYQ = fs / 2.0
    szerokosc_pasma_przejsciowego = szerokosc_pasma_przejsciowego_Hz / czestotliwosc_NYQ # 5 Hz

    N, beta = kaiserord(tlumienie_w_pasmie_zaporowym_db, szerokosc_pasma_przejsciowego) # wyznaczenmie parametrow filtru Kaisera
    
    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    wspolczynniki = firwin(N,czestotliwosc_odciecia_Hz/czestotliwosc_NYQ , window=('kaiser', beta))

    return wspolczynniki

def osie_z_danych_np_float32(dane):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)

    os_x = np.asarray(os_x).astype('float32')
    os_y = np.asarray(os_y).astype('float32')
    os_z = np.asarray(os_z).astype('float32')

    return (os_x,os_y,os_z)

def fitracja_cyfrowa(dane,fs,szerokosc_pasma_przejsciowego_Hz, czestotliwosc_odciecia_Hz,tlumienie_w_pasmie_zaporowym_db):
    wspolczynniki_filtru = projekt_filtru_cyfrowego(fs,szerokosc_pasma_przejsciowego_Hz, czestotliwosc_odciecia_Hz,tlumienie_w_pasmie_zaporowym_db)

    os_x,os_y,os_z = osie_z_danych_np_float32(dane)
    
    #FILTRACJA:
    filtered_x = lfilter(wspolczynniki_filtru, 1.0, os_x)
    filtered_y = lfilter(wspolczynniki_filtru, 1.0, os_y)
    filtered_z = lfilter(wspolczynniki_filtru, 1.0, os_z)

    return (filtered_x,filtered_y,filtered_z)
    
def wykresy_filtracja_cyfrowa(dane,fs,szerokosc_pasma_przejsciowego_Hz, czestotliwosc_odciecia_Hz,tlumienie_w_pasmie_zaporowym_db):
    decyzja = input("1.Wykresy czasowe + widmo\n2.Porownanie wykresow czasowych\n ")
    if decyzja == '1' :
        x,y,z = fitracja_cyfrowa(dane,fs,szerokosc_pasma_przejsciowego_Hz, czestotliwosc_odciecia_Hz,tlumienie_w_pasmie_zaporowym_db)
        wykresy_probki_FFT(dane,osie_juz_podzielone=True,x=x,y=y,z=z)
    elif decyzja == '2' :
        x_f,y_f,z_f = fitracja_cyfrowa(dane,fs,szerokosc_pasma_przejsciowego_Hz, czestotliwosc_odciecia_Hz,tlumienie_w_pasmie_zaporowym_db) # dane po filtracji
        x_o,y_o,z_o = osie_z_danych_np_float32(dane) # dane oryginalne

        dane_do_wykresu = [x_o,y_o,z_o,x_f,y_f,z_f]
        dziedzina = [list( range( len( x_o ) ) ),list( range( len( y_o ) ) ),list( range( len( z_o ) ) ),list( range( len(x_f ) ) ),list( range( len( y_f ) ) ),list( range( len( z_f ) ) )]
        x_label = ["Probki","Probki","Probki","Probki","Probki","Probki"]
        y_label = ["OS X","OS Y","OS Z","OS X","OS Y","OS Z"]
        tytuly = ["PRZED FILTRACJA","PO FILTRACJI"]

        rysuj_wykres_3_na_2(dane_do_wykresu, dziedzina ,x_label,y_label, tytuly, ile_probek = 300)
        
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
                print("1.Wykresy czas i FFT\n2.Wykresy czasowe akcelerometr i zyroskop")
                print("3.Spektrogram\n4.Filtracja cyfrowa\n")
                decyzja = input("q - wyjscie\n")
                if decyzja =='1' : wykresy_FFT(decyzja,czas,dane)
                elif decyzja =='2' :
                    wykresy_2_pliki(nazwa_pliku,typ_pliku,dane)
                elif decyzja =='3' :
                    spektrogram(dane,100)
                elif decyzja =='4' :
                    wykresy_filtracja_cyfrowa(dane,100,2.0,12.0,60)
                elif decyzja =="q" : break
                else : print("BLAD!")
                

################################################################################


if int(input("Analiza statystyczna WSZYSTKICH plikow? 0 - nie")) :
    lista_przetworzonych_plikow = [] # lista na nazwy plikow ktore byly juz przetwarzane
    oznaczenie_gyr = "_Gyroscope.csv"
    licznik_plikow = 0

    with os.scandir(os.curdir) as katalog_roboczy:
        for plik in katalog_roboczy:
            if(plik.name.find("Accelerometer.csv") != (-1) and not ( plik.name in lista_przetworzonych_plikow ) ) : # szukamy plikow akcelerometru, ktore nie byly jeszcze przetwarzane
                nazwa_pliku_tokeny = plik.name.split('_') # dzielimy po _
                etykieta_pliku = nazwa_pliku_tokeny[0]
                nazwa_pliku_gyr = etykieta_pliku + oznaczenie_gyr
                analza_statystyczna(plik.name,nazwa_pliku_gyr,etykieta_pliku)
                lista_przetworzonych_plikow.append(plik.name)
                licznik_plikow += 1

    print("\n")
    print(licznik_plikow)
    print("\n\n")


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
