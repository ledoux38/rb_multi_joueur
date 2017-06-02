#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

try:
	import package.carte
except:
	import carte

try:
	import package.gestionnaire_clients as g_c
except:
	import gestionnaire_clients as g_c

try:
	import package.utilitaires as us
except:
	import utilitaires as us

try:
	import package.Gestionnaire_entree_sortie_donnee as g_e_s
except:
	import Gestionnaire_entree_sortie_donnee as g_e_s

try:
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c

try:
	import package.sauvegarde_tmp as s_p
except:
	import sauvegarde_tmp as s_p

import copy


class Application_labyrinthe:

	def __init__(self):

		self.g_clients = g_c.Gestionnaire_clients()

		self.carte = None

		self.ch_dossier = "/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/"



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la class via un print()"""
		
		msg = "nb clients: {} \nCarte: {}".format(self.g_clients, self.carte)
		
		return msg



	def __len__(self):
		"""methode appeler lorsque on veut connaitre la taille du tableau"""
		
		return len(self.g_clients)


	def choix_carte(self):
		"""fonction qui permet de préparer une chaine de caractere à envoyer au joueur pour le choix de la carte"""
		es = g_e_s.Gestionnaire_entree_sortie_donnee.static_RecupList(self.ch_dossier)
		
		liste_str = ""

		for numero, index in enumerate(es):
			
			liste_str += "<{}>: {}\n".format(numero,index)

		texte_descriptif = "Bienvenue sur l'application l'Abyrinthe multi_joueurs.\n Veillez choisir la carte pour lancer la partie!\n{}".format(liste_str)
		
		return texte_descriptif



	def validation_reponse_joueurs(self, reponse, action):
		"""fonction qui va analyser la reponse pour verifier ça validiter"""
		reponse_joueur = us.conversion_saisie_en_majuscule(chaine = reponse)

		if reponse_joueur in action:
			
			return True

		else:
			
			return False



	def chargement_carte(self, choix):
		"""fonction qui va charger une carte choisi par le joueur"""
		
		liste = g_e_s.Gestionnaire_entree_sortie_donnee.static_RecupList(self.ch_dossier)

		nom_fichier = liste[int(choix)]

		adr = self.ch_dossier + nom_fichier

		carte_en_str = g_e_s.Gestionnaire_entree_sortie_donnee.static_chargement_donnee(adr)

		self.carte = carte.Carte(nom = nom_fichier, chaine = carte_en_str)



	def proposition_de_deplacement(self, joueur):
		"""retourne dans une list les valeurs de deplacement possible du joueur"""

		liste = self.carte.liste_coordonne_en_point_cardinaux(coordonnee = joueur.coordonnee)

		chaine = "proposition de deplacement:\n"

		if liste[0]:

			chaine += "<N> NORD\n"

		if liste[1]:

			chaine += "<E> EST\n"

		if liste[2]:

			chaine += "<S> SUD\n"

		if liste[3]:

			chaine += "<O> OUEST\n"

		return chaine



	def mouvement_joueur(self, joueur, mouvement):
		"""fonction qui va deplacer le joueurs sur la carte"""

		if not mouvement in "NSEW":
			raise ValueError( "mouvement != 'NSEW' ")

		coordonnee_joueur = joueur.coordonnee

		objet = None

		#coord = None

		dictionnaire = {"N":(-1,0), "E":(0,1), "S":(1,0), "O":(0,-1)}


		objet = self.carte [coordonnee_joueur[0] + dictionnaire[mouvement][0] ] [coordonnee_joueur[1] + dictionnaire[mouvement][1] ]

		#coord = objet.coordonnee


		if isinstance(objet, e_c.Couloir) or isinstance(objet, e_c.Porte) or isinstance(objet, e_c.Sortie):

			sauve_tmp = s_p.sauvegarde_tmp(joueur, objet)
			
			joueur.coordonnee = objet.coordonnee

			joueur.element_nouvelle_position = objet

			self.carte[joueur.coordonnee[0]][joueur.coordonnee[1]] = joueur

			self.carte[sauve_tmp[0].element_nouvelle_position.coordonnee[0]][sauve_tmp[0].element_nouvelle_position.coordonnee[1]] = sauve_tmp[0].element_nouvelle_position

			del sauve_tmp
		else:

			raise TypeError("Erreur objet carte != e_c.Couloir")



	def verification_de_victoire(self):
		"""fonction qui à pour but de verifier si il y a victoire"""

		liste = self.carte.rechercher_liste_valeurs(e_c.Joueur())

		if isinstance(liste, list):

			for joueur in liste:

				if joueur.coordonnee == self.carte.coord_sortie:

					return joueur

		else:

			if liste.coordonnee == self.carte.coord_sortie:

				return liste

		return None


if __name__ == '__main__':
	a = Application_labyrinthe()
	a.chargement_carte(choix = "0")