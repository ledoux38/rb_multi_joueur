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
	import package.connexion as c_n
except:
	import connexion as c_n

import copy

import unittest




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

		liste = self.carte.liste_coordonne_en_point_cardinaux(coord = joueur.coordonnee)

		chaine = "proposition de deplacement:\n"

		for mvt in liste:

			chaine += "{}".format(mvt)

		return chaine



	def mouvement_joueur(self, joueur, mouvement):
		"""fonction qui va deplacer le joueurs sur la carte"""

		if not mouvement in "NSEW":
			raise ValueError( "mouvement != 'NSEW' ")

		coord_j = joueur.coordonnee

		obj = None

		dic = {"N":(-1,0), "E":(0,1), "S":(1,0), "O":(0,-1)}


		obj = self.carte [coord_j[0] + dic[mouvement][0] ] [coord_j[1] + dic[mouvement][1] ]

		if isinstance(obj, e_c.Couloir) or isinstance(obj, e_c.Porte) or isinstance(obj, e_c.Sortie):

			copie_objet = copy.deepcopy(joueur.element_nouvelle_position)
			
			joueur.coordonnee = obj.coordonnee

			joueur.element_nouvelle_position = obj

			self.carte[joueur.coordonnee[0]][joueur.coordonnee[1]] = joueur

			self.carte[copie_objet.coordonnee[0]][copie_objet.coordonnee[1]] = copie_objet

		else:

			raise TypeError("Erreur objet carte != e_c.Couloir")



	def verification_de_victoire(self):
		"""fonction qui à pour but de verifier si il y a victoire"""

		liste = self.carte.rechercher_liste_valeurs(e_c.Joueur())

		if isinstance(liste, list):

			for joueur in liste:

				if joueur.coordonnee == self.carte.sortie.coordonnee:

					return joueur

		else:

			if liste.coordonnee == self.carte.coord_sortie:

				return liste

		return None


class test_app_labyrinthe (unittest.TestCase):



	def setUp(self):

		self.classe_app_lab =  Application_labyrinthe()



	def tearDown(self):

		print("\n")



	def test_appelle_fonction(self):

		a = self.classe_app_lab.g_clients

		b = self.classe_app_lab.carte

		self.assertEqual(type(a), type(g_c.Gestionnaire_clients()))

		self.assertEqual(b, None)



	def test_rajouter_connexion(self):

		self.classe_app_lab.g_clients += ["127.0.0.1",12800]

		a = self.classe_app_lab.g_clients[0]

		self.assertEqual(["127.0.0.1",12800], a)



	def test_recuperer_nb_connexion(self):

		self.classe_app_lab.g_clients += ["127.0.0.1",12800]

		self.classe_app_lab.g_clients += ["127.0.0.2",12800]

		self.classe_app_lab.g_clients += ["127.0.0.3",12800]

		self.assertEqual(3, len(self.classe_app_lab.g_clients))

		self.assertEqual(3, len(self.classe_app_lab))



	def test_supprimer_une_connexion(self):

		self.classe_app_lab.g_clients += ["127.0.0.1",12800]

		a = self.classe_app_lab.g_clients[0]

		self.assertEqual(["127.0.0.1",12800], a)

		self.classe_app_lab.g_clients.supprimer_connexion(0)

		self.assertEqual(0, len(self.classe_app_lab))



	def test_validation_reponse_joueurs(self):
		
		reponse = "0"
		
		action = ["0","1","2"]

		self.assertTrue(self.classe_app_lab.validation_reponse_joueurs(reponse,action))

		reponse = "02"
		
		action = ["0","1","2"]

		self.assertFalse(self.classe_app_lab.validation_reponse_joueurs(reponse,action))



	def test_chargement_carte(self):

		self.classe_app_lab.chargement_carte(choix = "0")

		echantillion_a = self.classe_app_lab.carte[0][0]

		self.assertEqual(type(echantillion_a), type(e_c.Obstacle()))

		echantillion_a = self.classe_app_lab.carte[5][5]

		self.assertEqual(type(echantillion_a), type(e_c.Obstacle()))



	def test_proposition_de_deplacement(self):

		joueur1 = c_n.Connexion().joueur

		self.classe_app_lab.chargement_carte(choix = "1")

		self.classe_app_lab.carte.positionement_aleatoire(joueur1)	

		retour = self.classe_app_lab.proposition_de_deplacement(joueur1)

		self.assertEqual(retour, "proposition de deplacement:\n<S>")



	def test_mouvement_joueur(self):

		joueur1 = c_n.Connexion().joueur

		self.classe_app_lab.chargement_carte(choix = "1")
		
		self.classe_app_lab.carte.positionement_aleatoire(joueur1)	

		self.classe_app_lab.mouvement_joueur(joueur1, "S")

		self.assertEqual( type( self.classe_app_lab.carte[1][1] ), type( e_c.Obstacle() ) )



	def test_verification_de_victoire(self):

		joueur1 = c_n.Connexion().joueur

		self.classe_app_lab.chargement_carte(choix = "1")
		
		self.classe_app_lab.carte.positionement_aleatoire(joueur1)	

		self.classe_app_lab.mouvement_joueur(joueur1, "S")

		victoire = self.classe_app_lab.verification_de_victoire()

		self.assertEqual(type(victoire), type(e_c.Joueur()))



if __name__ == "__main__":

	unittest.main()