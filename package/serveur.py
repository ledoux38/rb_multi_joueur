#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import unittest

import socket as st

import select as sc

try:
	import package.connexion as cn
except:
	import connexion as cn

try:
	import package.application_labyrinthe as a_l
except:
	import application_labyrinthe as a_l

try:
	import package.gestionnaire_clients as gs
except:
	import gestionnaire_clients as gs

try:
	import package.Gestionnaire_entree_sortie_donnee as g_e_s
except:
	import Gestionnaire_entree_sortie_donnee as g_e_s

try:
	import package.utilitaires as us
except:
	import utilitaires as us

class Serveur:
	"""la classe Serveur crée le serveur. elle gere les 
	connexions et aussi le jeux en general

	ATTRIBUTS:	- app
				- connexion

	"""
	def __init__(self, hote_serveur, port_serveur):
				
		self.connexion = self.initialisation_connexion(hote = hote_serveur, port = port_serveur)

		self.app = a_l.Application_labyrinthe()



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
		
		return message_recu.decode()



	def attente_de_connexion(self):
		
		connexion_client, info_client = self.connexion.accept()
		
		self.app.g_clients.tableau_de_connexions.append(cn.Connexion(connexion = connexion_client))


	def jeux_labyrinthe(self):

		self.attente_de_connexion()

		nb_carte = g_e_s.Gestionnaire_entree_sortie_donnee.static_nombre_de_fichier(self.app.ch_dossier)

		liste = str(list(range(nb_carte)))

		erreur = False

		while True:

			self.emission_donnee(self.app.g_clients[0].information_connexion, self.app.choix_carte(erreur = erreur))

			choix = self.reception_donnee(self.app.g_clients[0].information_connexion)
			
			if choix in liste:
			
				self.app.chargement_carte(choix)

				break

			else:

				erreur = True

		self.app.carte.positionement_aleatoire(self.app.g_clients[0].joueur)

		while True:

			prep_inter_utilisateur , liste = self.app.proposition_de_deplacement(self.app.g_clients[0].joueur)

			self.emission_donnee(self.app.g_clients[0].information_connexion, prep_inter_utilisateur)

			choix = self.reception_donnee(self.app.g_clients[0].information_connexion)

			reponse_joueur = us.conversion_saisie_en_majuscule(chaine = choix)

			if reponse_joueur in liste: 
			
				self.app.mouvement_joueur(self.app.g_clients[0].joueur, reponse_joueur)

			else:

				print("erreur")




class test_serveur (unittest.TestCase):

	def setUp(self):

		self.a = Serveur("127.0.0.1", 12100)



	def tearDown(self):

		for i in self.a.app.g_clients:

			i.information_connexion.close()

		self.a.connexion.close()



	def test_jeux_labyrinthe(self):

		self.a.jeux_labyrinthe()


if __name__ == '__main__':

	unittest.main()


"""
if __name__ == "__main__":
	version = 5

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
				a.reception_donnee(a.app[0])
				a.emission_donnee(a.app[0], donnee = "coucou")
				a.reception_donnee(a.app[1])
				a.emission_donnee(a.app[1], donnee = "coucou")
				#print(a.app[0])
"""