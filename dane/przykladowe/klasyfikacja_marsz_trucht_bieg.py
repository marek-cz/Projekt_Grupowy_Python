print("KLASYFIKACJA WIELOKLASOWA\nMARSZ, TRUCHT I BIEG")

import numpy as np
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical

liczba_epok = 10

wymiar_warstw = 16

dane = np.load('data.npy')
etykiety_liczby = np.load('labels.npy')
# KODOWANIE ETYKIET ZA POMOCA GOROCEJ JEDYNKI (strona 92)

etykiety = to_categorical(etykiety_liczby)
liczba_kategorii = len(etykiety[0])

############################################################
# PODZIAL DANYCH NA ZBIORY TRENINGOWY, WALIDACYJNY I TESTOWY
liczba_probek = dane.shape[0]
liczba_probek_treningowych = 3 * (liczba_probek // 5)
liczba_probek_walidacyjnych = (liczba_probek - liczba_probek_treningowych) // 2

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
model.add(layers.Dense(4 * wymiar_warstw,activation='relu', input_shape=(shape[1],)))
model.add(layers.Dense(2 * wymiar_warstw,activation='relu'))
model.add(layers.Dense(liczba_kategorii,activation='softmax')) # na kazdym wyjsciu prawdopodobienstwo ze element nalezy do danej klasy

# KOMPILOWANIE MODELU

model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

# TRENOWANIE MODELU

historia_treningu = model.fit(dane_treningowe, etykiety_treningowe, epochs = liczba_epok, batch_size = 52, validation_data=(dane_walidacyjne, etykiety_walidacyjne))

# WYNIKI

acc = historia_treningu.history['acc']
val_acc = historia_treningu.history['val_acc']
loss = historia_treningu.history['loss']
val_loss = historia_treningu.history['val_loss']
# WYKRES DOKLADNOSCI
epoki = range(1,len(acc)+1)
plt.plot(epoki,acc,'bo',label = 'Doklanopsc trenowania')
plt.plot(epoki,val_acc,'b',label = 'Doklanopsc walidacji')
plt.title('Dokldanopsc trenowania i walidacji')
plt.xlabel('Epoki')
plt.ylabel('Doklanopsc')
plt.legend()
plt.show()

#WYKRES STRATY
plt.clf()
plt.plot(epoki,loss,'ro',label = 'Strata trenowania')
plt.plot(epoki,val_loss,'r',label = 'Strata walidacji')
plt.title('Strata trenowania i walidacji')
plt.xlabel('Epoki')
plt.ylabel('Strata')
plt.legend()
plt.show()

# WYNIKI WALIDACYJNE:

wyniki_walidacji = model.evaluate(dane_walidacyjne, etykiety_walidacyjne)
print("WYNIKI WALIDACJI: ",wyniki_walidacji)

# zapisanie modelu do pliku

from keras.models import load_model
model.save("../../zapis_modelu.h5")
# Trenowanie na wszystkich danych treningowych:
#model.fit(dane_treningowe, etykiety_treningowe, epochs = liczba_epok, batch_size = 64)
