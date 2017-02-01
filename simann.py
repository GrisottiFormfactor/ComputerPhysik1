import numpy as np
import subprocess
import math
import random as ran
import copy

# Simulated Annealing

#----------KONSTANTEN ETC----------
# L: Laenge des Gitters. N: Anzahl der Staedte

N  = 16
L = math.ceil(math.sqrt(N))

# Zuerst muss man die Staedte generieren. In diesem Programm sind die Staedte regulaer platziert.
staedte = {0:(0,0)}

for i in range(L):
	for j in range(L):
		index = i*L+j
		staedte[index] = (1*j,1*i)

# Fuer die Berechnung des Kostenfunktionals braucht man den Weg. 
weg = [i for i in range(N)]
weg_original = copy.copy(weg)

# Laenge zwischen zwei Wegen:
def kostenfunktion(weg):
	
	# differenzx = staedte[i][0]-staedte[i-1][0]
	# differenzy = staedte[i][1]-staedte[i-1][1]

	laengen = (math.sqrt((staedte[weg[i]][0]-staedte[weg[i-1]][0])**2 + (staedte[weg[i]][1]-staedte[weg[i-1]][1])**2) for i in range(1,N))
	
	return sum(laengen)

# Man muss den Weg manipulieren koennen. Dafuer definieren wir die nachfolgenden Funktionen.

# Zuerst kommt der Tausch von benachbarten Eintraegen.
def swap(weg):
	
	# Waehle zufaellig eine Stadt:
	r = np.random.randint(0,N)

	# Suche die Nachbarn dieser Stadt: alle Einträge neben dem eintrag r in der Weg-Liste.
	zuf = weg.index(r)

	if (zuf != 0) & (zuf != len(weg)-1):
		nachbarn = [zuf+1,zuf-1]
	if zuf == 0:
		nachbarn = [zuf+1]
	if zuf == len(weg)-1:
		nachbarn = [zuf-1]

	# waehle einen der Nachbarn:
	n = ran.choice(nachbarn)

	# Tausche die Nachbarn aus:
	dummy = weg[zuf]
	weg[zuf] = weg[n]
	weg[n] = dummy


def flip(weg):

	# Waehle zuerst zwei Stellen, an denen ausgeschnitten werden soll.
	s2 = np.random.randint(1,N)
	s1 = np.random.randint(0,s2)

	# Drehe den Abschnitt des Weges um.
	weg[s1:s2] = list(reversed(weg[s1:s2]))
	

# Ausschneiden eines Weges und  anfuegen an eine andere stelle:
def schneide(weg):

	# Waehle zuerst zwei Stellen, an denen ausgeschnitten werden soll.
	s2 = np.random.randint(1,N)
	s1 = np.random.randint(0,s2)

	# zuerst Speichern:
	speich = weg[s1:s2]

	# Loeschen
	del weg[s1:s2]

	# und dann einsetzen
	weg.extend(speich)
	
# Energieunterschied zwischen zwei Wegen:
def deltaE(wegneu,weg):
	
	delta = kostenfunktion(wegneu)-kostenfunktion(weg)
	
	return delta

# Die "Sweep"-Funktion:
def neuer_weg(weg,T):
	
	# Waehle zufaellig eine der drei Funktionen zur veraenderung des Weges.
	funkt = ran.choice([swap,flip,schneide])
		
	#D Erzeuge einen neuen Weg.
	weg_tilde = funkt(weg)
		
	#Berechne das rho und akzeptiere nach den Regeln des Metropolis-Algorithmus.
	rho = math.exp(-(deltaE(weg,weg_tilde)/T))
	if rho > np.random.rand(): 
		weg = weg_tilde

#----------HAUPTTEIL----------

# Zuerst wird die Temperatur ermittelt:
T0 = 1
NT = 2000
zaehl = 0

# Erzeuge N wegketten:
while True:
	
	for j in range(NT):

		speich = copy.copy(weg)

		# Waehle zufaellig eine der drei Funktionen zur veraenderung des Weges.
		funkt = ran.choice([swap,flip,schneide])

		funkt(weg)

		#Berechne das rho und akzeptiere nach den Regeln des Metropolis-Algorithmus.
		rho = math.exp(-(deltaE(weg,speich)/T0))

		random = np.random.rand()

		if rho > random: 
			zaehl = zaehl + 1	

		if rho <= random:
			zaehl = zaehl

	if (zaehl/NT) > 0.8:

		break

	else:

		T0 = T0*2
		zaehl = 0


# Das T0 ist jetzt ermittelt. 
# Setze den Weg auf den urspruenglichen Weg:
weg = weg_original

T = T0
n = 1
eta = 100
rho = 0
eta_vec = []
n_vec = []

while T > 0.1:
# while (eta <= 0) | (eta > 0.01):

	# Kopiere den Weg..
	neu = copy.copy(weg)
	
	# Berechne die Laenge des Weges vor der Veraenderung
	Ln = kostenfunktion(neu)
	
	rand = np.random.rand()
	
	
	while rho <= rand:
		
		while True:
	
			funkt = ran.choice([swap,flip,schneide])
	
			# Erzeuge Angebotskonfiguration	
			funkt(neu)
		
			if neu != weg:
				break

		# Berechne die Metropolis-Akzeptanz:	
		rho = math.exp(-deltaE(neu,weg)/T)
		
		if rho > rand:

			# Berechne die Laenge nach der Veraenderung des Weges:
			Lnp1 = kostenfunktion(neu)
		
			# Akzeptiere die Angebotskonfiguration.
			weg = copy.copy(neu)
	
			eta = Lnp1 - Ln

			eta_vec.append(Lnp1)

	#Kuehle das System:
	T = T0*(0.99**n)

	# Erhohe n:
	n = n+1
	
	if n == 1000:
		break
	n_vec.append(n)
	# Setze Rho zurück
	rho = 0




subprocess.run(["gnuplot", "potts.p", "--persist"], shell=False)





