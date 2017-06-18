#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

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
	"""fonction qui ouvre un port pour ecoute"""

	connexion = st.socket(st.AF_INET, st.SOCK_STREAM)
	
	connexion.connect((adresse, port))
	
	return connexion






if __name__ == '__main__':
	
	a = ouverture_connexion("127.0.0.1", 12100)

	th_R = Thread_Reception(a)

	th_R.start()

	th_E = Thread_Emission(a)

	th_E.start()
	
