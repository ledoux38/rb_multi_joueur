#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

try:
	import package.Gestionnaire_entree_sortie_donnee as ES
except:
	import Gestionnaire_entree_sortie_donnee as ES


try:
	import package.utilitaires as utils
except:
	import utilitaires as utils

class Carte:
	"""Objet de transition entre un fichier et un labyrinthe."""

	def __init__(self, nom, chaine):
		"""procedure d'initialisation
		la classe comporte comme attribut: - nom <str>
											- chaine <str>
		"""

		if not isinstance(nom,str):
			raise TypeError("erreur le typage de la variable nom doit etre de type <str> et non <{}>".format(type(nom)))

		if not isinstance(chaine,str):
			raise TypeError("erreur le typage de la variable chaine doit etre de type <str> et non <{}>".format(type(chaine)))

		self.nom = nom
		self.labyrinthe = self.creer_labyrinthe_depuis_chaine(chaine)
		self.bordure_labyrinthe()



	def __repr__(self):
		return "<Carte {}>".format(self.nom)



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		msg = "{} \n <Carte: {}>".format(self.representation_labyrinthe_str(), self.nom)
		return msg



	def creer_labyrinthe_depuis_chaine(self,chaine):
		""" je cree une list de list pour cree le labyrinthre"""
		i = chaine + "\n"
		ligne = []
		labyrinthe = []


		for y,x in enumerate(i):

			if x != "\n":
				ligne.append(x)

			else:
				ligne.append(x)
				labyrinthe.append(ligne)
				ligne = []

		return labyrinthe



	def representation_labyrinthe_tableau(self):
		"""representation du labyrinthe en tableau"""
		for x in self.labyrinthe:
			print(x)



	def representation_labyrinthe_str(self):
		"""representation du labyrinthe en chaine de caractere"""
		chaine=str()
		for x in self.labyrinthe:
			for y in x:
				chaine += y
		return chaine



	def get_la_valeur_aux_coordonnees(self,coordonnee):
		"""on recupere la valeur directement au coordonnee choisi"""
		valeur = self.labyrinthe[coordonnee[0]][coordonnee[1]]
		return valeur



	def set_la_valeur_aux_coordonnee(self,valeur,coordonneeYX):
		"""on modifie la valeur au coordonnée choisi"""
		self.labyrinthe[coordonneeYX[0]][coordonneeYX[1]] = valeur



	def get_les_coordonnees_de_la_valeur(self,valeur="X"):
		"""retourne les coordonnee de la valeur trouvé.
		par defaut la valeur a chercher c'est X"""
		liste = list()
		for j,y in enumerate(self.labyrinthe):
			for v,x in enumerate(y):
				if x == valeur:
					liste.append(j)
					liste.append(v)
		return liste



	def bordure_labyrinthe(self):

		for i, y in enumerate(self.labyrinthe):
			self.labyrinthe[i].insert( 0, "O")
			self.labyrinthe[i].insert( -1, "O")

		self.labyrinthe.insert( 0, self.bordure_principale( len( self.labyrinthe[0] ) ) )
		self.labyrinthe.insert( -1, self.bordure_principale( len( self.labyrinthe[-1] ) ) )




	def bordure_principale(self, taille):
		bordure = []
		i = 0
		while i < taille-1:
			bordure.append("O")
			i += 1
		bordure.append("\n")
		return bordure



if __name__ == '__main__':

	a = utils.chargement_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
	labyrinthe = a[1]
	nom_labyrinthe = a[0]
	#print(labyrinthe, nom_labyrinthe)

	a = Carte(nom_labyrinthe, labyrinthe)
	a.representation_labyrinthe_tableau()
	print(a)
	"""
	Carte(a[0], a[1])
	print(a)
	"""