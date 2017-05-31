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
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c


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
		
		self.labyrinthe = list(self.initialisation(chaine))

		self.coord_sortie = self.rechercher_les_coordonnees_des_valeurs(e_c.Sortie())


	def __str__(self):
		"""Méthode appelée quand on souhaite afficher le tableau via un print()"""
		
		return self.tableau_en_str()



	def __getitem__(self, keys): 
		"""Méthode appelée quand on souhaite recuperer une valeur d'un tableau"""
		
		return self.labyrinthe[keys]



	def __setitem__(self, keys, valeur):
		"""Méthode appelée quand on souhaite modifier une valeur d'un tableau"""
		
		self.labyrinthe[keys] = valeur



	def tableau_en_str(self):
		"""Méthode appelée quand on souhaite recuperer le tableau en chaine de caractere"""
		
		chaine=str()
		
		for j,y in enumerate(self.labyrinthe):
			
			for v,x in enumerate(y):
				
				chaine += str(self.labyrinthe[j][v])
			
			chaine +="\n"
		
		return chaine



	def initialisation(self,chaine):
		"""Méthode appelée quand on souhaite creer le labyrinthe"""
		
		#je cree une list de list pour cree le labyrinthre
		i = chaine + "\n"
		
		ligne = []
		
		labyrinthe = []

		#je remplis le tableau d'objets
		for y,x in enumerate(i):

			if x != "\n":
				
				if x == "O":
				
					ligne.append(e_c.Obstacle())
				
				elif x == " ":
				
					ligne.append(e_c.Couloir())
				
				elif x == ".":
				
					ligne.append(e_c.Porte())
				
				elif x == "U":
				
					ligne.append(e_c.Sortie())
				
				else:
				
					ligne.append(e_c.Couloir())

			else:
				
				labyrinthe.append(ligne)
				
				ligne = []
		
		# mise en place des coordonnées dans les objets		
		for Y,y in enumerate(labyrinthe):

			for X,x in enumerate(y):

				labyrinthe[Y][X].coordonnee = (Y,X)		

		return labyrinthe



	def reinitialisation_des_coordonnees_des_objets(self):
		for Y,y in enumerate(self.labyrinthe):

			for X,x in enumerate(y):

				self.labyrinthe[Y][X].coordonnee = (Y,X)



	def rechercher_les_coordonnees_des_valeurs(self, valeur):
		"""retourne les coordonnee de la valeur trouvé."""

		liste = list()
		
		for j,y in enumerate(self.labyrinthe):
			
			for v,x in enumerate(y):
					
					retour = self.labyrinthe[j][v]
					
					if isinstance(retour, type(valeur)):
					
						liste.append((j, v))

		if len(liste) > 1:

			return liste

		else:
			return liste[0]



	def rechercher_liste_valeurs(self, valeur):
		"""retourne les coordonnee de la valeur trouvé."""

		liste = list()
		
		for j,y in enumerate(self.labyrinthe):
			
			for v,x in enumerate(y):
					
					retour = self.labyrinthe[j][v]
					
					if isinstance(retour, type(valeur)):
					
						liste.append(retour)

		if len(liste) > 1:

			return liste

		else:
			return liste[0]	

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
			
			self.labyrinthe[i].insert( 0, e_c.Obstacle())
			
			j = len(self.labyrinthe[i])

			while j <= nombre:
				#si les bordures sont irreguliere on rajoute des couloirs pour avoir une ligne droite
				
				self.labyrinthe[i].append(e_c.Obstacle())
				
				j += 1

			#je rajoute la derniere bordure a la fin de chaque ligne
			self.labyrinthe[i].append(e_c.Obstacle())

		self.labyrinthe.insert( 0, self.bordure_principale( nombre + 2 ) )
		
		self.labyrinthe.append(self.bordure_principale( nombre +2 ) )

		#reinitialisation des objets
		self.reinitialisation_des_coordonnees_des_objets()



	def bordure_principale(self, taille):
		"""Méthode appelée quand on souhaite creer la premiere et derniere bordure sur l'extremité du labyrinthe"""
		bordure = []
		
		i = 0
		
		while i <= taille-1:
		
			bordure.append(e_c.Obstacle())
		
			i += 1
		
		return bordure



	def carte_utilisateur(self, coordonnee_utilisateur):
		"""Méthode appelée quand on souhaite creer une carte pour un utilisateur"""
		if not isinstance(coordonnee_utilisateur, tuple):

			raise TypeError("erreur le typage de la variable coordonnee_utilisateur doit etre de type <tuple> et non <{}>".format(type(nom)))
		
		copie_labyrinthe = copy.deepcopy(self.labyrinthe)

		liste_coordonnees = list(self.rechercher_les_coordonnees_des_valeurs(e_c.Joueur()))

		for coordonnee in liste_coordonnees:
			
			if coordonnee != coordonnee_utilisateur:
				
				copie_labyrinthe[coordonnee[0]][coordonnee[1]] = e_c.Autres_joueurs()

		chaine=str()

		for j,y in enumerate(copie_labyrinthe):

			for v,x in enumerate(y):

				chaine += str(copie_labyrinthe[j][v])

			chaine +="\n"

		return chaine



	def liste_valeurs_par_lignes (self, valeur):
		"""Méthode appelée quand on souhaite creer liste de zone d'apparition autorisé"""
		liste = list()

		ligne = list()

		for j,y in enumerate(self.labyrinthe):

			for x in y:
				#if isinstance(x, type(valeur)):
				if type(x) == type(valeur):

					ligne.append(x.coordonnee)

			if not ligne == []:

				liste.append(ligne)

			ligne = []

		return liste



	def positionement_aleatoire(self, joueur):
		"""Méthode appelée quand on souhaite faire un positionnement aleatoire des joueurs"""

		liste_coordonnee = self.liste_valeurs_par_lignes(e_c.Couloir())

		coordonnee = random.choice(liste_coordonnee[0])

		joueur.coordonnee = coordonnee

		self.labyrinthe[coordonnee[0]][coordonnee[1]] = joueur



	def liste_coordonne_en_point_cardinaux(self, coordonnee):
		liste = []
		#NORD
		if isinstance(self.labyrinthe[coordonnee[0]-1][coordonnee[1]], e_c.Couloir):

			liste.append(True)

		else:

			liste.append(False)

		#EST
		if isinstance(self.labyrinthe[coordonnee[0]][coordonnee[1]+1], e_c.Couloir):

			liste.append(True)

		else:

			liste.append(False)

		#SUD
		if isinstance(self.labyrinthe[coordonnee[0]+1][coordonnee[1]], e_c.Couloir):

			liste.append(True)

		else:

			liste.append(False)

		#OUEST
		if isinstance(self.labyrinthe[coordonnee[0]][coordonnee[1]-1], e_c.Couloir):

			liste.append(True)

		else:

			liste.append(False)

		return liste



if __name__ == '__main__':

	a = utils.chargement_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
	labyrinthe = a[1]
	nom_labyrinthe = a[0]
	a = Carte(nom_labyrinthe, labyrinthe)
	print(a)
	a.bordure_labyrinthe()
	#a.initialisation_carte()
	print(a)
	a.positionement_aleatoire()
	print(a)
	#print(a)

	#print(a)
	
	#print(a.rechercher_les_coordonnees_des_valeurs(e_c.Joueur()))
	#print(a.carte_utilisateur((4, 9)))
	#print(a.labyrinthe)
	"""
	i = [ ["0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0"] ]
	for j,y in enumerate(i):
		for v,x in enumerate(y):
			if x == "0":
				i[j][v] = (e_c.Obstacle((j, v)))
	
	for x in i:
		for y in x:
			print (y)
		print("\n")
	print
	"""

