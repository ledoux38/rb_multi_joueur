#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 
import socket as st

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
	def __init__(self, coordonnee_xy_robot = (0, 0), forme_robot = "X", connexion = None):

		"""instancie le Robot.
		le robot est representer par une forme (X) et des coordonnes XY
		"""

		self.robot = rt.Robot(coordonnee_xy_robot, forme_robot)
		print("type connexion:{}".format(type(connexion)))
		self._information_connexion = connexion



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		msg = "client{}: {}".format(self._information_connexion, self.robot)
		return msg



	def __del__(self):
		"""Méthode appelée quand on souhaite supprimer la classe Connexion
		l'objectif et de pouvoir fermer la connexion la classe"""
		#self._information_connexion.close()
		pass



	def _set_information_connexion(self, connexion):
		"""Méthode appelée quand on souhaite modifier les informations de connexion
		mais comme je ne souhaite pas qu'elle soit modifiée je ne mais rien"""
		if isinstance(self._information_connexion, None):
			if not isinstance(connexion, st.socket):
					raise TypeError("""Erreur dans la classe Connexion!
									le parametre fourni à Connexion doit etre de type <socket> et non <{}>""".format(type(connexion)))
		else:
			pass



	def _get_information_connexion(self):
		print("connexion: ", type(self._information_connexion))
		"""Méthode appelée quand on souhaite modifier la forme du robot"""
		return self._information_connexion



	information_connexion = property(fget = _get_information_connexion, fset = _set_information_connexion)




if __name__ == "__main__":

	a = Connexion()
	print(a.robot)
	#a = Robot(coordonnee_XY = (2, 3))
	#a.forme_robot = "Y"
	b = a._information_connexion
	print(b)
