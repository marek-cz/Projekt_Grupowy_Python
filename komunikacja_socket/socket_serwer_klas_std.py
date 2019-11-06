""" KLASYFIKACJA NA PODSTAWIE ODCHYLENIA STD """
# KOMUNIKACJA KLIENT - SERWER
# PROCES SERWERA

ZAKRES_AKCELEROMETR = 8000
ZAKRES_ZYROSKOP     = 2000

IP_SERWERA = '' # U serwera puste
PORT = 5005 # liczba 16-bitowa, wiekszta niz 1024
BUFOR_ROZMIAR = 4096
BIEGANIE_PROGI_ODCHYLENIA_STD = {"akc_x" : 2000, "akc_y" : 2000, "akc_z" : 2000, "gyr_x" : 2000, "gyr_y" : 300, "gyr_z" : 2000 }
MARSZ_PROGI_ODCHYLENIA_STD    = {"akc_x" : 500,  "akc_y" : 2000, "akc_z" : 500,  "gyr_x" : 2000, "gyr_y" : 10, "gyr_z" : 2000 }
TRUCHT_PROGI_ODCHYLENIA_STD   = {"akc_x" : 1300, "akc_y" : 2000, "akc_z" : 1300, "gyr_x" : 2000, "gyr_y"  : 10, "gyr_z" : 2000 }

PROGI_ODCHYLENIE_STD = {"Bieganie" : BIEGANIE_PROGI_ODCHYLENIA_STD, "Marsz" : MARSZ_PROGI_ODCHYLENIA_STD, "Trucht" : TRUCHT_PROGI_ODCHYLENIA_STD } 



wykryta_aktywnosc = ["Marsz", "Trucht", "Bieg","Stanie"]
nazwa_pliku_z_baza_danych = "plik_bazy_danych.db"

###############################################################################################
def wyodrebnij_osie_danych(lista):
    result = [[],[],[],[],[],[]]
    for probka in lista:
        result[0].append(probka[0] )#/ ZAKRES_AKCELEROMETR ) # AKCELEROMETR X + NORMALIZACJA WZGLEDEM ZAKRESU
        result[1].append(probka[1] )#/ ZAKRES_AKCELEROMETR ) # AKCELEROMETR Y
        result[2].append(probka[2] )#/ ZAKRES_AKCELEROMETR ) # AKCELEROMETR Z
        result[3].append(probka[3] )#/ ZAKRES_ZYROSKOP ) # ZYROSKOP X
        result[4].append(probka[4] )#/ ZAKRES_ZYROSKOP ) # ZYROSKOP Y
        result[5].append(probka[5] )#/ ZAKRES_ZYROSKOP ) # ZYROSKOP Z

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


def klasyfikacja_odchylenie_std(probka_danych, slownik_progow):
    odchylenia_std_osi = []
    for os in probka_danych:
        odchylenia_std_osi.append(os.std())
    if (odchylenia_std_osi[0] >= slownik_progow['Bieganie']['akc_x']) and (odchylenia_std_osi[2] >= slownik_progow['Bieganie']['akc_z']) and (odchylenia_std_osi[4] >= slownik_progow['Bieganie']['gyr_y']):
        return 2 # indeks biegania
    elif (odchylenia_std_osi[0] >= slownik_progow['Trucht']['akc_x']) and (odchylenia_std_osi[2] >= slownik_progow['Trucht']['akc_z']) and (odchylenia_std_osi[4] >= slownik_progow['Trucht']['gyr_y']):
        return 1 # indeks truchtu
    elif (odchylenia_std_osi[0] >= slownik_progow['Marsz']['akc_x']) and (odchylenia_std_osi[2] >= slownik_progow['Marsz']['akc_z']) and (odchylenia_std_osi[4] >= slownik_progow['Marsz']['gyr_y']):
        return 1 # indeks marszu
    else :
        return 3 # indeks stania
#################################################################################################
import socket
import numpy as np
import sqlite3
import datetime



