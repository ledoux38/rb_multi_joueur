#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import unittest

import socket as st

import threading

import time

class ThreadReception(threading.Thread):
	"""objet thread gérant la réception des messages"""
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn	     # réf. du socket de connexion
 
	def run(self):
		print("run")
		while 1:
			message_recu = self.connexion.recv(1024).decode()
			print("*" + message_recu + "*")
			if not message_recu or message_recu.upper() =="FIN":
				print("arret")
				break
			# Le thread <réception> se termine ici.
			# On force la fermeture du thread <émission> :
		#self._stop()
		print("Client arrêté. Connexion interrompue.")
		self.connexion.close()
 
class ThreadEmission(threading.Thread):
	"""objet thread gérant l'émission des messages"""
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn	     # réf. du socket de connexion
	 
	def run(self):
		while 1:
			message_emis = input()
			self.connexion.send(message_emis.encode())


def ouverture_connexion(adresse, port):
	connexion = st.socket(st.AF_INET, st.SOCK_STREAM)
	connexion.connect((adresse, port))
	return connexion

def reception_donnee(connexion, poids_donnee = 1024, encodage = "utf-8"):
	message_recu = connexion.recv(poids_donnee)
	return message_recu.decode(encodage)

def emission_donnee(message_a_envoyer, connexion, encodage = "utf-8"):
	message_a_envoyer = message_a_envoyer.encode(encodage)
	connexion.send(message_a_envoyer)

def dialogue_utilisateur(texte_a_afficher = "", reponse = True):
	print(texte_a_afficher)

	if reponse:
		reponse_utilisateur = input(" > ")
		return reponse_utilisateur

def fermeture_connexion(connexion):
	connexion.close()



class test_serveur (unittest.TestCase):

	def setUp(self):

		self.a = ouverture_connexion("127.0.0.1", 12100)



	def tearDown(self):

		self.a.close()



	def client(self):

		message_a_envoyer = str()
		
		while message_a_envoyer != b"fin":

			message_recu = reception_donnee(self.a)
		
			dialogue_utilisateur(message_recu, reponse = False)
		
			message_a_envoyer = dialogue_utilisateur()
		
			emission_donnee(message_a_envoyer, self.a)


	def test_client_threader(self):
		th_R = ThreadReception(self.a)

		th_R.start()

		th_E = ThreadEmission(self.a)

		th_E.start()





if __name__ == '__main__':

#	unittest.main()

	a = ouverture_connexion("127.0.0.1", 12100)

	th_R = ThreadReception(a)

	th_R.start()

	th_E = ThreadEmission(a)

	th_E.start()


	



"""
	if version == 3:
		
		connexion_au_serveur = ouverture_connexion("127.0.0.1", 12100)

		message_a_envoyer = str()
		
		while message_a_envoyer != b"fin":

			message_recu = reception_donnee(connexion_au_serveur)
		
			dialogue_utilisateur(message_recu, reponse = False)
		
			message_a_envoyer = dialogue_utilisateur()
		
			emission_donnee(message_a_envoyer, connexion_au_serveur)
		


		fermeture_connexion(connexion_au_serveur)		

"""