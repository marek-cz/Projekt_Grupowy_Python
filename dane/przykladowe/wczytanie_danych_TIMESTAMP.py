# WCZYTANIE DANYCH Z PLIKU
import numpy as np
import matplotlib.pyplot as plt
import funkcje # wlasny modul z funkcjami
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
################################################################################################


#dane_akcelerometr = marsz1_akc + trucht2_akc + trucht1_akc + marsz2_akc + marsz3_akc  + bieg1_akc + bieg2_akc + trucht3_akc + trucht4_akc
#dane_zyroskop     = marsz1_gyr + trucht2_gyr + trucht1_gyr + marsz2_gyr + marsz3_gyr  + bieg1_gyr + bieg2_gyr + trucht3_gyr + trucht4_gyr

(dane_akcelerometr , dane_zyroskop) = funkcje.wczytaj_dane_z_plikow() # wczytuje dane z plikow csv w folderze roboczym

# PRZEKSZTALCENIE DANYCH ZE STRINGOW NA LICZBY

akcelerometr_x = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_akcelerometr,0)).astype('float32')
akcelerometr_y = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_akcelerometr,1)).astype('float32')
akcelerometr_z = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_akcelerometr,2)).astype('float32')

zyroskop_x = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_zyroskop,0)).astype('float32')
zyroskop_y = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_zyroskop,1)).astype('float32')
zyroskop_z = np.asarray(funkcje.wyodrebnij_os_z_tablicy(dane_zyroskop,2)).astype('float32')


# NORMALIZACJA ???
if normalizacja :
    funkcje.normalizuj(akcelerometr_x)
    funkcje.normalizuj(akcelerometr_y)
    funkcje.normalizuj(akcelerometr_z)
    funkcje.normalizuj(zyroskop_x)
    funkcje.normalizuj(zyroskop_y)
    funkcje.normalizuj(zyroskop_z)


liczba_probek = len(dane_akcelerometr) // (klasyfikuj_co_n_s * fs)

etykiety = np.zeros((liczba_probek,))
dane = np.zeros((liczba_probek,6,klasyfikuj_co_n_s * fs))

licznik = 0
while(licznik < liczba_probek):
    dane[licznik][0] = akcelerometr_x[licznik *klasyfikuj_co_n_s * fs : (licznik + 1)*klasyfikuj_co_n_s * fs]
    dane[licznik][1] = akcelerometr_y[licznik *klasyfikuj_co_n_s * fs : (licznik + 1)*klasyfikuj_co_n_s * fs]
    dane[licznik][2] = akcelerometr_z[licznik *klasyfikuj_co_n_s * fs : (licznik + 1)*klasyfikuj_co_n_s * fs]
    dane[licznik][3] = zyroskop_x[licznik *klasyfikuj_co_n_s * fs : (licznik + 1)*klasyfikuj_co_n_s * fs]
    dane[licznik][4] = zyroskop_y[licznik *klasyfikuj_co_n_s * fs : (licznik + 1)*klasyfikuj_co_n_s * fs]
    dane[licznik][5] = zyroskop_z[licznik *klasyfikuj_co_n_s * fs : (licznik + 1)*klasyfikuj_co_n_s * fs]
    #print('Licznik : ',licznik,'\n')
    etykiety[licznik] = dane_akcelerometr[licznik *klasyfikuj_co_n_s * fs][3]
    licznik += 1

# LOSOWANIE KOLEJNOSCI PROBEK

kolejnosc = np.arange(0,liczba_probek,1)
np.random.shuffle(kolejnosc)

labels = np.zeros((liczba_probek,))
data = np.zeros((liczba_probek,6,klasyfikuj_co_n_s * fs))
funkcje.ustaw_w_losowej_kolejnosci(kolejnosc,etykiety,labels,liczba_probek)
funkcje.ustaw_w_losowej_kolejnosci(kolejnosc,dane, data, liczba_probek)

# zapisanie do plikow:
np.save("data",data)
np.save("labels",labels)
