print("KLASYFIKACJA WIELOKLASOWA\nMARSZ, TRUCHT I BIEG")

import numpy as np
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical

liczba_epok = 25
wymiar_warstw = 16
liczba_probek_w_paczce = 100

decyzja = input("czy losowac dane na nowo t/n\n")
if decyzja == 't':
    
    ############################################################### 
    # WCZYTANIE DANYCH Z PLIKOW
    data_Socik = np.load('data_Socik.npy')
    etykiety_liczby_Socik = np.load('labels_Socik.npy')
    data_Marek = np.load('data_Marek.npy')
    etykiety_liczby_Marek = np.load('labels_Marek.npy')


    data = np.concatenate( (data_Socik, data_Marek) )
    etykiety_liczby = np.concatenate( (etykiety_liczby_Socik, etykiety_liczby_Marek) )


    liczba_probek = data.shape[0]
    liczba_probek_treningowych = 3 * (liczba_probek // 5)
    liczba_probek_walidacyjnych = (liczba_probek - liczba_probek_treningowych) // 2

    # KODOWANIE ETYKIET ZA POMOCA GOROCEJ JEDYNKI (strona 92)

    labels = to_categorical(etykiety_liczby)
    liczba_kategorii = len(labels[0])
    ###########################################################
    # USTAWIENIE W LOSOWEJ KOLEJNOSCI
    kolejnosc = np.arange(0,liczba_probek,1)
    np.random.shuffle(kolejnosc)

    etykiety = to_categorical(etykiety_liczby)
    dane = np.zeros((liczba_probek,6,liczba_probek_w_paczce))

    for i in range(len(kolejnosc)):
        dane[kolejnosc[i]] = data[i]
        etykiety[kolejnosc[i]] = labels[i]

    np.save("dane",dane)
    np.save("etykiety",etykiety)
else :
    dane = np.load('dane.npy')
    etykiety = np.load('etykiety.npy')
    
    liczba_kategorii = len(etykiety[0])
    liczba_probek = dane.shape[0]
    liczba_probek_treningowych = 3 * (liczba_probek // 5)
    liczba_probek_walidacyjnych = (liczba_probek - liczba_probek_treningowych) // 2


############################################################
# PODZIAL DANYCH NA ZBIORY TRENINGOWY, WALIDACYJNY I TESTOWY

dane_treningowe = dane[:liczba_probek_treningowych]
etykiety_treningowe = etykiety[:liczba_probek_treningowych]

dane_walidacyjne     = dane[liczba_probek_treningowych : (liczba_probek_treningowych + liczba_probek_walidacyjnych)]
etykiety_walidacyjne = etykiety[liczba_probek_treningowych : (liczba_probek_treningowych + liczba_probek_walidacyjnych)]

dane_testowe = dane[(liczba_probek_treningowych + liczba_probek_walidacyjnych):]
etykiety_testowe = etykiety[(liczba_probek_treningowych + liczba_probek_walidacyjnych):]

# DOPASOWANIE KSZTALTU DANYCH DO WARSTWY DENSE

shape = dane_treningowe.shape
dane_treningowe = dane_treningowe.reshape((shape[0],shape[1]*shape[2]))

shape = dane_walidacyjne.shape
dane_walidacyjne = dane_walidacyjne.reshape((shape[0],shape[1]*shape[2]))

shape = dane_testowe.shape
dane_testowe = dane_testowe.reshape((shape[0],shape[1]*shape[2]))



shape = dane_treningowe.shape
from keras import models
from keras import layers

# DEFINICJA MODELU
model = models.Sequential()
model.add(layers.Dense(4 * wymiar_warstw,activation='relu', input_shape=(shape[1],))) # wejscie warstwy ma ksztalt (batch_size,shape[1]), a wyjscie (batch_size,4*wymiar...)
model.add(layers.Dense(2 * wymiar_warstw,activation='relu'))
model.add(layers.Dense(liczba_kategorii,activation='softmax')) # na kazdym wyjsciu prawdopodobienstwo ze element nalezy do danej klasy

# KOMPILOWANIE MODELU

model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

# TRENOWANIE MODELU

historia_treningu = model.fit(dane_treningowe, etykiety_treningowe, epochs = liczba_epok, batch_size = 32,
                              validation_data=(dane_walidacyjne, etykiety_walidacyjne))


# WYNIKI

acc = historia_treningu.history['acc']
val_acc = historia_treningu.history['val_acc']
loss = historia_treningu.history['loss']
val_loss = historia_treningu.history['val_loss']

epoki = range(1,len(acc)+1)

fig, ax = plt.subplots(2, 1)

ax[0].plot(epoki,acc,'bo',label = 'Doklanosc trenowania')
ax[0].plot(epoki,val_acc,'b',label = 'Doklanosc walidacji')
ax[0].set_title('Dokldanosc trenowania i walidacji')
ax[0].set_xlabel('Epoki')
ax[0].set_ylabel('Doklanopsc')

ax[1].plot(epoki,loss,'ro',label = 'Strata trenowania')
ax[1].plot(epoki,val_loss,'r',label = 'Strata walidacji')
ax[1].set_title('Strata trenowania i walidacji')
ax[1].set_xlabel('Epoki')
ax[1].set_ylabel('Strata')
# WYKRES DOKLADNOSCI
#epoki = range(1,len(acc)+1)
#plt.plot(epoki,acc,'bo',label = 'Doklanopsc trenowania')
#plt.plot(epoki,val_acc,'b',label = 'Doklanopsc walidacji')
#plt.title('Dokldanopsc trenowania i walidacji')
#plt.xlabel('Epoki')
#plt.ylabel('Doklanopsc')
plt.legend()
plt.show()

#WYKRES STRATY
#plt.clf()
#plt.plot(epoki,loss,'ro',label = 'Strata trenowania')
#plt.plot(epoki,val_loss,'r',label = 'Strata walidacji')
#plt.title('Strata trenowania i walidacji')
#plt.xlabel('Epoki')
#plt.ylabel('Strata')
#plt.legend()
#plt.show()

# WYNIKI WALIDACYJNE:

wyniki_walidacji = model.evaluate(dane_walidacyjne, etykiety_walidacyjne)
print("WYNIKI WALIDACJI: ",wyniki_walidacji)

# zapisanie modelu do pliku

from keras.models import load_model
model.save("../../zapis_modelu.h5")
# Trenowanie na wszystkich danych treningowych:
#model.fit(dane, etykiety, epochs = liczba_epok, batch_size = 64)
