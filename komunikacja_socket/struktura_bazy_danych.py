""" SKRYPT TWORZACY BAZE DANYCH SQLite """

nazwa_pliku_z_baza_danych = "plik_bazy_danych.db"

# SPRAWDZENIE CZY PLIK Z BAZA DANYCH JUZ ISTNIEJE - JESLI TAK -> USUN
import os

with os.scandir(os.curdir) as katalog_roboczy:
    for plik in katalog_roboczy:
        if(plik.name == nazwa_pliku_z_baza_danych) : # jesli jest plik o tej samej nazwie
            os.remove(nazwa_pliku_z_baza_danych)     # usun go 
            break;                                   # i wyjdz z petli

# UTWORZENIE BAZY DANYCH :
import sqlite3

polaczenie_z_baza_danych = sqlite3.connect(nazwa_pliku_z_baza_danych)
kursor_bazy_danych = polaczenie_z_baza_danych.cursor() # za pomoca kursora wykonujemy operacje na bazie danych
kursor_bazy_danych.execute("create table probki (id integer primary key, a_x text, a_y text, a_z text, g_x text, g_y text, g_z text, etykieta text ,czas datetime )")
kursor_bazy_danych.execute("create table zawodnik (id integer primary key, imie text, nazwisko text, klub text )")
kursor_bazy_danych.execute("create table aktywnosc (id integer primary key, etykieta text, czas datetime  ,zawodnik_id integer ,FOREIGN KEY(zawodnik_id) REFERENCES zawodnik(id)  )")
polaczenie_z_baza_danych.commit()
polaczenie_z_baza_danych.close()

def dodaj_zawodnika():
    imie = input("Podaj imie zawodnika : \n")
    nazwisko = input("Podaj nazwisko zawodnika : \n")
    klub = input("Podaj nazwe klubu zawodnika : \n")
    polaczenie_z_baza_danych = sqlite3.connect(nazwa_pliku_z_baza_danych)
    kursor_bazy_danych = polaczenie_z_baza_danych.cursor() # za pomoca kursora wykonujemy operacje na bazie danych
    kursor_bazy_danych.execute("insert into zawodnik (imie,nazwisko,klub) values(?,?,?)" , (imie, nazwisko,klub) )
    polaczenie_z_baza_danych.commit()
    polaczenie_z_baza_danych.close()
