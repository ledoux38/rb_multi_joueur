#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

class Robot:
	"""la classe robot et une classe qui permet de cree une entité avec une position X et Y et une forme
		ATTRIBUTS:	- forme_robot
					- coordonnee_XY
					- ancien_caractere


	"""
	def __init__(self,coordonnee_XY = (0, 0), forme_robot = "X"):
		"""instancie le robot.
		le robot est representer par une forme (X) et des coordonnes XY
		"""


		if not isinstance(forme_robot,str):
			raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
				le parametre fourni à forme_robot doit etre de type <str> et non <{}>""".format(type(coordonnee_XY)))

		if not len(forme_robot) == 1:
			raise ValueError("""erreur parametre <{}> incorrect!
				nombre de caractere autorisé dans le parametre est de 1. EX:"X" """.format(forme_robot))
		
		if not isinstance(coordonnee_XY, tuple):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
					le parametre fourni à coordonnee_XY doit etre de type <tuple> et non <{}>""".format(type(coordonnee_XY)))

		for i in coordonnee_XY:
			if not isinstance(i,int):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
		argument dans list doit etre de type int et non <{}>""".format(type(i)))				

		if not len(coordonnee_XY) == 2:
			raise ValueError("""erreur parametre <{}> incorrect!
				nombre de d'axe autorisé dans le parametre est de 2. EX:"[X,Y]" """.format(coordonnee_XY))


		self._forme_robot = forme_robot
		self._coordonnee_XY = coordonnee_XY
		self._ancien_caractere = " "



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		msg = "{}".format(self.coordonnee_XY)
		return msg


	def __get__(self):
		"""Méthode appelée quand on souhaite recuperer la classe robot"""
		return self.coordonnee_XY


	def _set_forme_robot(self, nouvelle_forme):
		"""Méthode appelée quand on souhaite modifier la forme du robot"""

		if not isinstance(nouvelle_forme,str):
			raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
				le parametre fourni à forme_robot doit etre de type <str> et non <{}>""".format(type(coordonnee_XY)))

		if not len(nouvelle_forme) == 1:
			raise ValueError("""erreur parametre <{}> incorrect!
				nombre de caractere autorisé dans le parametre est de 1. EX:"X" """.format(nouvelle_forme))		

		self._forme_robot = nouvelle_forme



	def _get_forme_robot(self):
		"""Méthode appelée quand on souhaite lire la forme du robot"""
		return self._forme_robot



	def _set_coordonnee_XY(self, nouvelle_coordonnee_XY):
		"""Méthode appelée quand on souhaite modifier la forme du robot"""
		if not isinstance(nouvelle_coordonnee_XY, tuple):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
					le parametre fourni à coordonnee_XY doit etre de type <tuple> et non <{}>""".format(type(nouvelle_coordonnee_XY)))

		for i in nouvelle_coordonnee_XY:
			if not isinstance(i,int):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
		argument dans list doit etre de type int et non <{}>""".format(type(i)))				

		if not len(nouvelle_coordonnee_XY) == 2:
			raise ValueError("""erreur parametre <{}> incorrect!
				nombre de d'axe autorisé dans le parametre est de 2. EX:"[X,Y]" """.format(nouvelle_coordonnee_XY))

		self._coordonnee_XY = nouvelle_coordonnee_XY



	def _get_coordonnee_XY(self):
		"""Méthode appelée quand on souhaite lire coordonnee_XY"""
		return self._coordonnee_XY



	def _set_ancien_caractere(self, nouveau_caractere):
		"""Méthode appelée quand on souhaite modifier la forme du robot"""
		self._ancien_caractere = nouveau_caractere



	def _get_ancien_caractere(self):
		"""Méthode appelée quand on souhaite modifier la forme du robot"""
		return self._ancien_caractere



	forme_robot = property(fget = _get_forme_robot, fset = _set_forme_robot)
	coordonnee_XY = property(fget = _get_coordonnee_XY, fset = _set_coordonnee_XY)
	ancien_caractere = property(fget = _get_ancien_caractere, fset = _set_ancien_caractere)




if __name__ == "__main__":

	a = Robot()
	#a = Robot(coordonnee_XY = (2, 3))
	#a.forme_robot = "Y"
	print(a.forme_robot)
	#a.coordonnee_XY = (8, 8)
	#print(a.coordonnee_XY)
	print(a, type(a))
	b = a
	print(b, type(b))