# polaczenie z baza danych SQLite
#polaczenie_z_baza_danych = sqlite3.connect(nazwa_pliku_z_baza_danych)
#kursor_bazy_danych = polaczenie_z_baza_danych.cursor() # za pomoca kursora wykonujemy operacje na bazie danych


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
        ramka_danych_lista_stringow = ramka_danych_string.split()
        while ramka_danych_lista_stringow[-1] != '$' :
            data = connection.recv(BUFOR_ROZMIAR)
            if not data : break
            ramka_danych_string += data.decode() # dane sa odbierane w formacie Byte
            ramka_danych_lista_stringow = ramka_danych_string.split()
        if ramka_danych_string =="END" : connection.send("END".encode())
        print('Odebralem dane : \n', ramka_danych_string)
        #print("\n\n")

        ramka_danych_lista_stringow = ramka_danych_string.split() # podzial stringa po DOWOLNYM BIALYM ZNAKU
        print(len(ramka_danych_lista_stringow))
        # w zaleznosci od typu ramki - DO USTALENIA NA SPOTKANIU!!!! - realizujemy odpowiedznie operacje
        
        if ramka_danych_lista_stringow[0] == "Klasyfikacja" : # zakladana ramka : [Klasyfikacja][ID_ZAWODNIKA][DANE][$]
            # [DANE] = [Timestamp][a_x][a_y][a_z][g_x][g_y][g_z] x Liczba_probek_w_paczce
            print("\nKLASYFIKUJE!\n")
            lista_probek_timestamp = lista_stringow_na_liste_probek(ramka_danych_lista_stringow[2:-1])
            lista_probek_timestamp.sort() # sortujemy po Timestamp
            lista_posortowanych_probek = usun_timestamp(lista_probek_timestamp) # usuwamy timestamp
            
            lista_posortowanych_probek_float = np.asarray(lista_posortowanych_probek).astype('float32') # przechodzimy na floaty
            
            dane_osie = wyodrebnij_osie_danych(lista_posortowanych_probek_float) # podzial probek na osie czujnikow
            
            probka = np.asarray(dane_osie).astype('float32')
                
            indeks = klasyfikacja_odchylenie_std(probka,PROGI_ODCHYLENIE_STD)
            # odeslij wynik klasyfikacji
            #odpowiedz = "Tu serwer, odebralem dane :)\nWykryta aktywnosc to :  "
            odpowiedz = "Tu serwer, odebralem dane :)\nWykryta aktywnosc to :  " + wykryta_aktywnosc[indeks] + " \n"
            connection.send(odpowiedz.encode())
            # wpisz do bazy danych
            #dane_osie = wyodrebnij_osie_danych_string(lista_posortowanych_probek) # podzial probek na osie czujnikow - do zapisu
            #kursor_bazy_danych.execute("insert into probki (a_x,a_y,a_z,g_x,g_y,g_z, etykieta ,czas) values(?,?,?,?,?,?,?,?)", (" ".join(dane_osie[0]), " ".join(dane_osie[1])," ".join(dane_osie[2]), " ".join(dane_osie[3])," ".join(dane_osie[4])," ".join(dane_osie[5]), wykryta_aktywnosc[indeks] ,datetime.datetime.now() ) )
            #kursor_bazy_danych.execute("insert into aktywnosc (etykieta,czas,zawodnik_id) values(?,?,?)", (wykryta_aktywnosc[indeks],datetime.datetime.now(),int(ramka_danych_lista_stringow[1])) )
            #polaczenie_z_baza_danych.commit()
        elif ramka_danych_lista_stringow[0] == "Wpis" : # wpisanie zawodnika [WPIS][IMIE][NAZWISKO][KLUB]
            kursor_bazy_danych.execute("insert into zawodnik (imie,nazwisko,klub) values(?,?,?)", (ramka_danych_lista_stringow[1],ramka_danych_lista_stringow[2],ramka_danych_lista_stringow[3]) )
        #elif ramka_danych_lista_stringow[0] == "Zapytanie" :
            # kod obslugi zapytania
        else :
            print("DUPA")
            


    #connection.close()


#wynik = kursor_bazy_danych.execute("select * from probki")

#print(wynik.fetchall()) # fetchall() - wybiera wszystkie rekordy | fetchone - 1 wiersz|fetchmany - kilka wierszy
#polaczenie_z_baza_danych.commit()
#polaczenie_z_baza_danych.close()


