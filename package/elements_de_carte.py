#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

class Elements_de_carte():
	"""la classe Elements_de_carte et une classe de base pour les autres classe(Joueur, Mur, Bordure, Porte, Couloir)"""
	def __init__(self, coordonnee):
		if not isinstance(coordonnee, tuple):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
					le parametre fourni à coordonnee doit etre de type <tuple> et non <{}>""".format(type(coordonnee)))

		for i in coordonnee:
			if not isinstance(i,int):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
		argument dans list doit etre de type int et non <{}>""".format(type(i)))	

		self.destructible = False
		self.traversant = False
		self.forme = ""
		self.coordonnee = coordonnee



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		msg = "destructible:{} traversant:{} forme:{} coordonnee:{}".format(self.destructible, self.traversant, self.forme, self.coordonnee)
		return msg



class Joueur(Elements_de_carte):
	def __init__(self, coordonnee):
		Elements_de_carte.__init__(self, coordonnee = coordonnee)
		self.forme = "X"
		self.element_avant_nouvelle_position = Couloir(coordonnee)



class Mur(Elements_de_carte):
	def __init__(self, coordonnee):
		Elements_de_carte.__init__(self,  coordonnee = coordonnee)
		self.forme = "O"
		self.destructible = True



class Bordure(Elements_de_carte):
	def __init__(self, coordonnee):
		Elements_de_carte.__init__(self,  coordonnee = coordonnee)
		self.forme = "O"



class Porte(Elements_de_carte):
	def __init__(self, coordonnee):
		Elements_de_carte.__init__(self,  coordonnee = coordonnee)
		self.forme = "."
		self.traversant = True



class Couloir(Elements_de_carte):
	def __init__(self, coordonnee):
		Elements_de_carte.__init__(self,  coordonnee = coordonnee)
		self.forme = " "
		self.traversant = True



if __name__ == "__main__":

	#a = Elements_de_carte()
	a = Joueur(coordonnee = (4, 2))
	print(a)
	a = Mur(coordonnee = (4, 2))
	print(a)
	a = Bordure(coordonnee = (4, 2))
	print(a)
	a = Porte(coordonnee = (4, 2))
	print(a)
	a = Couloir(coordonnee = (4, 2))
	print(a)
