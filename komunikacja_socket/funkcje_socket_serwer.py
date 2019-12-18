""" MODUL ZAWIERAJACY FUNKCJE I STALE WYKORZYSTYWANE W SKRYPTACH
    KLASYFIKUJACYCH DANE"""

import numpy as np

###############################################################################################
#                                       STALE
###############################################################################################
ZAKRES_AKCELEROMETR = 8000
ZAKRES_ZYROSKOP     = 2000

IP_SERWERA = '' # U serwera puste
PORT = 5005 # liczba 16-bitowa, wiekszta niz 1024
BUFOR_ROZMIAR = 4096


BIEGANIE_PROGI_ODCHYLENIA_STD = {"akc_x" : 2000, "akc_y" : 2000, "akc_z" : 2000, "gyr_x" : 2000, "gyr_y" : 300, "gyr_z" : 2000 }
MARSZ_PROGI_ODCHYLENIA_STD    = {"akc_x" : 500,  "akc_y" : 2000, "akc_z" : 500,  "gyr_x" : 2000, "gyr_y" : 100, "gyr_z" : 2000 }
TRUCHT_PROGI_ODCHYLENIA_STD   = {"akc_x" : 1300, "akc_y" : 2000, "akc_z" : 1300, "gyr_x" : 2000, "gyr_y"  : 200, "gyr_z" : 2000 }

PROGI_ODCHYLENIE_STD = {"Bieganie" : BIEGANIE_PROGI_ODCHYLENIA_STD, "Marsz" : MARSZ_PROGI_ODCHYLENIA_STD, "Trucht" : TRUCHT_PROGI_ODCHYLENIA_STD } 



wykryta_aktywnosc = ["Marsz", "Trucht", "Bieg","Stanie","Skok"]
nazwa_pliku_z_baza_danych = "plik_bazy_danych.db"
sciezka_do_modelu_klasyfikatora = "../zapis_modelu.h5"


###############################################################################################
#                                       FUNKCJE
###############################################################################################
def wyodrebnij_osie_danych_BEZ_NORMALIZACJI(lista): # [DANE] = [a_x][a_y][a_z][g_x][g_y][g_z] * Liczba_probek_w_paczce
    result = [[],[],[],[],[],[]]
    for probka in lista:
        result[0].append(probka[0] ) # AKCELEROMETR X
        result[1].append(probka[1] ) # AKCELEROMETR Y
        result[2].append(probka[2] ) # AKCELEROMETR Z
        result[3].append(probka[3] ) # ZYROSKOP X
        result[4].append(probka[4] ) # ZYROSKOP Y
        result[5].append(probka[5] ) # ZYROSKOP Z

    return result

def wyodrebnij_osie_danych_NORMALIZACJA(lista): # [DANE] = [a_x][a_y][a_z][g_x][g_y][g_z] * Liczba_probek_w_paczce
    """ WYODREBNIA OSIE DANYCH I NORMALIZUJE WZGLEDEM
        ZAKRESOW POMIAROWYCH CZUJNIKOW - KLASYFIKATOR
        NEURONOWY"""
    result = [[],[],[],[],[],[]]
    for probka in lista:
        result[0].append(probka[0] / ZAKRES_AKCELEROMETR ) # AKCELEROMETR X + NORMALIZACJA WZGLEDEM ZAKRESU
        result[1].append(probka[1] / ZAKRES_AKCELEROMETR ) # AKCELEROMETR Y
        result[2].append(probka[2] / ZAKRES_AKCELEROMETR ) # AKCELEROMETR Z
        result[3].append(probka[3] / ZAKRES_ZYROSKOP ) # ZYROSKOP X
        result[4].append(probka[4] / ZAKRES_ZYROSKOP ) # ZYROSKOP Y
        result[5].append(probka[5] / ZAKRES_ZYROSKOP ) # ZYROSKOP Z

    return result


def wyodrebnij_osie_danych_string(lista):
    result = [[],[],[],[],[],[]]
    for probka in lista:
        result[0].append(probka[0]) # AKCELEROMETR X
        result[1].append(probka[1]) # AKCELEROMETR Y
        result[2].append(probka[2]) # AKCELEROMETR Z
        result[3].append(probka[3]) # ZYROSKOP X
        result[4].append(probka[4]) # ZYROSKOP Y
        result[5].append(probka[5]) # ZYROSKOP Z

    return result


def normalizuj(x): # dokladniej standaryzacja - wartosc srednia 0 i odchylenie standardowe 1
    srednie = x.mean(axis=1)
    for i in range(x.shape[0]):
        x[i] -= srednie[i]
    odchylenia_std = x.std(axis=1)
    for i in range(x.shape[0]):
        x[i] /= odchylenia_std[i]

def lista_stringow_na_liste_probek(lista_stringow):
    result = []
    rekord = []
    licznik = 0
    for string in lista_stringow:
        #napis = str(licznik) + ". String : " + str(string)
        rekord.append(string)
        #print(napis)
        licznik += 1
        if licznik == 7 :
            licznik = 0
            result.append(rekord)
            rekord = []
            #print(result)

    return result

def usun_timestamp(lista_probek_timestamp):
    result = []
    for probka in lista_probek_timestamp:
        result.append(probka[1:])
    return result


