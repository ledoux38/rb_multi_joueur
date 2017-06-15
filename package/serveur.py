#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import unittest

import socket as st

import select as s_c

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
		"""initialisation des attributs"""
				
		self.connexion = self.initialisation_connexion(hote = hote_serveur, port = port_serveur)

		self.app = a_l.Application_labyrinthe()



	def initialisation_connexion(self, hote, port, listen = 5):
		"""Méthode qui permet l'initialisation de la connexion"""
	
		connexion = st.socket(st.AF_INET, st.SOCK_STREAM)
		
		connexion.bind((hote, port))
		
		connexion.listen(listen)
		
		return connexion	



	def emission_donnee(self, connexion, *donnee):
		"""Méthode qui permet la transmission de donnee"""

		message_a_envoyer = ""

		for i in donnee:

			message_a_envoyer += str(i) + "\n"

		message_a_envoyer = message_a_envoyer.encode()
		
		connexion.send(message_a_envoyer)



	def reception_donnee(self, connexion, taille = 1024):
		"""Méthode qui permet la reception de donnee"""
		
		message_recu =connexion.recv(taille)
		
		return message_recu.decode()



	def attente_de_connexion(self):
		"""Méthode qui l'attente de nouvelle connexion"""

		connexion_client, info_client = self.connexion.accept()
		
		self.app.g_clients.tableau_de_connexions.append(cn.Connexion(connexion = connexion_client))



	def phase_chargement_carte(self, liste_choix, connexion = False):

		erreur = False

		while True:

			if connexion == True:

				self.emission_donnee(connexion.information_connexion, self.app.choix_carte(erreur = erreur))

				choix = self.reception_donnee(connexion.information_connexion)

			else:

				choix = input(self.app.choix_carte(erreur = erreur))
			
			if choix in liste_choix:
			
				self.app.chargement_carte(choix)

				break

			else:

				erreur = True




	def phase_chargement_carteV2(self, connexion = False):

		nb_carte = g_e_s.Gestionnaire_entree_sortie_donnee.static_nombre_de_fichier(self.app.ch_dossier)

		liste = str(list(range(nb_carte)))

		erreur = False

		while True:

			if connexion == True:

				self.emission_donnee(connexion.information_connexion, self.app.choix_carte(erreur = erreur))

				choix = self.reception_donnee(connexion.information_connexion)

			else:

				choix = input(self.app.choix_carte(erreur = erreur))
			
			if choix in liste:
			
				self.app.chargement_carte(choix)

				break

			else:

				erreur = True



	def phase_mouvement_joueur(self, connexion):

		erreur = False

		while True:

			if erreur:

				prep_inter_utilisateur , liste = self.app.proposition_de_deplacement(connexion.joueur, "Erreur dans la saisie veuillez recommencer!")

				print(prep_inter_utilisateur, liste)
			
			else:

				prep_inter_utilisateur , liste = self.app.proposition_de_deplacement(connexion.joueur, "A vous de jouer!")

			self.emission_donnee(connexion.information_connexion, prep_inter_utilisateur)

			reponse_joueur = self.reception_donnee(connexion.information_connexion)

			reponse_joueur = us.conversion_saisie_en_majuscule(chaine = reponse_joueur)

			if reponse_joueur in liste: 
			
				self.app.mouvement_joueur(connexion.joueur, reponse_joueur)

				self.emission_donnee(connexion.information_connexion, self.app.carte.carte_utilisateur(connexion.joueur.coordonnee))

			else:

				erreur = True

				continue

			if connexion.joueur.coordonnee == self.app.carte.sortie.coordonnee:

				return True

			else:

				return False

	
	def app_labyrinthe(self):
		"""Méthode qui permet de lancer l'application labyrinthe"""



		nb_carte = g_e_s.Gestionnaire_entree_sortie_donnee.static_nombre_de_fichier(self.app.ch_dossier)

		liste = str(list(range(nb_carte)))

		self.phase_chargement_carte(liste_choix = liste)



		if len(self.app.g_clients) < 2:

			self.emission_donnee(self.app.g_clients[0].information_connexion, "veuillez patienter en attente d'un nouveau joueur")

			print("serveur lancer")

			self.attente_de_connexion()

			print("client connecté")

			self.attente_de_connexion()


		for connexion in self.app.g_clients:

			self.app.carte.positionement_aleatoire(connexion.joueur)

		boucle = True

		while boucle:

			for connexion in self.app.g_clients:

				#self.emission_donnee(connexion.information_connexion, "\n"*50)

				if self.phase_mouvement_joueur(connexion):

					prep_inter_utilisateur = "felicitation vous avez gagné"

					self.emission_donnee(connexion.information_connexion, prep_inter_utilisateur)

					boucle = False

					break


	def test_attente_de_connexionv2(self):

		serveur_lance = True

		liste_client = []
		
		while serveur_lance:

			connexions_demandees, wlist, xlist = s_c.select([self.connexion],[], [], 0.05)

			for connexion in connexions_demandees:
				
				connexion_avec_client, infos_connexion = connexion.accept()

				liste_client.append(connexion_avec_client)	
				
				self.app.g_clients.tableau_de_connexions.append(cn.Connexion(connexion = connexion_avec_client))

				self.app.carte.positionement_aleatoire(self.app.g_clients[-1].joueur)

				message_a_envoyer = "bienvenue au jeux du labyrinthe! \n vous etes {} joueurs \n{}\nCommande: <C> pour commencer partie".format(
					len(self.app.g_clients), self.app.carte.carte_utilisateur(self.app.g_clients[-1].joueur.coordonnee)).encode()
		
				connexion_avec_client.send(message_a_envoyer)		

				for client in self.app.g_clients:

					if client == self.app.g_clients[-1]:

						pass

					else:

						message_a_envoyer = "{}\nnouveau joueur connecté\ntotal de joueur: {} \n{}\nCommande: <C> pour commencer partie".format("\n"*50,
						len(self.app.g_clients), self.app.carte.carte_utilisateur(client.joueur.coordonnee)).encode()
		
						client.information_connexion.send(message_a_envoyer)

		    
			clients_a_lire = []
			try:
				clients_a_lire, wlist, xlist = s_c.select(liste_client,[], [], 0.05)

			except s_c.error:

				pass

			else:

				for client in clients_a_lire:

					msg_recu = client.recv(1024)

					msg_recu = msg_recu.decode().upper()

					if msg_recu == "C":

						serveur_lance = False

						break

					else:

						message_a_envoyer = "erreur commande non reconnu\ncommande : <C> commencer partie\n".encode()
				
						connexion_avec_client.send(message_a_envoyer)




class test_serveur (unittest.TestCase):

	def setUp(self):

		self.a = Serveur("127.0.0.1", 12100)



	def tearDown(self):

		self.a.connexion.close()

		for i in self.a.app.g_clients:

			i.information_connexion.close()



	"""def test_app_labyrinthe(self):

		self.a.app_labyrinthe()
	"""

	def test_attente_de_connexionv2(self):

		self.a.phase_chargement_carteV2()

		print("carte chargée!\n en attente de clients")

		self.a.test_attente_de_connexionv2()

		boucle = True

		while boucle:

			for connexion in self.a.app.g_clients:

				self.a.emission_donnee(connexion.information_connexion, "\n"*50)

				if self.a.phase_mouvement_joueur(connexion):

					prep_inter_utilisateur = "felicitation vous avez gagné"

					self.a.emission_donnee(connexion.information_connexion, prep_inter_utilisateur)

					boucle = False

					break
	
		self.a.connexion.close()

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