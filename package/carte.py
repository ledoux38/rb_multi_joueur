#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

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

		self.bordure_labyrinthe()

		self.sortie = self.rechercher_liste_valeurs(e_c.Sortie())[0]

		self.list_posit_joueur = self.dfs()


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

		dictionnaire = {" ": e_c.Couloir, 
						".": e_c.Porte, 
						"U": e_c.Sortie, 
						"O": e_c.Obstacle, 
						"X": e_c.Couloir
						}

		i = chaine + "\n"
		
		ligne = []
		
		labyrinthe = []

		#je remplis le tableau d'objets	
		for x in i:

			if x != "\n":

				try:
					ligne.append(dictionnaire[x]())
					#print(dictionnaire[x])

				except KeyError:

					ligne.append(dictionnaire[" "]())
				
			else:
				
				labyrinthe.append(ligne)
				
				ligne = []		

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

		return liste



	def rechercher_liste_valeurs(self, valeur):
		"""retourne les coordonnee de la valeur trouvé."""

		liste = list()
		
		for j,y in enumerate(self.labyrinthe):
			
			for v,x in enumerate(y):
					
					retour = self.labyrinthe[j][v]
					
					if isinstance(retour, type(valeur)):
					
						liste.append(retour)

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
		
		#creation d'une copie de la carte
		copie_labyrinthe = copy.deepcopy(self.labyrinthe)

		#recuperation de la liste des autres joueur
		liste_coordonnees = list(self.rechercher_les_coordonnees_des_valeurs(e_c.Joueur()))

		for coordonnee in liste_coordonnees:
			
			if coordonnee != coordonnee_utilisateur:
				
				#modification des autres joueurs
				copie_labyrinthe[coordonnee[0]][coordonnee[1]] = "x"

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
		"""Méthode appelée quand on souhaite positionner le joueur sur la carte"""

		tab_v_max = []

		#recuperation de la liste des positionnements possibles
		for i in self.list_posit_joueur:
			tab_v_max.append(i[1])

		# pour eviter que les joueurs soit tous regrouper en ligne je donne un interval de 2 case à chaques joueurs
		if len(tab_v_max) > 4:

			maxi = max(tab_v_max)-2

		else:

			maxi = max(tab_v_max)

		ind = tab_v_max.index(maxi)

		#positionnement du joueur sur la carte
		coordonnee = self.list_posit_joueur[ind][0]

		joueur.coordonnee = coordonnee

		joueur.element_nouvelle_position.coordonnee = coordonnee

		self.labyrinthe[coordonnee[0]][coordonnee[1]] = joueur

		#suppression du choix dans la liste list_posit_joueur
		self.list_posit_joueur.remove((coordonnee, maxi))



	def liste_coordonne_en_point_cardinaux(self, coord):
		"""Méthode appelée quand on souhaite connaitre les coordonne de passage valide"""

		p_cardinaux = []

		liste_objet = []


		dic = {"N":(-1,0), "E":(0,1), "S":(1,0), "O":(0,-1)}

		for mvt in "NESO":

			objet = self.labyrinthe [coord[0] + dic[mvt][0] ] [coord[1] + dic[mvt][1] ]
			
			if objet.traversant or isinstance(objet, e_c.Porte):

				p_cardinaux.append("{}".format(mvt))

				liste_objet.append(objet)

				print("liste_coordonne : ", p_cardinaux)

		return p_cardinaux, liste_objet



	def liste_valeur_en_point_cardinaux(self, coord):
		"""Méthode appelée quand on souhaite connaitre les objet de passage valide"""

		liste = []

		dic = {"N":(-1,0), "E":(0,1), "S":(1,0), "O":(0,-1)}

		for mvt in "NESO":

			objet = self.labyrinthe [coord[0] + dic[mvt][0] ] [coord[1] + dic[mvt][1] ]
			
			if isinstance(objet, e_c.Couloir) or isinstance(objet, e_c.Porte) or isinstance(objet, e_c.Sortie) :

				liste.append(objet.coordonnee)

		return liste



	def dfs(self):
		"""methode qui permet de verifier et de recuperer dans une liste les chemin valide du labyrinthe ou graphe de profondeur"""

		#l'objectif et de cree une list de chemin possible
		y, x = len(self.labyrinthe), len(self.labyrinthe[0])

		tab = [ [999 for _ in range(x)] for _ in range(y) ]

		todo_list = [(i.coordonnee,0) for i in self.rechercher_liste_valeurs(e_c.Sortie())]

		liste_noeud_dist_max = []

		dist_max = 0


		while len(todo_list) != 0:

			elem_actuel, distance = todo_list.pop()

			if tab[elem_actuel[0]][elem_actuel[1]] > distance:

				tab[elem_actuel[0]][elem_actuel[1]] = distance

				todo_list += [(i,distance + 1) for i in self.liste_valeur_en_point_cardinaux(elem_actuel)]


		liste_valeur = []

		for y, r in enumerate(tab):

			for x, v in enumerate(r):

				if not v == 999:

					liste_valeur.append(((y, x),v))
		
		return liste_valeur
