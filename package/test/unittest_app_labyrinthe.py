#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

from __future__ import absolute_import

import os,sys

dossier = os.path.dirname(os.path.abspath(__file__))
 
while not dossier.endswith('package'):
	dossier = os.path.dirname(dossier)
 
dossier = os.path.dirname(dossier)
 
if dossier not in sys.path:
	sys.path.append(dossier)




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


try:
	import package.application_labyrinthe as a_l
except:
	import application_labyrinthe as a_l


import copy

import unittest






class test_app_labyrinthe (unittest.TestCase):



	def setUp(self):

		self.classe_app_lab = a_l.Application_labyrinthe()



	def tearDown(self):

		print("\n")



	def test_appelle_fonction(self):

		a = self.classe_app_lab.g_clients

		b = self.classe_app_lab.carte

		self.assertEqual(type(a), type(g_c.Gestionnaire_clients()))

		self.assertEqual(b, None)



	def test_rajouter_connexion(self):

		self.classe_app_lab.g_clients += ["127.0.0.1",12800]

		a = self.classe_app_lab.g_clients[0].information_connexion

		self.assertEqual(["127.0.0.1",12800], a)



	def test_recuperer_nb_connexion(self):

		self.classe_app_lab.g_clients += ["127.0.0.1",12800]

		self.classe_app_lab.g_clients += ["127.0.0.2",12800]

		self.classe_app_lab.g_clients += ["127.0.0.3",12800]

		self.assertEqual(3, len(self.classe_app_lab.g_clients))

		self.assertEqual(3, len(self.classe_app_lab))



	def test_supprimer_une_connexion(self):

		self.classe_app_lab.g_clients += ["127.0.0.1",12800]

		a = self.classe_app_lab.g_clients[0].information_connexion

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



	def test_choix_carte(self):

		retour = self.classe_app_lab.choix_carte()

		retour_reel = """Bienvenue sur l'application l'Abyrinthe multi_joueurs.
 Veillez choisir la carte pour lancer la partie!
<0>: facile.txt
<1>: test.txt
<2>: prison.txt\n"""


		self.assertEqual(retour, retour_reel)

		retour = self.classe_app_lab.choix_carte(erreur = True)

		retour_reel = """Erreur lors de la saisi! 
 Bienvenue sur l'application l'Abyrinthe multi_joueurs.
 Veillez choisir la carte pour lancer la partie!
<0>: facile.txt
<1>: test.txt
<2>: prison.txt\n"""

		self.assertEqual(retour, retour_reel)



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

		retour, liste = self.classe_app_lab.proposition_de_deplacement(joueur1)

		liste_reel = ['S', 'MN', 'ME', 'MS', 'MO', 'PN', 'PE', 'PS', 'PO', 'QUIT']

		self.assertEqual(liste_reel, liste)





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

		self.classe_app_lab.mouvement_joueur(joueur1, "S")

		victoire = self.classe_app_lab.verification_de_victoire()

		self.assertEqual(type(victoire), type(e_c.Joueur()))



		




if __name__ == "__main__":

	unittest.main()