""" MODUL SERWERA KLASYFIKUJACEGO DANE ZA POMOCA SIECI NEURONOWEJ """
# KOMUNIKACJA KLIENT - SERWER
# PROCES SERWERA

import socket
import numpy as np
import funkcje_socket_serwer as funkcje # wlasny modul z funkcjami i stalymi
from keras.models import load_model
import sqlite3
import datetime
####################################################################################################################################################################
#                                       FUNKCJE - WYSOKOPOZIOMOWE 
####################################################################################################################################################################
def Klasyfikacja():
    probka , dane_osie = funkcje.lista_stringow_na_probke(ramka_danych_lista_stringow[2:-1]) # WYSYLAMY DO FUNKCJI TYLKO DANE!!!
    klasyfikacja = model.predict(probka)
    indeks_np = np.where(klasyfikacja == klasyfikacja.max()) # szukamy najbardziej prawdopodobnego wyniku
    indeks = np.asscalar(indeks_np[1])
    # odeslij wynik klasyfikacji
    odpowiedz = "Tu serwer, odebralem dane :)\nWykryta aktywnosc to :  " + funkcje.wykryta_aktywnosc[indeks] + " \n"  + str(klasyfikacja) + "\n"
    connection.send(odpowiedz.encode())
    print(odpowiedz)
    # wpisz do bazy danych
    kursor_bazy_danych.execute("insert into probki (a_x,a_y,a_z,g_x,g_y,g_z, etykieta ,czas) values(?,?,?,?,?,?,?,?)", (" ".join(dane_osie[0]), " ".join(dane_osie[1])," ".join(dane_osie[2]), " ".join(dane_osie[3])," ".join(dane_osie[4])," ".join(dane_osie[5]), funkcje.wykryta_aktywnosc[indeks] ,datetime.datetime.now() ) )
    kursor_bazy_danych.execute("insert into aktywnosc (etykieta,czas,zawodnik_id) values(?,?,?)", (funkcje.wykryta_aktywnosc[indeks],datetime.datetime.now(),int(ramka_danych_lista_stringow[1])) )
    polaczenie_z_baza_danych.commit()

def Wpis():
    print("Polecenie wpsiania do bazy danych")
    odpowiedz = "Operacja wpisania do bazy danych nie jest jeszcze gotowa"
    connection.send(odpowiedz.encode())

def Zapytanie():
    print("Zapytanie do bazy danych")
    odpowiedz = "Operacja zapytania do bazy danych nie jest jeszcze gotowa"
    connection.send(odpowiedz.encode())
#####################################################################################################################################################################

slownik_funkcji = {"Klasyfikacja":Klasyfikacja, "Wpis":Wpis, "Zapytanie":Zapytanie}

model = load_model(funkcje.sciezka_do_modelu_klasyfikatora) # wczytanie modelu klasyfikatora
# polaczenie z baza danych SQLite
polaczenie_z_baza_danych = sqlite3.connect(funkcje.nazwa_pliku_z_baza_danych)
kursor_bazy_danych = polaczenie_z_baza_danych.cursor() # za pomoca kursora wykonujemy operacje na bazie danych


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # AF_INET - IPv4
    # SOCK_STREAM - TCP
    
    s.bind((funkcje.IP_SERWERA,funkcje.PORT))
    s.listen(1)

    connection, address = s.accept()
    print("Adres polaczenia: ", address)

    while True:         # ODBIOR DANYCH
        data = connection.recv(funkcje.BUFOR_ROZMIAR)
        if not data : break # zakomentowac na probe
        ramka_danych_string = data.decode() # dane sa odbierane w formacie Byte
        ramka_danych_lista_stringow = ramka_danych_string.split() # podzial stringa po DOWOLNYM BIALYM ZNAKU
        while ramka_danych_lista_stringow[-1] != '$' :
            data = connection.recv(funkcje.BUFOR_ROZMIAR)
            if not data : break # zakomentowac na probe
            ramka_danych_string += data.decode() # w kazdej iteracji string sie powieksza, az zbierzemy cala ramke danych
            ramka_danych_lista_stringow = ramka_danych_string.split() # podzial stringa po DOWOLNYM BIALYM ZNAKU - zbiera CALA ramke danych w liste :)
        if ramka_danych_lista_stringow[0] =="END" :
            connection.send("END".encode())
            break
        
        if ramka_danych_lista_stringow[0] in slownik_funkcji :
            slownik_funkcji[ramka_danych_lista_stringow[0]]()
        else :
            print("Bledna ramka!")
            odpowiedz = "Bledna ramka!" + "\n" + ramka_danych_string
            connection.send(odpowiedz.encode())
        
polaczenie_z_baza_danych.commit()
polaczenie_z_baza_danych.close()


