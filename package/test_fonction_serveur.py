#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

try:
	import package.serveur as sr
except:
	import serveur as sr

import unittest as ut

class test_serveur(ut.TestCase):
	def setUp(self):
		pass
		#self.a = Serveur()
	def tearDown(self):
		pass
		#self.a.connexion.close()

	def test_instance(self):
		self.a = sr.Serveur("127.0.0.1", 12500)
		self.assertIsInstance(self.a, sr.Serveur)

if __name__ == "__main__":
	ut.main()