def klasyfikacja_odchylenie_std(probka_danych):
    odchylenia_std_osi = []
    for os in probka_danych:
        odchylenia_std_osi.append(os.std())
        print(odchylenia_std_osi)
    if (odchylenia_std_osi[0] >= PROGI_ODCHYLENIE_STD['Bieganie']['akc_x']) or (odchylenia_std_osi[2] >= PROGI_ODCHYLENIE_STD['Bieganie']['akc_z']) or (odchylenia_std_osi[4] >= PROGI_ODCHYLENIE_STD['Bieganie']['gyr_y']):
        return 2 # indeks biegania
    elif (odchylenia_std_osi[0] >= PROGI_ODCHYLENIE_STD['Trucht']['akc_x']) or (odchylenia_std_osi[2] >= PROGI_ODCHYLENIE_STD['Trucht']['akc_z']) or (odchylenia_std_osi[4] >= PROGI_ODCHYLENIE_STD['Trucht']['gyr_y']):
        return 1 # indeks truchtu
    elif (odchylenia_std_osi[0] >= PROGI_ODCHYLENIE_STD['Marsz']['akc_x']) or (odchylenia_std_osi[2] >= PROGI_ODCHYLENIE_STD['Marsz']['akc_z']) or (odchylenia_std_osi[4] >= PROGI_ODCHYLENIE_STD['Marsz']['gyr_y']):
        return 1 # indeks marszu
    else :
        return 3 # indeks stania


def lista_stringow_na_probke(lista_danych, zamien_na_float = True):
    """ Na podstawie listy stringow formuje probke danych do modelu
        sieci neuronowej. Zwraca probke (macierz numpy) i dane z
        czujnikow w formie listy stringow"""
    lista_probek_timestamp = lista_stringow_na_liste_probek(lista_danych)
    lista_probek_timestamp.sort() # sortujemy po Timestamp
    lista_posortowanych_probek = usun_timestamp(lista_probek_timestamp) # usuwamy timestamp
    dane_osie_string = wyodrebnij_osie_danych_string(lista_posortowanych_probek) # podzial probek na osie czujnikow - do zapisu
    if zamien_na_float:
        #try :
        lista_posortowanych_probek_float = np.asarray(lista_posortowanych_probek).astype('float32') # przechodzimy na floaty
        #except ValueError as zmienna1:
        #    print("Blad konwersji  string - float!")
        dane_osie = wyodrebnij_osie_danych_NORMALIZACJA(lista_posortowanych_probek_float) # podzial probek na osie czujnikow
        probka = np.asarray(dane_osie).astype('float32')
        shape = probka.shape
        probka = probka.reshape(1,shape[0]*shape[1])
    else :
        probka = "Blad"


    return (probka,dane_osie_string)

def lista_stringow_na_probke_BEZ_NORMALIZACJI(lista_danych):
    lista_probek_timestamp = lista_stringow_na_liste_probek(lista_danych)
    lista_probek_timestamp.sort() # sortujemy po Timestamp
    lista_posortowanych_probek = usun_timestamp(lista_probek_timestamp) # usuwamy timestamp
    try :
        lista_posortowanych_probek_float = np.asarray(lista_posortowanych_probek).astype('float32') # przechodzimy na floaty
    except ValueError as zmienna1:
        print("Blad konwersji  string - float!\n")
        print(lista_posortowanych_probek)
    dane_osie = wyodrebnij_osie_danych_BEZ_NORMALIZACJI(lista_posortowanych_probek_float) # podzial probek na osie czujnikow
    probka = np.asarray(dane_osie).astype('float32')
    #print(probka)

    dane_osie_string = wyodrebnij_osie_danych_string(lista_posortowanych_probek) # podzial probek na osie czujnikow - do zapisu

    return (probka,dane_osie_string)

#####################################################################################

def SPLOTOWA_normalizacja(macierz_probek):
    for probka in macierz_probek:
        probka[0] /= ZAKRES_AKCELEROMETR
        probka[1] /= ZAKRES_AKCELEROMETR
        probka[2] /= ZAKRES_AKCELEROMETR
        
        probka[3] /= ZAKRES_ZYROSKOP
        probka[4] /= ZAKRES_ZYROSKOP
        probka[5] /= ZAKRES_ZYROSKOP

#######################################################################################

def SPLOTOWA_lista_stringow_na_probke(lista_danych, zamien_na_float = True):
    lista_probek_timestamp = lista_stringow_na_liste_probek(lista_danych)
    lista_probek_timestamp.sort() # sortujemy po Timestamp
    lista_posortowanych_probek = usun_timestamp(lista_probek_timestamp) # usuwamy timestamp
    dane_osie_string = wyodrebnij_osie_danych_string(lista_posortowanych_probek) # podzial probek na osie czujnikow - do zapisu

    poprawnosc = True
    
    if zamien_na_float:
        try :
            probka = np.asarray(lista_posortowanych_probek).astype('float32') # przechodzimy na floaty
            SPLOTOWA_normalizacja(probka)
            shape = probka.shape
            probka = probka.reshape(1,shape[0],shape[1])
        except ValueError as zmienna1:
            print("Blad konwersji  string - float!")
            probka = 0
            poprawnosc = False
        
    else :
        probka = 0
        poprawnosc = False
        
    return (poprawnosc,probka,dane_osie_string)
   
        
