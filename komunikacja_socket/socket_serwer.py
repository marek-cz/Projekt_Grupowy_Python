
# KOMUNIKACJA KLIENT - SERWER
# PROCES SERWERA
###############################################################################################
def wyodrebnij_osie_danych(lista):
    result = [[],[],[],[],[],[]]
    for i in range (len(lista)//6):
        result[0].append(lista[6*i + 0]) # AKCELEROMETR X
        result[1].append(lista[6*i + 1]) # AKCELEROMETR Y
        result[2].append(lista[6*i + 2]) # AKCELEROMETR Z
        result[3].append(lista[6*i + 3]) # ZYROSKOP X
        result[4].append(lista[6*i + 4]) # ZYROSKOP Y
        result[5].append(lista[6*i + 5]) # ZYROSKOP Z

    return result

def normalizuj(x): # dokladniej standaryzacja - wartosc srednia 0 i odchylenie standardowe 1
    x -= x.mean()
    x /= x.std()
#################################################################################################
import socket
import numpy as np
from keras.models import load_model
import sqlite3
import datetime


model = load_model("../zapis_modelu.h5") # wczytanie modelu klasyfikatora
IP_SERWERA = '' # U serwera puste
PORT = 5005 # liczba 16-bitowa, wiekszta niz 1024
BUFOR_ROZMIAR = 4096

wykryta_aktywnosc = ["Marsz", "Trucht", "Bieg"]
nazwa_pliku_z_baza_danych = "plik_bazy_danych.db"

# polaczenie z baza danych SQLite
polaczenie_z_baza_danych = sqlite3.connect(nazwa_pliku_z_baza_danych)
kursor_bazy_danych = polaczenie_z_baza_danych.cursor() # za pomoca kursora wykonujemy operacje na bazie danych


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # AF_INET - IPv4
    # SOCK_STREAM - TCP
    
    s.bind((IP_SERWERA,PORT))
    s.listen(1)

    connection, address = s.accept()
    print("Adres polaczenia: ", address)

    while True:
        data = connection.recv(BUFOR_ROZMIAR)
        if not data : break
        ramka_danych_string = data.decode() # dane sa odbierane w formacie Byte
        if ramka_danych_string =="END" : connection.send("END".encode())
        print('Odebralem dane : \n', ramka_danych_string)
        print("\n\n")

        ramka_danych_lista_stringow = ramka_danych_string.split()
        # w zaleznosci od typu ramki - DO USTALENIA NA SPOTKANIU!!!! - realizujemy odpowiedznie operacje
        
        if ramka_danych_lista_stringow[0] == "Klasyfikacja" : # zakladana ramka : [Klasyfikacja][ID_ZAWODNIKA][DANE]
            dane_osie = wyodrebnij_osie_danych(ramka_danych_lista_stringow[2:])
            probka = np.asarray(dane_osie).astype('float32')
            shape = probka.shape
            probka = probka.reshape(1,shape[0]*shape[1])
            klasyfikacja = model.predict(probka)
            indeks_np = np.where(klasyfikacja == klasyfikacja.max()) # szukamy najbardziej prawdopodobnego wyniku
            indeks = np.asscalar(indeks_np[1])
            # odeslij wynik klasyfikacji
            odpowiedz = "Tu serwer, odebralem dane :)\nWykryta aktywnosc to :  " + wykryta_aktywnosc[indeks] + " \n"
            connection.send(odpowiedz.encode())
            # wpisz do bazy danych
            kursor_bazy_danych.execute("insert into probki (a_x,a_y,a_z,g_x,g_y,g_z, etykieta ,czas) values(?,?,?,?,?,?,?,?)", (" ".join(dane_osie[0]), " ".join(dane_osie[1])," ".join(dane_osie[2]), " ".join(dane_osie[3])," ".join(dane_osie[4])," ".join(dane_osie[5]), wykryta_aktywnosc[indeks] ,datetime.datetime.now() ) )
            kursor_bazy_danych.execute("insert into aktywnosc (etykieta,czas,zawodnik_id) values(?,?,?)", (wykryta_aktywnosc[indeks],datetime.datetime.now(),int(ramka_danych_lista_stringow[1])) )
            polaczenie_z_baza_danych.commit()
        elif ramka_danych_lista_stringow[0] == "Wpis" : # wpisanie zawodnika [WPIS][IMIE][NAZWISKO][KLUB]
            kursor_bazy_danych.execute("insert into zawodnik (imie,nazwisko,klub) values(?,?,?)", (ramka_danych_lista_stringow[1],ramka_danych_lista_stringow[2],ramka_danych_lista_stringow[3]) )
        #elif ramka_danych_lista_stringow[0] == "Zapytanie" :
            # kod obslugi zapytania
            


    #connection.close()


#wynik = kursor_bazy_danych.execute("select * from probki")

#print(wynik.fetchall()) # fetchall() - wybiera wszystkie rekordy | fetchone - 1 wiersz|fetchmany - kilka wierszy
polaczenie_z_baza_danych.commit()
polaczenie_z_baza_danych.close()


