#!/usr/bin/python3.5
# -*-coding:Utf-8 -*


import socket as st
import select as sc

try:
	import package.connexion as cn
except:
	import connexion as cn


try:
	import package.gestionnaire_clients as gs
except:
	import gestionnaire_clients as gs

class Serveur:
	"""la classe Serveur crée le serveur. elle gere les 
	connexions et aussi le jeux en general

	ATTRIBUTS:	- _tableau_de_connexions
				- connexion

	"""
	def __init__(self, hote_serveur, port_serveur):
		self._tableau_de_connexions = gs.Gestionnaire_clients()
		self.connexion = self.initialisation_connexion(hote = hote_serveur, port = port_serveur)



	def __del__(self):
		self.connexion.close()



	def __str__(self):
		msg = "{}, {}".format(self.connexion, self._tableau_de_connexions)
		return msg



	def _get_tableau_de_connexions(self):
		return self._tableau_de_connexions



	def _set_tableau_de_connexions(self, nouvelle_connexion):
		self._tableau_de_connexions.ajouter_connexion(nouvelle_connexion)



	def initialisation_connexion(self, hote, port, listen = 5):
		connexion = st.socket(st.AF_INET, st.SOCK_STREAM)
		connexion.bind((hote, port))
		connexion.listen(listen)
		return connexion	



	def emission_donnee(self, connexion, donnee):
		message_a_envoyer = str(donnee)
		message_a_envoyer = message_a_envoyer.encode()
		connexion.send(message_a_envoyer)





	def reception_donnee(self, connexion, taille = 1024):
		message_recu =connexion.recv(taille)
		print(message_recu.decode())




	def attente_de_connexion(self):
		connexion_client, info_client = self.connexion.accept()
		self._tableau_de_connexions += connexion_client
		#self._tableau_de_connexions.ajouter_connexion(connexion_client)


	tableau_de_connexions = property(fget = _get_tableau_de_connexions, fset = _set_tableau_de_connexions)

if __name__ == "__main__":
	version = 5


	#version tres basique d'un code de serveur
	if version == 0:
		

		connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
		connexion_principale.bind(("", 12800))

		connexion_principale.listen(5)

		connexion_client, info_client = connexion_principale.accept()

		print("info_client: {}".format(info_client))

		connexion_client.send(b"je viens de recevoir et d'accepter la connexion")

		connexion_client.close()
	


	#version basique d'un echange de donnée avec un client
	if version == 1:

		try:
			connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
			connexion_principale.bind(("", 12800))
			connexion_principale.listen(5)

		except ConnectionRefusedError:
			print("erreur lors du l'initialisation du serveur")

		print("serveur lancé \n en attente d'une connexion au port: 12800")
		connexion_client, info_client = connexion_principale.accept()
		print(type(connexion_client))

		message_recu = str()
		while message_recu != b"fin":

			message_recu = connexion_client.recv(1024)
			#print(connexion_client)
			print(message_recu.decode())

			message_a_envoyer = "5/5"
			message_a_envoyer = message_a_envoyer.encode()
			connexion_client.send(message_a_envoyer)

		print("fermeture de la connexion")

		connexion_client.close()
	


	#version basique d'un echange de donnée avec plusieurs clients
	if version == 2:

		try:
			connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
			connexion_principale.bind(("", 12800))
			connexion_principale.listen(5)


		except ConnectionRefusedError:
			print("erreur lors du l'initialisation du serveur")

		serveur_lance = True
		print("serveur lancé \n en attente d'une connexion au port: 12800")
		clients_connectes = []

		while serveur_lance:

			connexions_demandees, wlist, xlist = sc.select([connexion_principale], [], [], 0.05)
			#print (connexions_demandees, wlist, xlist, type(connexions_demandees), type(wlist), type(xlist))

			for connexion in connexions_demandees:
				connexions_clients, infos_connexion = connexion.accept()
				clients_connectes.append(connexions_clients)

			clients_a_lire = []

			try:
				clients_a_lire, wlist, xlist = sc.select(clients_connectes, [], [], 0.05)
			except select.error:
				pass

			else:
				for client in clients_a_lire:
					message_recu = client.recv(1024)
					message_recu = message_recu.decode()

					print("recu {}".format(message_recu))
					client.send(b"5/5")
					if message_recu == "fin":
						serveur_lance == False

		print("fermeture des connexions")

		for client in clients_connectes:
			client.close()

		connexion_principale.close()



	#version basique d'un echange de donnée avec plusieurs clients
	if version == 3:

		try:
			connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
			connexion_principale.bind(("", 12800))
			connexion_principale.listen(5)


		except ConnectionRefusedError:
			print("erreur lors du l'initialisation du serveur")

		serveur_lance = True
		print("serveur lancé \n en attente d'une connexion au port: 12800")
		tableau_des_clients = gs.Gestionnaire_clients()
		
		#clients_connectes = []

		while serveur_lance:

			connexions_demandees, wlist, xlist = sc.select([connexion_principale], [], [], 0.05)
			#print (connexions_demandees, wlist, xlist, type(connexions_demandees), type(wlist), type(xlist))

			for connexion in connexions_demandees:
				connexions_clients, infos_connexion = connexion.accept()
				#print(clients_connectes, type(clients_connectes))
				tableau_des_clients.ajouter_connexion(connexions_clients)
				#clients_connectes.append(connexions_clients)
				print(tableau_des_clients._tableau_de_connexions[0])
				print(type(tableau_des_clients._tableau_de_connexions[0]))
			clients_a_lire = []

			try:
				clients_a_lire, wlist, xlist = sc.select(tableau_des_clients._tableau_de_connexions, [], [], 0.05)
				#clients_a_lire, wlist, xlist = sc.select(clients_connectes, [], [], 0.05)
				#print(clients_connectes, type(clients_connectes))
			except sc.error:
				pass

			else:
				for client in clients_a_lire:
					message_recu = client.recv(1024)
					message_recu = message_recu.decode()

					print("recu {}".format(message_recu))
					client.send(b"5/5")
					if message_recu == "fin":
						serveur_lance == False

		print("fermeture des connexions")

		for client in clients_connectes:
			client.close()

		connexion_principale.close()


	#version en class Serveur
	if version == 5:
		try:
			a = Serveur("127.0.0.1", 12100)
			serveur = True
		except:
			serveur = False
			print("erreur lors de la creation de l'objet")

		if serveur:
			print("serveur actif et en attente d'une connexion")

			while True:
				a.attente_de_connexion()
				a.attente_de_connexion()
				a.reception_donnee(a._tableau_de_connexions[0])
				a.emission_donnee(a._tableau_de_connexions[0], donnee = "coucou")
				a.reception_donnee(a._tableau_de_connexions[1])
				a.emission_donnee(a._tableau_de_connexions[1], donnee = "coucou")
				#print(a._tableau_de_connexions[0])
