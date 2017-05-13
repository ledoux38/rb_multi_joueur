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
		chaine=str()
		for x in self.labyrinthe:
			for y in x:
				chaine += y



		msg = "{} \n <Carte: {}>".format(chaine, self.nom)
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



	def representation_labyrinthe_str(self, labyrinthe):
		"""representation du labyrinthe en chaine de caractere"""
		chaine=str()
		for x in labyrinthe:
			for y in x:
				chaine += y
		return chaine



	def recherche_la_valeur_aux_coordonnees(self,coordonnee):
		"""on recupere la valeur directement au coordonnee choisi"""
		valeur = self.labyrinthe[coordonnee[0]][coordonnee[1]]
		return valeur



	def modifie_la_valeur_aux_coordonnees(self, labyrinthe, valeur, coordonneeYX):
		"""on modifie la valeur au coordonnée choisi"""
		labyrinthe[coordonneeYX[0]][coordonneeYX[1]] = valeur
		return labyrinthe


	def recherche_les_coordonnees_des_valeurs(self,valeurs="X"):
		"""retourne les coordonnee de la valeur trouvé.
		par defaut la valeur a chercher c'est X"""
		liste = list()
		for j,y in enumerate(self.labyrinthe):
			for v,x in enumerate(y):
				if x == valeurs:
					coord = (j, v)
					liste.append(coord)
		return liste




	def bordure_labyrinthe(self):
		nombre = []
		for i, y in enumerate(self.labyrinthe):
			nombre.insert(-1, len(self.labyrinthe[i]))

		nombre = max(nombre)

		for i, y in enumerate(self.labyrinthe):
			self.labyrinthe[i].insert( 0, "O")
			j = len(self.labyrinthe[i])
			while j <= nombre:
				self.labyrinthe[i].insert( -1, " ")

				j += 1
			self.labyrinthe[i][-1] = "O"
			self.labyrinthe[i].append("\n")


		self.labyrinthe.insert( 0, self.bordure_principale( nombre + 2 ) )
		self.labyrinthe.append(self.bordure_principale( nombre +2 ) )




	def bordure_principale(self, taille):
		bordure = []
		i = 0
		while i < taille-1:
			bordure.append("O")
			i += 1
		bordure.append("\n")
		return bordure



	def carte_pour_utilisateur(self, coordonnee_utilisateur, valeur = "X"):
		if not isinstance(coordonnee_utilisateur, tuple):
			raise TypeError("erreur le typage de la variable coordonnee_utilisateur doit etre de type <tuple> et non <{}>".format(type(nom)))
		labyrinthe = self.labyrinthe
		liste_coordonnee = self.recherche_les_coordonnees_des_valeurs(valeur)
		print(liste_coordonnee)
		for coordonnee in liste_coordonnee:
			if coordonnee != coordonnee_utilisateur:
				labyrinthe = self.modifie_la_valeur_aux_coordonnees(labyrinthe, "x", coordonnee)
		return labyrinthe




if __name__ == '__main__':

	a = utils.chargement_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
	labyrinthe = a[1]
	nom_labyrinthe = a[0]
	#print(labyrinthe, nom_labyrinthe)

	a = Carte(nom_labyrinthe, labyrinthe)
	a.representation_labyrinthe_tableau()
	print(a)
	b = a.recherche_les_coordonnees_des_valeurs()[0]
	print(b)
	print(a.recherche_la_valeur_aux_coordonnees((4, 9)))
	print(a.representation_labyrinthe_str(a.carte_pour_utilisateur(coordonnee_utilisateur = (4, 9))))
	"""
	Carte(a[0], a[1])
	print(a)
	"""