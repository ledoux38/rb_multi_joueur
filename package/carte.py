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


try:
	import package.elements_de_carte as el_carte
except:
	import elements_de_carte as el_carte


try:
	import package.tableau_carte 
except:
	import tableau_carte

import copy

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
		self.labyrinthe = tableau_carte.Tableau_carte(self.creer_labyrinthe_depuis_chaine(chaine))



	def __repr__(self):
		return "<Carte {}>".format(self.nom)



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""

		return "{}".format(self.labyrinthe)


	def creer_labyrinthe_depuis_chaine(self,chaine):
		"""Méthode appelée quand on souhaite creer le labyrinthe"""
		
		#je cree une list de list pour cree le labyrinthre
		i = chaine + "\n"
		ligne = []
		labyrinthe = []

		#je remplit le tableau par des chaines de caracteres
		for y,x in enumerate(i):

			if x != "\n":
				if x == "O":
					ligne.append(el_carte.Mur())
				elif x == " ":
					ligne.append(el_carte.Couloir())
				elif x == ".":
					ligne.append(el_carte.Porte())
				elif x == "X":
					ligne.append(el_carte.Joueur())
				elif x == "U":
					ligne.append(el_carte.Sortie())
				else:
					print("erreur lettre non reconnu par le programme")

			else:
				labyrinthe.append(ligne)
				ligne = []
		return labyrinthe



	def recherche_la_valeur_aux_coordonnees(self,coordonnee):
		"""on recupere la valeur directement au coordonnee choisi"""
		valeur = self.labyrinthe[(coordonnee[0],coordonnee[1])]
		return valeur



	def modifie_la_valeur_aux_coordonnees(self, valeur, coordonnee):
		"""on modifie la valeur au coordonnée choisi"""

		self.labyrinthe[(coordonnee[0],coordonnee[1])] = valeur



	def recherche_les_coordonnees_des_valeurs(self, valeur):
		"""retourne les coordonnee de la valeur trouvé."""

		liste = list()
		for j,y in enumerate(self.labyrinthe):
			for v,x in enumerate(y):
					retour = self.labyrinthe[(j, v)]
					if isinstance(retour, type(valeur)):
						liste.append((j, v))
		return liste



	def bordure_labyrinthe(self):
		"""Méthode appelée quand on souhaite creer une bordure sur l'extremité du labyrinthe"""

		#je compte le nombre de case dans chaque ligne
		nombre = []
		for i, y in enumerate(self.labyrinthe):
			nombre.insert(-1, len(self.labyrinthe[i]))
		#je recupere le nombre de la plus grande ligne qui sera la valeur max
		nombre = max(nombre)

		for i, y in enumerate(self.labyrinthe):
			#j'insert a l'index zero de chaque ligne une bordure
			self.labyrinthe.tableau[i].insert( 0, el_carte.Bordure())
			j = len(self.labyrinthe[i])

			while j <= nombre:
				#si les bordures sont irreguliere on rajoute des couloirs pour avoir une ligne droite
				self.labyrinthe.tableau[i].append(el_carte.Couloir())
				j += 1

			#je rajoute la derniere bordure a la fin de chaque ligne
			self.labyrinthe.tableau[i].append(el_carte.Bordure())


		self.labyrinthe.tableau.insert( 0, self.bordure_principale( nombre + 2 ) )
		self.labyrinthe.tableau.append(self.bordure_principale( nombre +2 ) )



	def bordure_principale(self, taille):
		bordure = []
		i = 0
		while i <= taille-1:
			bordure.append(el_carte.Bordure())
			i += 1
		return bordure



	def modification_sur_copie_labyrinthe(self, coordonnee, copie_labyrinthe, valeur):
		#print(copie_labyrinthe)
		copie_labyrinthe[coordonnee[0]][coordonnee[1]] = valeur
		#return copie_labyrinthe

	#version avec le tableau du tableau

	def carte_pour_utilisateur(self, coordonnee_utilisateur):
		if not isinstance(coordonnee_utilisateur, tuple):
			raise TypeError("erreur le typage de la variable coordonnee_utilisateur doit etre de type <tuple> et non <{}>".format(type(nom)))
		copie_labyrinthe = copy.deepcopy(self.labyrinthe.tableau)

		liste_coordonnees = list(self.recherche_les_coordonnees_des_valeurs(el_carte.Joueur()))
		print(coordonnee_utilisateur)
		for coordonnee in liste_coordonnees:
			if coordonnee != coordonnee_utilisateur:
				self.modification_sur_copie_labyrinthe(coordonnee, copie_labyrinthe, el_carte.Autres_joueurs())

		chaine=str()
		for j,y in enumerate(copie_labyrinthe):
			for v,x in enumerate(y):
				chaine += str(copie_labyrinthe[j][v])
			chaine +="\n"
		return chaine



if __name__ == '__main__':

	a = utils.chargement_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
	labyrinthe = a[1]
	nom_labyrinthe = a[0]
	a = Carte(nom_labyrinthe, labyrinthe)
	#print(a)
	#print(a.recherche_la_valeur_aux_coordonnees((0, 0)))
	a.bordure_labyrinthe()
	#print(a)
	#a.modifie_la_valeur_aux_coordonnees(el_carte.Couloir(), (0, 0))
	#print(a)
	
	#print(a.recherche_les_coordonnees_des_valeurs(el_carte.Joueur()))
	print(a.carte_pour_utilisateur((4, 9)))
	print(a.labyrinthe)
	"""
	i = [ ["0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0"] ]
	for j,y in enumerate(i):
		for v,x in enumerate(y):
			if x == "0":
				i[j][v] = (el_carte.Mur((j, v)))
	
	for x in i:
		for y in x:
			print (y)
		print("\n")
	print
	"""

