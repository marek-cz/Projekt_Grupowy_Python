""" API SQLowe do bazy danych """
nazwa_pliku_z_baza_danych = 'plik_bazy_danych.db'
# UTWORZENIE BAZY DANYCH :
import sqlite3

polaczenie_z_baza_danych = sqlite3.connect(nazwa_pliku_z_baza_danych)
kursor_bazy_danych = polaczenie_z_baza_danych.cursor() # za pomoca kursora wykonujemy operacje na bazie danych

while True:
    zapytanie = input("Zapytanie SQL. (q - wyjscie)\n>")
    if zapytanie == 'q' or zapytanie == 'Q' :
        break
    else:
        wynik = kursor_bazy_danych.execute(zapytanie)
        polaczenie_z_baza_danych.commit()
        print(wynik.fetchall())
polaczenie_z_baza_danych.commit()
polaczenie_z_baza_danych.close()
