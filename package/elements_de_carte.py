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
		"""Méthode appelée quand on souhaite afficher la classe"""
		
		msg = "{}".format(self.forme)
		
		return msg


class Joueur(Elements_de_carte):
	"""clase qui represente le joueur"""

	def __init__(self, coordonnee = (0, 0)):
		
		Elements_de_carte.__init__(self, coordonnee = coordonnee)
		
		self.forme = "X" #"\e[32mX\e[0m"
		
		self.element_nouvelle_position = Couloir(coordonnee = coordonnee)


class Autres_joueurs(Elements_de_carte):
	"""clase qui represente les autres joueurs"""

	def __init__(self):

		Elements_de_carte.__init__(self)

		self.forme = "x"



class Obstacle(Elements_de_carte):
	"""clase qui represente les Obstacle du jeux"""

	def __init__(self):

		Elements_de_carte.__init__(self)

		self.forme = "O"

		self.destructible = False



class Porte(Elements_de_carte):
	"""clase qui represente les portes du jeux"""

	def __init__(self):

		Elements_de_carte.__init__(self)

		self.forme = "."

		self.traversant = True



class Couloir(Elements_de_carte):
	"""clase qui represente les portes du jeux"""

	def __init__(self, coordonnee = (0, 0)):

		Elements_de_carte.__init__(self, coordonnee = coordonnee)

		self.forme = " "

		self.traversant = True



class Sortie(Elements_de_carte):
	"""clase qui represente la sortie du jeux"""
	def __init__(self):

		Elements_de_carte.__init__(self)

		self.forme = "U"

		self.traversant = True



