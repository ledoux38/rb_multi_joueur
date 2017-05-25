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
	import package.tableau 
except:
	import tableau

import copy

import random  

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
		
		self.labyrinthe = tableau.Tableau(self.creer_labyrinthe_depuis_chaine(chaine))



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
				
				elif x == "U":
				
					ligne.append(el_carte.Sortie())
				
				else:
				
					ligne.append(el_carte.Couloir())

			else:
				
				labyrinthe.append(ligne)
				
				ligne = []
		
		return labyrinthe



	def rechercher_la_valeur_aux_coordonnees(self,coordonnee):
		"""on recupere la valeur directement au coordonnee choisi"""
		valeur = self.labyrinthe[(coordonnee[0],coordonnee[1])]
		
		return valeur



	def modifier_la_valeur_aux_coordonnees(self, valeur, coordonnee):
		"""on modifie la valeur au coordonnée choisi"""

		self.labyrinthe[(coordonnee[0],coordonnee[1])] = valeur



	def rechercher_les_coordonnees_des_valeurs(self, valeur):
		"""retourne les coordonnee de la valeur trouvé."""

		liste = list()
		
		for j,y in enumerate(self.labyrinthe):
			
			for v,x in enumerate(y):
					
					retour = self.labyrinthe[(j, v)]
					
					if isinstance(retour, type(valeur)):
					
						liste.append((v, j))
		
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
				
				self.labyrinthe.tableau[i].append(el_carte.Bordure())
				
				j += 1

			#je rajoute la derniere bordure a la fin de chaque ligne
			self.labyrinthe.tableau[i].append(el_carte.Bordure())

		self.labyrinthe.tableau.insert( 0, self.bordure_principale( nombre + 2 ) )
		
		self.labyrinthe.tableau.append(self.bordure_principale( nombre +2 ) )



	def bordure_principale(self, taille):
		"""Méthode appelée quand on souhaite creer la premiere et derniere bordure sur l'extremité du labyrinthe"""
		bordure = []
		
		i = 0
		
		while i <= taille-1:
		
			bordure.append(el_carte.Bordure())
		
			i += 1
		
		return bordure



	def carte_utilisateur(self, coordonnee_utilisateur):
		"""Méthode appelée quand on souhaite creer une carte pour un utilisateur"""
		if not isinstance(coordonnee_utilisateur, tuple):

			raise TypeError("erreur le typage de la variable coordonnee_utilisateur doit etre de type <tuple> et non <{}>".format(type(nom)))
		
		copie_labyrinthe = tableau.Tableau(self.labyrinthe.tableau)

		liste_coordonnees = list(self.rechercher_les_coordonnees_des_valeurs(el_carte.Joueur()))

		for coordonnee in liste_coordonnees:
			
			if coordonnee != coordonnee_utilisateur:
				
				copie_labyrinthe[coordonnee[0]][coordonnee[1]] = el_carte.Autres_joueurs()

		return copie_labyrinthe.tableau_en_str()



	def initialisation_carte(self):
		"""Méthode appelée quand on souhaite supprimer les joueurs existant sur la carte et positionner les joueurs aleatoirement"""
		liste = self.rechercher_les_coordonnees_des_valeurs(valeur = el_carte.Joueur())

		for i in liste:

			self.modifier_la_valeur_aux_coordonnees(coordonnee = i, valeur = el_carte.Couloir())

		for Y,y in enumerate(self.labyrinthe):

			for X,x in enumerate(y):

				self.labyrinthe[Y][X].coordonnee = (Y,X)



	def liste_valeurs_par_lignes (self, tableau, valeur):
		"""Méthode appelée quand on souhaite creer liste de zone d'apparition autorisé"""
		liste = list()

		ligne = list()

		for j,y in enumerate(tableau):

			for x in y:

				if isinstance(x, type(valeur)):

					ligne.append(x.coordonnee)

			if not ligne == []:

				liste.append(ligne)

			ligne = []

		return liste



	def positionement_aleatoire(self):
		"""Méthode appelée quand on souhaite faire un positionnement aleatoire des joueurs"""

		liste_coordonnee = self.liste_valeurs_par_lignes(self.labyrinthe, el_carte.Couloir())

		coordonnee = random.choice(liste_coordonnee[0])

		self.modifier_la_valeur_aux_coordonnees(coordonnee = coordonnee, valeur = el_carte.Joueur(coordonnee = coordonnee))



if __name__ == '__main__':

	a = utils.chargement_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
	labyrinthe = a[1]
	nom_labyrinthe = a[0]
	a = Carte(nom_labyrinthe, labyrinthe)
	print(a)
	#print(a.rechercher_la_valeur_aux_coordonnees((0, 0)))
	a.bordure_labyrinthe()
	a.initialisation_carte()
	print(a)
	a.positionement_aleatoire()
	print(a)
	#print(a)
	#a.modifier_la_valeur_aux_coordonnees(el_carte.Couloir(), (0, 0))
	#print(a)
	
	#print(a.rechercher_les_coordonnees_des_valeurs(el_carte.Joueur()))
	#print(a.carte_utilisateur((4, 9)))
	#print(a.labyrinthe)
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

