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


	def test_labyrinthe(self):

		self.a.app_labyrinthe()


if __name__ == '__main__':

	unittest.main()

