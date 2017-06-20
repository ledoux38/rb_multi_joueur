#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

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
	import package.Gestionnaire_entree_sortie_donnee as g_e_s
except:
	import Gestionnaire_entree_sortie_donnee as g_e_s

try:
	import package.utilitaires as us
except:
	import utilitaires as us

try:
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c


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


	def phase_chargement_carte(self, connexion = None):
		"""Méthode qui charge la carte choisi par l'utilisateur"""

		nb_carte = g_e_s.Gestionnaire_entree_sortie_donnee.static_nombre_de_fichier(self.app.ch_dossier)

		liste = str(list(range(nb_carte)))

		erreur = False

		while True:

			#si connexion en parametre envoi liste de carte a la connexion concerné
			if connexion != None:

				self.emission_donnee(connexion.information_connexion, self.app.choix_carte(erreur = erreur))

				choix = self.reception_donnee(connexion.information_connexion)

			#sinon demande a l'operateur du serveur le choix
			else:

				choix = input(self.app.choix_carte(erreur = erreur))
			
			#verification du choix par rapport a la liste
			if choix in liste:
			
				self.app.chargement_carte(choix)

				break

			else:

				erreur = True


	def phase_mouvement_joueur(self, connexion):
		"""Méthode qui gerent le deplacement de la connexion"""

		erreur = False

		while True:

			#si erreur True message reception de la reponse incorrecte parmi la liste envoyer
			if erreur:
				
				prep_inter_utilisateur , liste = self.app.proposition_de_deplacement(connexion.joueur, "Erreur dans la saisie veuillez recommencer!")

				print(prep_inter_utilisateur, liste)
			
			#sinon envoi proposition à la connexion et verification des donnees
			else:

				prep_inter_utilisateur , liste = self.app.proposition_de_deplacement(connexion.joueur, "A vous de jouer!")

			self.emission_donnee(connexion.information_connexion, prep_inter_utilisateur)

			reponse_joueur = self.reception_donnee(connexion.information_connexion)

			reponse_joueur = us.conversion_saisie_en_majuscule(chaine = reponse_joueur)

			#verification reponse connexion et conforme à la liste
			if reponse_joueur in liste: 

				#si reponse connexion == quit alors procedure de deconnexion lancé 
				if reponse_joueur == "QUIT":

					#si moins de 2 connexions en cours sur le serveur coupure de la connexion client <-> serveur
					#et coupure connexion serveur
					if len(self.app.g_clients) < 2:

						connexion.information_connexion.close()

						self.connexion = close()

						break

					else:

						coordonnee = connexion.joueur.coordonnee

						self.app.carte[coordonnee[0]][coordonnee[1]] = e_c.Couloir(coordonnee = coordonnee)

						connexion.information_connexion.close()

						self.app.g_clients.tableau_de_connexions.remove(connexion)

				elif reponse_joueur == "PASSER":
				#sinon si la connexion renvoi PASSER alors on passe le tour du joueur
					pass

				#si reponse connexion different de "quit alors mouvement autorisé"
				else:

					self.app.mouvement_joueur(connexion.joueur, reponse_joueur)

					self.emission_donnee(connexion.information_connexion,self.app.carte.carte_utilisateur(connexion.joueur.coordonnee), "en attente des autres joueurs...")

			#si reponse non conforme a la liste envoi d'un message d'erreur à la connexion
			else:

				erreur = True

				continue

			#verification que la connexion sois egal a la sortie
			if connexion.joueur.coordonnee == self.app.carte.sortie.coordonnee:

				return True

			else:

				return False

	
	def app_labyrinthe(self):
		"""gestionnaire principale de la classe serveur"""

		#chargment de la carte
		self.phase_chargement_carte()

		print("carte chargée!\n en attente de clients")

		#attente de connexion
		self.test_attente_de_connexion()

		boucle = True

		#lancement de la partie jusqua victoire ou qu'ils y est plus de joueur
		while boucle:

			for connexion in self.app.g_clients:

				if self.phase_mouvement_joueur(connexion):

					prep_inter_utilisateur = "felicitation vous avez gagné"

					self.emission_donnee(connexion.information_connexion, prep_inter_utilisateur)

					boucle = False

					break

		#procedure de deconnexion des connexions 
		for connexion in self.app.g_clients:

			connexion.information_connexion.close()
		
		#arret de l'ecoute du port du serveur
		self.connexion.close()



	def attente_de_connexion(self):
		"""methode qui attend le nombre de connexion"""

		serveur_lance = True

		liste_client = []
		
		while serveur_lance:

			"""verification dde de connexion"""
			connexions_demandees, wlist, xlist = s_c.select([self.connexion],[], [], 0.05)

			"""pour chaque demande de connexion creation d'une connexion et d'un joueur"""
			for connexion in connexions_demandees:
				
				connexion_avec_client, infos_connexion = connexion.accept()

				liste_client.append(connexion_avec_client)	
				
				self.app.g_clients.tableau_de_connexions.append(cn.Connexion(connexion = connexion_avec_client))

				self.app.carte.positionement_aleatoire(self.app.g_clients[-1].joueur)

				message_a_envoyer = "bienvenue au jeux du labyrinthe! \n vous etes {} joueurs \n{}\nCommande: <C> pour commencer partie".format(
					len(self.app.g_clients), self.app.carte.carte_utilisateur(self.app.g_clients[-1].joueur.coordonnee)).encode()
		
				connexion_avec_client.send(message_a_envoyer)		

				"""envoi d'information au differente connexion"""
				for client in self.app.g_clients:

					if client == self.app.g_clients[-1]:

						pass

					else:

						message_a_envoyer = "nouveau joueur connecté\ntotal de joueur: {} \n{}\nCommande: <C> pour commencer partie".format(
						len(self.app.g_clients), self.app.carte.carte_utilisateur(client.joueur.coordonnee)).encode()
		
						client.information_connexion.send(message_a_envoyer)

		    
			clients_a_lire = []
			try:
				clients_a_lire, wlist, xlist = s_c.select(liste_client,[], [], 0.05)

			except s_c.error:

				pass

			#reception de message des differente connexions
			else:

				for client in clients_a_lire:

					msg_recu = client.recv(1024)

					msg_recu = msg_recu.decode().upper()

					"""si message == C alors arret de la boucle et lancement de la partie"""
					if msg_recu == "C":

						for client in self.app.g_clients:

							message_a_envoyer = "{}\n{}".format("Debut de la partie:",self.app.carte.carte_utilisateur(client.joueur.coordonnee)).encode()

							client.information_connexion.send(message_a_envoyer)

						serveur_lance = False

						break

					else:

						message_a_envoyer = "erreur commande non reconnu\ncommande : <C> commencer partie\n".encode()
				
						connexion_avec_client.send(message_a_envoyer)

