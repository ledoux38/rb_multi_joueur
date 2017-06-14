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

import unittest

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

		self.list_posit_joueur = self.graphe_de_sommet()


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

		for liste in liste_coordonnee:

			for i in liste:

				if not i in self.list_posit_joueur:

					liste.remove(i)

		coordonnee = random.choice(liste_coordonnee[0])

		joueur.coordonnee = coordonnee

		joueur.element_nouvelle_position.coordonnee = coordonnee

		self.labyrinthe[coordonnee[0]][coordonnee[1]] = joueur



	def liste_coordonne_en_point_cardinaux(self, coord):
		"""Méthode appelée quand on souhaite connaitre les chemins de passage valide"""

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
		"""Méthode appelée quand on souhaite connaitre les chemins de passage valide"""

		liste = []

		dic = {"N":(-1,0), "E":(0,1), "S":(1,0), "O":(0,-1)}

		for mvt in "NESO":

			objet = self.labyrinthe [coord[0] + dic[mvt][0] ] [coord[1] + dic[mvt][1] ]
			
			if isinstance(objet, e_c.Couloir) or isinstance(objet, e_c.Porte) or isinstance(objet, e_c.Sortie) :

				liste.append(objet.coordonnee)

		return liste



	def graphe_de_sommet(self):
		liste_obj = []

		dic = {}

		liste_recherche = [ e_c.Couloir(), e_c.Porte(), e_c.Sortie() ]
		#recuperation de tout les objets de type couloir, porte,sortie
		for recherche in liste_recherche:

			liste_obj.extend(self.rechercher_liste_valeurs(recherche))

		#pour chaque case du tableau je vais cree une liste de voisin
		for i in liste_obj:

			dic[i.coordonnee] = self.liste_valeur_en_point_cardinaux(i.coordonnee)

		#pour chaque case du dictionnaire je vais remonter le chemin
		liste_dfs = self.dfs(dic, self.sortie.coordonnee)

		liste = []

		# je recupere chaque clee du dictionnaire retourné
		for valeur in liste_dfs.keys():

			liste.append(valeur)

		return liste



	def dfs(self, G, s) :

		P,Q={s :None},[s]

		while Q :

			u=Q[-1]

			R=[y for y in G[u] if y not in P]

			if R :

				v=random.choice(R)

				P[v]=u

				Q.append(v)

			else :

				Q.pop()

		return P



	def dfsV2(self):

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

		return tab




class test_carte (unittest.TestCase):

	def setUp(self):
		dossier = ES.Gestionnaire_entree_sortie_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
		
		labyrinthe = dossier.chargement_donnee("facile.txt")

		nom_labyrinthe = "a[0]"
		
		self.a = Carte(nom_labyrinthe, labyrinthe)



	def tearDown(self):

		print("\n")



	def test_getitem(self):
		
		valeur_1 = self.a[0][0]

		self.assertEqual(valeur_1, self.a.labyrinthe[0][0])

		valeur_2 = self.a[2][2]

		self.assertEqual(valeur_2, self.a.labyrinthe[2][2])

		valeur_3 = self.a[5][5]

		self.assertEqual(valeur_3, self.a.labyrinthe[5][5])



	def test_setitem(self):

		self.a[0][0] = e_c.Joueur()

		self.assertEqual(type(e_c.Joueur()), type(self.a.labyrinthe[0][0]))		



	def test_rechercher_les_coordonnees_des_valeurs(self):
		
		liste = self.a.rechercher_les_coordonnees_des_valeurs(e_c.Porte())
		
		liste_reel = [(3, 3), (5, 9), (7, 9), (10, 3)]


		self.assertEqual(liste, liste_reel)

		liste = self.a.rechercher_les_coordonnees_des_valeurs(e_c.Sortie())
		
		liste_reel = [(6, 10)]

		self.assertEqual(liste, liste_reel)



	def test_liste_valeurs_par_lignes(self):

		retour = self.a.liste_valeurs_par_lignes(valeur = e_c.Couloir())

		liste_reel_debut = [(2, 2), (2, 4), (2, 5), (2, 6), (2, 7), (2, 9)]

		liste_reel_fin = [(10, 2), (10, 4), (10, 6), (10, 7), (10, 8), (10, 9)]


		self.assertEqual(retour[0],liste_reel_debut)
		
		self.assertEqual(retour[-1],liste_reel_fin)



	def test_positionement_aleatoire(self):

		joueur1 = e_c.Joueur()

		joueur2 = e_c.Joueur()

		self.a.positionement_aleatoire(joueur1)
		
		self.a.positionement_aleatoire(joueur2)

		coord1 = joueur1.coordonnee

		coord2 = joueur2.coordonnee

		self.assertEqual(id(joueur1),id(self.a[coord1[0]][coord1[1]]))
		
		self.assertEqual(joueur2,self.a[coord2[0]][coord2[1]])	



	def test_carte_utilisateur(self):

		joueur1 = e_c.Joueur()

		joueur2 = e_c.Joueur()

		self.a.positionement_aleatoire(joueur1)
		
		self.a.positionement_aleatoire(joueur2)	
		
		coord = self.a.rechercher_les_coordonnees_des_valeurs(valeur = e_c.Joueur())

		coord = random.choice(coord)



	def test_liste_coordonne_en_point_cardinaux(self):

		joueur1 = e_c.Joueur()

		self.a.positionement_aleatoire(joueur1)

		liste = self.a.liste_coordonne_en_point_cardinaux(coord = joueur1.coordonnee)

		print(liste[1])



	def test_rechercher_liste_valeurs(self):

		liste_objet = self.a.rechercher_liste_valeurs(e_c.Sortie())[0]

		coord_objet = self.a.rechercher_les_coordonnees_des_valeurs(e_c.Sortie())[0]

		objet = self.a[coord_objet[0]] [coord_objet[1]]

		self.assertEqual(id(liste_objet), id(objet))

		liste_objet = self.a.rechercher_liste_valeurs(e_c.Porte())

		self.assertEqual(len(liste_objet), 4)

		self.assertEqual(type(liste_objet[0]), type(e_c.Porte()))
		
		self.assertEqual(type(liste_objet[1]), type(e_c.Porte()))

		self.assertEqual(type(liste_objet[2]), type(e_c.Porte()))

		self.assertEqual(type(liste_objet[3]), type(e_c.Porte()))

	def test_dfsV2(self):

		retour = self.a.dfsV2()

		for i in retour:

			for j in i:

				if j == -1:

					print("#", end = "")

				elif j >= 10:

					print("*", end = "")

				else:

					print(j, end = "")

			print("")




if __name__ == '__main__':

	unittest.main()

