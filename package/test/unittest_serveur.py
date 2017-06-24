#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import sys
sys.path[:0] = ['./']

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

try:
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c 

try:
	import package.serveur as s
except:
	import serveur as s 


class test_serveur (unittest.TestCase):

	def setUp(self):

		self.a = s.Serveur("127.0.0.1", 12100)



	def tearDown(self):

		self.a.connexion.close()

		for i in self.a.app.g_clients:

			i.information_connexion.close()



	"""def test_app_labyrinthe(self):

		self.a.app_labyrinthe()
	"""

	def test_labyrinthe(self):

		self.a.app_labyrinthe()
		"""

		self.a.phase_chargement_carte()

		print("carte chargée!\n en attente de clients")

		self.a.attente_de_connexion()

		boucle = True

		while boucle:

			for connexion in self.a.app.g_clients:

				if self.a.phase_mouvement_joueur(connexion):

					prep_inter_utilisateur = "felicitation vous avez gagné"

					self.a.emission_donnee(connexion.information_connexion, prep_inter_utilisateur)

					boucle = False

					break

		for connexion in self.a.app.g_clients:

			connexion.information_connexion.close()
	
		self.a.connexion.close()
		"""


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