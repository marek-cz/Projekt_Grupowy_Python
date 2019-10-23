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

def usun_dane_z_przedzialu(od,do,lista):
    del(lista[od:do])

def wykresy_timestamp(czas,dane):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)
    warunek = True
    while (warunek):
        decyzja = input("Wybierz os: \nx\ny\nz\n")
        if decyzja =='x':
            rysuj_wykres(czas,os_x,"x")
        elif decyzja =='y':
            rysuj_wykres(czas,os_y,"y")
        elif decyzja =='z' :
            rysuj_wykres(czas,os_y,"z")
        else :
            print("Powtorz wybor osi")
            break

def wykresy_probki(dane):
    os_x = f.wyodrebnij_os_z_tablicy(dane,0)
    os_y = f.wyodrebnij_os_z_tablicy(dane,1)
    os_z = f.wyodrebnij_os_z_tablicy(dane,2)
    warunek = True
    while (warunek):
        decyzja = input("Wybierz os: \nx\ny\nz\n")
        if decyzja =='x':
            rysuj_wykres(list(range(len(os_x))),os_x,"x",x_label = 'probka')
        elif decyzja =='y':
            rysuj_wykres(list(range(len(os_x))),os_y,"y",x_label = 'probka')
        elif decyzja =='z' :
            rysuj_wykres(list(range(len(os_x))),os_y,"z",x_label = 'probka')
        else :
            print("Powtorz wybor osi")
            break

def wykresy(decyzja,czas,dane):
    while(True):
        print("WYKRESY:\n")
        decyzja = input("1.TIMESTAMP\n2.NUMER PROBKI\nELSE - wyjscie\n")
        if decyzja == '1' :
            wykresy_timestamp(czas,dane)
        elif decyzja == '2':
            wykresy_probki(dane)
        else :
            print("Nie analizujemy tego pliku !")
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

nazwa_pliku = "Bieg2_Accelerometer.csv" # input("Podaj nazwe pliku: ")

obrobka_danych_z_pliku(nazwa_pliku)
