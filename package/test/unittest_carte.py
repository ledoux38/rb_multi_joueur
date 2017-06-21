#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
import sys
sys.path[:0] = ['./']

try:
	import package.Gestionnaire_entree_sortie_donnee as ES
except:
	import Gestionnaire_entree_sortie_donnee as ES

try:
	import package.utilitaires as utils
except:
	import utilitaires as utils

try:
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c


try:
	import package.carte as c
except:
	import carte as c

import unittest

import copy

import random  
 


class test_carte (unittest.TestCase):

	def setUp(self):
		dossier = ES.Gestionnaire_entree_sortie_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
		
		labyrinthe = dossier.chargement_donnee("facile.txt")

		nom_labyrinthe = "a[0]"
		
		self.a = c.Carte(nom_labyrinthe, labyrinthe)



	def tearDown(self):

		print("\n")



	def test_getitem(self):
		
		valeur_1 = self.a[0][0]

		self.assertEqual(valeur_1, self.a.labyrinthe[0][0])

		valeur_2 = self.a[2][2]

		self.assertEqual(valeur_2, self.a.labyrinthe[2][2])

		valeur_3 = self.a[5][5]

		self.assertEqual(valeur_3, self.a.labyrinthe[5][5])



	def test_setitem(self):

		self.a[0][0] = e_c.Joueur()

		self.assertEqual(type(e_c.Joueur()), type(self.a.labyrinthe[0][0]))		



	def test_rechercher_les_coordonnees_des_valeurs(self):
		
		liste = self.a.rechercher_les_coordonnees_des_valeurs(e_c.Porte())
		
		liste_reel = [(3, 3), (5, 9), (7, 9), (10, 3)]

		self.assertEqual(liste, liste_reel)

		liste = self.a.rechercher_les_coordonnees_des_valeurs(e_c.Sortie())
		
		liste_reel = [(6, 10)]

		self.assertEqual(liste, liste_reel)



	def test_liste_valeurs_par_lignes(self):

		retour = self.a.liste_valeurs_par_lignes(valeur = e_c.Couloir())

		liste_reel_debut = [(2, 2), (2, 4), (2, 5), (2, 6), (2, 7), (2, 9)]

		liste_reel_fin = [(10, 2), (10, 4), (10, 6), (10, 7), (10, 8), (10, 9)]

		self.assertEqual(retour[0],liste_reel_debut)
		
		self.assertEqual(retour[-1],liste_reel_fin)



	def test_positionement_aleatoire(self):

		joueur1 = e_c.Joueur()

		joueur2 = e_c.Joueur()

		self.a.positionement_aleatoire(joueur1)
		
		self.a.positionement_aleatoire(joueur2)

		coord1 = joueur1.coordonnee

		coord2 = joueur2.coordonnee

		self.assertEqual(id(joueur1),id(self.a[coord1[0]][coord1[1]]))
		
		self.assertEqual(joueur2,self.a[coord2[0]][coord2[1]])	



	def test_liste_coordonne_en_point_cardinaux(self):

		joueur1 = e_c.Joueur()

		self.a.positionement_aleatoire(joueur1)

		liste = self.a.liste_coordonne_en_point_cardinaux(coord = joueur1.coordonnee)



	def test_rechercher_liste_valeurs(self):

		liste_objet = self.a.rechercher_liste_valeurs(e_c.Sortie())[0]

		coord_objet = self.a.rechercher_les_coordonnees_des_valeurs(e_c.Sortie())[0]

		objet = self.a[coord_objet[0]] [coord_objet[1]]

		self.assertEqual(id(liste_objet), id(objet))

		liste_objet = self.a.rechercher_liste_valeurs(e_c.Porte())

		self.assertEqual(len(liste_objet), 4)

		self.assertEqual(type(liste_objet[0]), type(e_c.Porte()))
		
		self.assertEqual(type(liste_objet[1]), type(e_c.Porte()))

		self.assertEqual(type(liste_objet[2]), type(e_c.Porte()))

		self.assertEqual(type(liste_objet[3]), type(e_c.Porte()))


	"""
	def test_dfsV2(self):

		for i in retour:

			for j in i:

				if j == -1:

					print("#", end = "")

				elif j >= 10:

					print("*", end = "")

				else:

					print(j, end = "")

			print("")
		

		liste_valeur_max = []

		for y, r in enumerate(retour):
			for x, v in enumerate(r):
				if not v == 999:
					liste_valeur_max.append(((y, x),v))

		valeur = []

		for i in liste_valeur_max:
			valeur.append(i[1])

		print(liste_valeur_max)

		print(valeur)

	"""

if __name__ == '__main__':

	unittest.main()

