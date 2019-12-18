# WCZYTANIE DANYCH Z PLIKU
import numpy as np
import matplotlib.pyplot as plt
import funkcje # wlasny modul z funkcjami

ZAKRES_AKCELEROMETRU = 8000
ZAKRES_ZYROSKOPU     = 2000

##############################################################################################
liczba_probek_w_paczce = int(input("Podaj liczbe probek w paczce danych : "))
##############################################################################################
#       ETYKIETY DANYCH :
slownik_etykiet_danych = { "Marsz" : 0, "Trucht" : 1, "Bieg" : 2 ,"Stanie" : 3,"Skok" : 4}
################################################################################################


(dane_akcelerometr , dane_zyroskop) = funkcje.wczytaj_dane_z_plikow(liczba_probek_w_paczce, slownik_etykiet_danych) # wczytuje dane z plikow csv w folderze roboczym

# PRZEKSZTALCENIE DANYCH ZE STRINGOW NA LICZBY + NORMALIZACJA WZGLEDEM ZAKRESU POMIAROWEGO

akcelerometr_x = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_akcelerometr,0)).astype('float32') / ZAKRES_AKCELEROMETRU
akcelerometr_y = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_akcelerometr,1)).astype('float32') / ZAKRES_AKCELEROMETRU
akcelerometr_z = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_akcelerometr,2)).astype('float32') / ZAKRES_AKCELEROMETRU

zyroskop_x = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_zyroskop,0)).astype('float32') / ZAKRES_ZYROSKOPU
zyroskop_y = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_zyroskop,1)).astype('float32') / ZAKRES_ZYROSKOPU
zyroskop_z = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_zyroskop,2)).astype('float32') / ZAKRES_ZYROSKOPU

##########################################################################################################################################

liczba_probek = len(dane_akcelerometr) // liczba_probek_w_paczce

etykiety = np.zeros((liczba_probek,))
dane = np.zeros((liczba_probek,6,liczba_probek_w_paczce))

licznik = 0
while(licznik < liczba_probek):
    dane[licznik][0] = akcelerometr_x[licznik * liczba_probek_w_paczce : (licznik + 1) * liczba_probek_w_paczce]
    dane[licznik][1] = akcelerometr_y[licznik * liczba_probek_w_paczce : (licznik + 1) * liczba_probek_w_paczce]
    dane[licznik][2] = akcelerometr_z[licznik * liczba_probek_w_paczce : (licznik + 1) * liczba_probek_w_paczce]
    
    dane[licznik][3] = zyroskop_x[licznik * liczba_probek_w_paczce : (licznik + 1) * liczba_probek_w_paczce]
    dane[licznik][4] = zyroskop_y[licznik * liczba_probek_w_paczce : (licznik + 1) * liczba_probek_w_paczce]
    dane[licznik][5] = zyroskop_z[licznik * liczba_probek_w_paczce : (licznik + 1) * liczba_probek_w_paczce]
    #print('Licznik : ',licznik,'\n')
    etykiety[licznik] = dane_akcelerometr[licznik *liczba_probek_w_paczce][3]
    licznik += 1

# WYROWNANIE LICZBY DANYCH DLA KAZDEJ AKTYWNOSCI:

dane , etykiety = funkcje.wyrownaj_liczbe_danych(dane,etykiety,slownik_etykiet_danych)

ksztalt_danych = dane.shape
liczba_probek  = ksztalt_danych[0]
# LOSOWANIE KOLEJNOSCI PROBEK

kolejnosc = np.arange(0,liczba_probek,1)
np.random.shuffle(kolejnosc)

labels = np.zeros((liczba_probek,))
data = np.zeros((liczba_probek,6,liczba_probek_w_paczce))
funkcje.ustaw_w_zadanej_kolejnosci(kolejnosc,etykiety,labels,liczba_probek)
funkcje.ustaw_w_zadanej_kolejnosci(kolejnosc,dane, data, liczba_probek)

# zapisanie do plikow:
np.save("../data_Socik",data)
np.save("../labels_Socik",labels)
