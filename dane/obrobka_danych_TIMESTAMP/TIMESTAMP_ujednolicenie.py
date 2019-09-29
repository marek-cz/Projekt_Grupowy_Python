

def timestamp_ogarnij(nazwa_pliku_akc, nazwa_pliku_gyr,offset = 4):
    """ Pobiera dane TIMESTAMP  z pliku akcelerometru i szuka tego
        samego timestampu w pliku gyro
        w wyniku dzialania funkcji otrzymujemy 2 nowe pliki:
        - akcelerometr
        - zyroskop
        w ktorych TIMESTAMP JEST IDENTYCZNY!!!"""
    with ( open(nazwa_pliku_akc,"r")) as plik_akc_old , open("./nowe_pliki_csv/"+nazwa_pliku_akc,"w") as plik_akc_new,open("./nowe_pliki_csv/"+nazwa_pliku_gyr,"w") as plik_gyr_new :
        licznik_linii = 0
        for linia in plik_akc_old:
            licznik_linii += 1
            if licznik_linii > offset :
                linia_tokeny = linia.split(',') # dzielimy stringa po ','
                timestamp_akc = linia_tokeny[-6:-5] # timestamp akcelerometru
                with open(nazwa_pliku_gyr,"r") as plik_gyr_old:
                    licznik_linii_gyr = 0
                    for linia_gyr in plik_gyr_old:
                        licznik_linii_gyr += 1
                        if licznik_linii_gyr > offset :
                            linia_gyr_tokeny = linia_gyr.split(',') # dzielimy stringa po ','
                            timestamp_gyr = linia_gyr_tokeny[-6:-5] # timestamp akcelerometru
                            if (timestamp_akc == timestamp_gyr):
                                plik_akc_new.write(linia)
                                plik_gyr_new.write(linia_gyr)
                                break # wychodzimy z pliku zyroskopu - timestamp moze sie zgadzac tylko raz :)
            else :
                plik_akc_new.write(linia)
                plik_gyr_new.write(linia)

import os

lista_przetworzonych_plikow = [] # lista na nazwy plikow ktore byly juz przetwarzane
oznaczenie_gyr = "_Gyroscope.csv"

with os.scandir(os.curdir) as katalog_roboczy:
    for plik in katalog_roboczy:
        if(plik.name.find("Accelerometer.csv") != (-1) and not ( plik.name in lista_przetworzonych_plikow ) ) : # szukamy plikow akcelerometru, ktore nie byly jeszcze przetwarzane
            print(plik.name)
            nazwa_pliku_tokeny = plik.name.split('_') # dzielimy po _
            etykieta_pliku = nazwa_pliku_tokeny[0]
            nazwa_pliku_gyr = etykieta_pliku + oznaczenie_gyr
            timestamp_ogarnij(plik.name, nazwa_pliku_gyr) # ogarniamy timestamp :)
            lista_przetworzonych_plikow.append(plik.name) 
