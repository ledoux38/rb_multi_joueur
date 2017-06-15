#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import unittest

import socket as st

import threading

import time

import os

class Thread_Reception(threading.Thread):
	"""objet thread gérant la réception des messages"""
	
	def __init__(self, connexion):
		
		threading.Thread.__init__(self)
		
		self.connexion = connexion



	def run(self):

		while True:
			
			message_recu = self.connexion.recv(1024).decode()

			if not message_recu or message_recu.upper() =="FIN":
				
				break

			else:

				print("\033c", message_recu)
			


		print("Client arrêté. appuyer sur une touche pour terminer.")
		
		self.connexion.close()



class Thread_Emission(threading.Thread):
	"""objet thread gérant l'émission des messages"""
	
	def __init__(self, connexion):
		
		threading.Thread.__init__(self)
		
		self.connexion = connexion
	 
	def run(self):

		while True:

			message_emis = input()

			try:

				self.connexion.send(message_emis.encode())

			except:

				break




def ouverture_connexion(adresse, port):
	
	connexion = st.socket(st.AF_INET, st.SOCK_STREAM)
	
	connexion.connect((adresse, port))
	
	return connexion






if __name__ == '__main__':
	a = ouverture_connexion("127.0.0.1", 12100)

	th_R = Thread_Reception(a)

	th_R.start()

	th_E = Thread_Emission(a)

	th_E.start()
	
	#unittest.main()


	



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


	def client(self):

		message_a_envoyer = str()
		
		while message_a_envoyer != b"fin":

			message_recu = reception_donnee(self.a)
		
			dialogue_utilisateur(message_recu, reponse = False)
		
			message_a_envoyer = dialogue_utilisateur()
		
			emission_donnee(message_a_envoyer, self.a)



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
"""