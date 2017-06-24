#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

try:
	import package.carte as c
except:
	import carte as c

try:
	import package.gestionnaire_clients as g_c
except:
	import gestionnaire_clients as g_c

try:
	import package.Gestionnaire_entree_sortie_donnee as g_e_s
except:
	import Gestionnaire_entree_sortie_donnee as g_e_s

try:
	import package.elements_de_carte as e_c
except:
	import elements_de_carte as e_c


import copy


class Application_labyrinthe:
	"""classe qui organise les clients, joueur, et la carte"""

	def __init__(self):

		self.g_clients = g_c.Gestionnaire_clients()

		self.carte = None

		self.ch_dossier = "/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/"



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la class via un print()"""
		
		msg = "nb clients: {} \nCarte: {}".format(self.g_clients, self.carte)
		
		return msg



	def __len__(self):
		"""methode appeler lorsque on veut connaitre la taille du tableau"""
		
		return len(self.g_clients)



	def choix_carte(self, erreur = False):
		"""fonction qui permet de préparer une chaine de caractere à envoyer au joueur pour le choix de la carte"""
		es = g_e_s.Gestionnaire_entree_sortie_donnee.static_RecupList(self.ch_dossier)
		
		liste_str = ""

		for numero, index in enumerate(es):
			
			liste_str += "<{}>: {}\n".format(numero,index)

		texte_descriptif = "Bienvenue sur l'application l'Abyrinthe multi_joueurs.\n Veillez choisir la carte pour lancer la partie!\n{}".format(liste_str)
		
		if erreur:

			texte_descriptif = "{} \n {}".format("Erreur lors de la saisi!", texte_descriptif)

		return texte_descriptif



	def chargement_carte(self, choix):
		"""fonction qui va charger une carte choisi par le joueur"""
		
		#chargement du fichier
		liste = g_e_s.Gestionnaire_entree_sortie_donnee.static_RecupList(self.ch_dossier)

		nom_fichier = liste[int(choix)]

		adr = self.ch_dossier + nom_fichier

		carte_en_str = g_e_s.Gestionnaire_entree_sortie_donnee.static_chargement_donnee(adr)

		#creation de la carte via le fichier
		self.carte = c.Carte(nom = nom_fichier, chaine = carte_en_str)



	def proposition_de_deplacement(self, joueur, *affichage):
		"""retourne dans une list des valeurs de deplacement possible du joueur"""

		texte_sup = ""

		#rajoute le texte envoyer en argument
		for i in affichage:

			texte_sup += str(i) + "\n"

		p_cardinaux, liste_objet = self.carte.liste_coordonne_en_point_cardinaux(coord = joueur.coordonnee)

		#formatage de la chaine de caractere
		chaine = "{}\n{}\nproposition de deplacement:\n".format(texte_sup, self.carte.carte_utilisateur(joueur.coordonnee))

		for i, mvt in enumerate(p_cardinaux):
			
			#si objet est une porte je verifie si elle et traversant ou non en fonction, choix au joueur de percer ou murrer porte
			if isinstance(liste_objet[i], e_c.Porte):

				if liste_objet[i].traversant:

					chaine += "<M{}> ".format(mvt)

				else:

					chaine += "<P{}> ".format(mvt)
			
			if liste_objet[i].traversant:
			
				chaine += "<{}> ".format(mvt)

		chaine += "<QUIT> <PASSER>"

		#rajout des autres comportement possible
		autre_comportement = ["MN","ME","MS","MO","PN","PE","PS","PO","QUIT", "PASSER" ]
		
		p_cardinaux.extend(autre_comportement)

		return chaine, p_cardinaux



	def mouvement_joueur(self, joueur, mouvement):
		"""fonction qui va deplacer le joueurs sur la carte"""

		coord_j = joueur.coordonnee

		obj = None

		dic = {
			"N":(-1,0),
			"E":(0,1),
			"S":(1,0), 
			"O":(0,-1),
			"MN" : (-1,0),
			"ME" : (0,1),
			"MS" : (1,0),
			"MO" : (0,-1),
			"PN" : (-1,0),
			"PE" : (0,1),
			"PS" : (1,0),
			"PO" : (0,-1)}

		#en fonction de la reposne recu de la connexion je renvoi l'objet ciblé
		obj = self.carte [coord_j[0] + dic[mouvement][0] ] [coord_j[1] + dic[mouvement][1] ]

		if isinstance(obj, e_c.Couloir) or isinstance(obj, e_c.Porte) or isinstance(obj, e_c.Sortie):

			#si reponse joueur equivalent a l'intervalle,  porte murrée
			if mouvement in ["MN", "ME", "MS", "MO"]:

				obj.forme = "0"

				obj.traversant = False
			
			#sinon si reponse joueur equivalent a l'intervalle,  porte percée
			elif mouvement in ["PN", "PE", "PS", "PO"]:

				obj.forme = "."

				obj.traversant = True

			else:

				#joueur transferer dans ca nouvelle position
				copie_objet = copy.deepcopy(joueur.element_nouvelle_position)
					
				joueur.coordonnee = obj.coordonnee

				joueur.element_nouvelle_position = obj

				self.carte[joueur.coordonnee[0]][joueur.coordonnee[1]] = joueur

				self.carte[copie_objet.coordonnee[0]][copie_objet.coordonnee[1]] = copie_objet

		else:

			raise TypeError("Erreur objet carte != e_c.Couloir")



	def verification_de_victoire(self):
		"""fonction qui à pour but de verifier si il y a victoire"""

		liste = self.carte.rechercher_liste_valeurs(e_c.Joueur())

		if isinstance(liste, list):

			for joueur in liste:

				if joueur.coordonnee == self.carte.sortie.coordonnee:

					return joueur

		else:

			if liste.coordonnee == self.carte.coord_sortie:

				return liste

		return None

