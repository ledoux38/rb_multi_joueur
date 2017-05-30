#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

class Elements_de_carte():
	"""la classe Elements_de_carte et une classe de base pour les autres classe(Joueur, Mur, Bordure, Porte, Couloir)"""
	def __init__(self, coordonnee = (0, 0)):


		self.destructible = False
		self.traversant = False
		self.forme = ""
		self.coordonnee = coordonnee



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		msg = "{}".format(self.forme)
		return msg


	"""
	def __getitem__():
		print("coucou")
		return self.forme
	"""


class Joueur(Elements_de_carte):
	def __init__(self, coordonnee = (0, 0)):
		Elements_de_carte.__init__(self, coordonnee = coordonnee)
		self.forme = "X"
		self.element_nouvelle_position = Couloir(coordonnee = coordonnee)


class Autres_joueurs(Elements_de_carte):
	def __init__(self):
		Elements_de_carte.__init__(self)
		self.forme = "x"



class Obstacle(Elements_de_carte):
	def __init__(self):
		Elements_de_carte.__init__(self)
		self.forme = "O"
		self.destructible = False



class Porte(Elements_de_carte):
	def __init__(self):
		Elements_de_carte.__init__(self)
		self.forme = "."
		self.traversant = True



class Couloir(Elements_de_carte):
	def __init__(self, coordonnee = (0, 0)):
		Elements_de_carte.__init__(self, coordonnee = coordonnee)
		self.forme = " "
		self.traversant = True



class Sortie(Elements_de_carte):
	def __init__(self):
		Elements_de_carte.__init__(self)
		self.forme = "U"
		self.traversant = True



if __name__ == "__main__":

	#a = Elements_de_carte()
	a = Joueur(coordonnee = (4, 2))
	print(a)
	a = Mur()
	print(a)
	a = Bordure()
	print(a)
	a = Porte()
	print(a)
	a = Couloir()
	print(a)
