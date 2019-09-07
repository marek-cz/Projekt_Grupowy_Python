# WCZYTANIE DANYCH Z PLIKU
import numpy as np
import matplotlib.pyplot as plt
plik_akcelerometr = "Accelerometer.csv"
plik_zyroskop = "Gyroscope.csv"
dane_akcelerometr = []
dane_zyroskop = []
offset = 4

#normalizacja = False
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
    
################################################################################################

dane_akcelerometr = wczytaj_dane_z_pliku_csv(plik_akcelerometr,offset,1.)
dane_zyroskop = wczytaj_dane_z_pliku_csv(plik_zyroskop,offset,1.)



bieg1_akc = wczytaj_dane_z_pliku_csv_Timestamp('Bieg1_Accelerometer.csv',offset,bieg)         # 311 - nic nie usuwac
bieg1_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Bieg1_Gyroscope.csv',offset,bieg)             # 312
usun_ostatnie_N_rekordow(bieg1_gyr,1)
dopasuj_rozmiar_listy(bieg1_akc)
dopasuj_rozmiar_listy(bieg1_gyr)

bieg2_akc = wczytaj_dane_z_pliku_csv_Timestamp('Bieg2_Accelerometer.csv',offset,bieg)         
bieg2_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Bieg2_Gyroscope.csv',offset,bieg)              

dopasuj_rozmiar_listy(bieg2_akc)    # 7384
dopasuj_rozmiar_listy(bieg2_gyr)    # 7384

marsz1_akc = wczytaj_dane_z_pliku_csv_Timestamp('Marsz1_Accelerometer.csv',offset,marsz)      # 727 - nie usuwac, tylko wyrownac
usun_ostatnie_N_rekordow(marsz1_akc,1)
marsz1_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Marsz1_Gyroscope.csv',offset,marsz)          # 726
dopasuj_rozmiar_listy(marsz1_akc)
dopasuj_rozmiar_listy(marsz1_gyr)

marsz2_akc = wczytaj_dane_z_pliku_csv_Timestamp('Marsz2_Accelerometer.csv',offset,marsz)      # 28878 - 
marsz2_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Marsz2_Gyroscope.csv',offset,marsz)          # 28878
dopasuj_rozmiar_listy(marsz2_akc)
dopasuj_rozmiar_listy(marsz2_gyr)

marsz3_akc = wczytaj_dane_z_pliku_csv_Timestamp('Marsz3_Accelerometer.csv',offset,marsz)      # 48165
marsz3_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Marsz3_Gyroscope.csv',offset,marsz)          # 48165
dopasuj_rozmiar_listy(marsz3_akc)
dopasuj_rozmiar_listy(marsz3_gyr)

trucht1_akc = wczytaj_dane_z_pliku_csv_Timestamp('Trucht1_Accelerometer.csv',offset,trucht)   # 1318
usun_ostatnie_N_rekordow(trucht1_akc,1)
trucht1_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Trucht1_Gyroscope.csv',offset,trucht)       # 1317
dopasuj_rozmiar_listy(trucht1_akc)
dopasuj_rozmiar_listy(trucht1_gyr)

trucht2_akc = wczytaj_dane_z_pliku_csv_Timestamp('Trucht2_Accelerometer.csv',offset,trucht)   # 3281
trucht2_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Trucht2_Gyroscope.csv',offset,trucht)       # 3281
dopasuj_rozmiar_listy(trucht2_akc)
dopasuj_rozmiar_listy(trucht2_gyr)

trucht3_akc = wczytaj_dane_z_pliku_csv_Timestamp('Trucht3_Accelerometer.csv',offset,trucht)   # 28398
usun_ostatnie_N_rekordow(trucht3_akc,1)
trucht3_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Trucht3_Gyroscope.csv',offset,trucht)       # 28397
dopasuj_rozmiar_listy(trucht3_akc)
dopasuj_rozmiar_listy(trucht3_gyr)

trucht4_akc = wczytaj_dane_z_pliku_csv_Timestamp('Trucht4_Accelerometer.csv',offset,trucht)   # 39166
trucht4_gyr = wczytaj_dane_z_pliku_csv_Timestamp('Trucht4_Gyroscope.csv',offset,trucht)       # 39166
dopasuj_rozmiar_listy(trucht4_akc)
dopasuj_rozmiar_listy(trucht4_gyr)

# LACZENIE DANYCH Z ROZNYCH PLIKOW :

dane_akcelerometr = marsz1_akc + trucht2_akc + trucht1_akc + marsz2_akc + marsz3_akc  +bieg1_akc + bieg2_akc + trucht3_akc + trucht4_akc
dane_zyroskop     = marsz1_gyr + trucht1_gyr + trucht2_gyr +marsz2_gyr + marsz3_gyr  + bieg1_gyr + bieg2_gyr + trucht3_gyr + trucht4_gyr


# PRZEKSZTALCENIE DANYCH ZE STRINGOW NA LICZBY

akcelerometr_x = np.asarray(wyodrebnij_os_z_tablicy(dane_akcelerometr,0)).astype('float32')
akcelerometr_y = np.asarray(wyodrebnij_os_z_tablicy(dane_akcelerometr,1)).astype('float32')
akcelerometr_z = np.asarray(wyodrebnij_os_z_tablicy(dane_akcelerometr,2)).astype('float32')

zyroskop_x = np.asarray(wyodrebnij_os_z_tablicy(dane_zyroskop,0)).astype('float32')
zyroskop_y = np.asarray(wyodrebnij_os_z_tablicy(dane_zyroskop,1)).astype('float32')
zyroskop_z = np.asarray(wyodrebnij_os_z_tablicy(dane_zyroskop,2)).astype('float32')


# NORMALIZACJA ???
if normalizacja :
    normalizuj(akcelerometr_x)
    normalizuj(akcelerometr_y)
    normalizuj(akcelerometr_z)
    normalizuj(zyroskop_x)
    normalizuj(zyroskop_y)
    normalizuj(zyroskop_z)


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
ustaw_w_losowej_kolejnosci(kolejnosc,etykiety,labels,liczba_probek)
ustaw_w_losowej_kolejnosci(kolejnosc,dane, data, liczba_probek)

# zapisanie do plikow:
np.save("data",data)
np.save("labels",labels)
