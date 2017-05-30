#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

try:
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c

class Connexion:

	"""la classe Connexion et une classe qui est crée pour représenter un joueur. elle permet de créer une entitée de type Robot
	avec position X, Y et une forme
	mais aussi garder en mémoire la connexion ainsi que l'adresse (IP/ port)

	ATTRIBUTS:	- Joueur
				- information_connexion

	"""
	def __init__(self, connexion = None):

		"""instancie le Robot.
		le joueur est representer par une forme (X) et des coordonnes XY
		"""

		self.joueur = e_c.Joueur()

		self.information_connexion = connexion



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe joueur"""
		
		msg = "client {}: {}".format(self.information_connexion, self.joueur)
		
		return msg



if __name__ == "__main__":

	a = Connexion()
	print(a)
	#a = Robot(coordonnee_XY = (2, 3))
	#a.forme_joueur = "Y"
	b = a.information_connexion
	print(b)
