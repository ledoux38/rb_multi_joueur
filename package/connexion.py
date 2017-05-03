#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

try:
	import package.robot as rt
except:
	import robot as rt


class Connexion:

	"""la classe Connexion et une classe qui est crée pour représenter un joueur. elle permet de créer une entitée de type Robot
	avec position X, Y et une forme
	mais aussi garder en mémoire la connexion ainsi que l'adresse (IP/ port)

	ATTRIBUTS:	- Robot
				- information_connexion

	"""
	def __init__(self, coordonnee_xy_robot = (0, 0), forme_robot = "X", connexion = []):

		"""instancie le Robot.
		le robot est representer par une forme (X) et des coordonnes XY
		"""
		if not isinstance(connexion, list):
				raise TypeError("""Erreur lors de l'instanciation de la classe Connexion!
					le parametre fourni à connexion doit etre de type <list> et non <{}>""".format(type(connexion)))

		self.robot = rt.Robot(coordonnee_xy_robot, forme_robot)
		self._information_connexion = connexion



	def _set_information_connexion(self, modification_connexion):
		"""Méthode appelée quand on souhaite modifier les information de connexion"""
		if not isinstance(connexion, list):
				raise TypeError("""Erreur lors de l'instanciation de la classe Connexion!
					le parametre fourni à connexion doit etre de type <list> et non <{}>""".format(type(connexion)))

		self._information_connexion = modification_connexion



	def _get_information_connexion(self):
		"""Méthode appelée quand on souhaite modifier la forme du robot"""
		return self._information_connexion



	information_connexion = property(fget = _get_information_connexion, fset = _set_information_connexion)




if __name__ == "__main__":

	a = Connexion()
	print(a.robot)
	#a = Robot(coordonnee_XY = (2, 3))
	#a.forme_robot = "Y"
