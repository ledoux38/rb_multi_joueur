#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

import os

class Gestionnaire_entree_sortie_donnee:
	"""class qui charge les données on peu la cree de plusieur façon, vide ou avec un chemin d'accee. la modification du chemin d'accee recuperent automatiquement la list """

	def __init__(self,chemin_dossier):
		"""initialisation permet de sauvegarder dans les attributs la _liste des fichiers
		et le chemin d'acces"""

		if not isinstance(chemin_dossier,str):
			raise TypeError("erreur parametre chemin_dossier n'est pas de type <str> il est de type <{}>".format(type(chemin_dossier)))

		if not os.path.exists(chemin_dossier):
			raise FileNotFoundError("le dossier <{}> d'existe pas".format(chemin_dossier))

		self._chemin_dossier = chemin_dossier
		"""contien par defaut le chemin d'acces du fichier"""

		self._liste = os.listdir(chemin_dossier)
		"""c'est une liste des donnee"""



	def __repr__(self):
		"""affichage de l'object dans l'interpreteur"""
	
		return "{}".format(self._liste)
	
	
	def __str__(self):
		"""affichage de l'object un print"""
		
		return "{}".format(self._liste) 


	def __len__(self):
		"""methode appeler lorsque on veut connaitre la taille du tableau"""
		
		return len(self._liste)


	def __getitem__(self, index):
		"""Cette méthode spéciale est appelée quand on fait objet[index]
		Elle redirige vers self._dictionnaire[index]"""

		liste_carte = self._liste[index]

		return liste_carte


	def _set_changement_adresse_fichier(self, nouvelle_adresse):
		if not os.path.exists(nouvelle_adresse):
			raise FileNotFoundError("le dossier <{}> d'existe pas".format(nouvelle_adresse))
		
		self._chemin_dossier = nouvelle_adresse
		"""contien par defaut le chemin d'acces du fichier"""

		self._liste = os.listdir(nouvelle_adresse)
		"""c'est une liste des donnee"""



	def _get_adresse_fichier(self):
		"""retourne l'adresse du fichier"""
		return self._chemin_dossier



	def _set_actualise_liste_donnee(self):
		"""actualise la liste de donnee"""	
		self._liste = os.listdir(self._chemin_dossier)



	def _get_liste_donnee(self):
		"""retourne la liste de donnee"""
		return self._liste







	def chargement_donnee(self,nom_fichier):
		""" charge le fichier a l'adresse indiquer """
		if not isinstance(nom_fichier,str):
			raise TypeError("erreur parametre chemin_dossier n'est pas de type <str> il est de type <{}>".format(type(nom_fichier)))
		
		adr = self.chemin_dossier + nom_fichier		

		if not os.path.isfile(adr):
			raise FileNotFoundError("erreur le fichier n'existe pas ou plus!")
		

		with open(adr,'r') as mon_fichier:
			fichier = mon_fichier.read()
			return fichier



	def sauvegarde_donnee(self,nom_fichier,donnee_a_sauvegarder):
		"""methode qui sauvegarde dans l'adresse sauvegarder dans l'attribut self.chemin_dossier"""

		"""verification des parametre envoyer a la fonction"""
		if not isinstance(nom_fichier,str):
			raise TypeError("erreur parametre chemin_dossier ou donnee n'est pas de type <str> il est de type <{}>".format(type(nom_fichier)))
			
		if not isinstance(donnee_a_sauvegarder,str):
			raise TypeError("erreur parametre donnee_a_sauvegarder ou donnee n'est pas de type <str> il est de type <{}>".format(type(donnee_a_sauvegarder)))
		"""ouverture du fichier pour la sauvegarde"""
		adr = self.chemin_dossier + nom_fichier
		with open(adr,'w') as mon_fichier:
			mon_fichier.write(donnee_a_sauvegarder)



	chemin_dossier= property(_get_adresse_fichier,_set_changement_adresse_fichier)
	liste= property(_get_liste_donnee,_set_actualise_liste_donnee)



	def static_chargement_donnee(self,nom_fichier):
		""" charge le fichier a l'adresse indiquer """
		if not isinstance(nom_fichier,str):
			raise TypeError("erreur parametre chemin_dossier n'est pas de type <str> il est de type <{}>".format(type(nom_fichier)))
		
		adr = self.chemin_dossier + nom_fichier		

		if not os.path.isfile(adr):
			raise FileNotFoundError("erreur le fichier n'existe pas ou plus!")
		

		with open(adr,'r') as mon_fichier:
			fichier = mon_fichier.read()
			return fichier



	def static_presence_fichier(chemin_dossier):
		"""Methode static qui permet d'eviter de creer un obj pour verifier
		si presence de donnee dans le dossier ciblé
		si il y a presence de fichier la methode renvoi true sinon elle renvoi false"""
		
		donnee = os.listdir(chemin_dossier)
		
		if len(donnee)!= 0:
		
			return True
		
		else:
		
			return False
		
		static_presence_fichier = staticmethod(static_presence_fichier)



	def static_nombre_de_fichier(chemin_dossier):
		"""methode static pour recuperer le nombre de fichier dans le dossier"""
		
		donnee = os.listdir(chemin_dossier)
		
		return len(donnee)
		
		static_nombre_de_fichier = staticmethod(static_nombre_de_fichier)



	#methode réécrite
	def static_recherche_nom_fichier(chemin_dossier, mot_rechercher):
		"""methode static pour recuperer l'index du fichier recherché dans le dossier"""

		#je recupere la list de données de fichier
		donnee = os.listdir(chemin_dossier)
		# je cherche les donnee dans le tableau
		index = donnee.index(mot_rechercher)
		# je retourne l'index du mot rechercher
		return index

		static_recherche_nom_fichier = staticmethod(static_recherche_nom_fichier)
	


	#methode réécrite
	def static_RecupList(chemin_dossier):
		"""recupere la liste des noms"""
		
		donnee = os.listdir(chemin_dossier)
		
		return donnee
		
		static_RecupList = staticmethod(static_RecupList)



	def static_chargement_donnee(ch_fichier):
		""" charge le fichier a l'adresse indiquer """
		if not isinstance(ch_fichier,str):
		
			raise TypeError("erreur parametre chemin_dossier n'est pas de type <str> il est de type <{}>".format(type(nom_fichier)))
		
		if not os.path.isfile(ch_fichier):
			
			raise FileNotFoundError("erreur le fichier n'existe pas ou plus!")
		
		with open(ch_fichier,'r') as mon_fichier:
			
			fichier = mon_fichier.read()
			
			return fichier

		static_RecupList = staticmethod(static_RecupList)




if __name__ == '__main__':
	a = Gestionnaire_entree_sortie_donnee("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/package/")
	print(a.liste)
	a.chemin_dossier = ("/home/ledoux/Documents/Programmation/python/python-le-on/proj/rb_multi_joueur/cartes/")
	print(a.liste)
	print(a.chargement_donnee("facile.txt"))

	print(Gestionnaire_entree_sortie_donnee.static_RecupList(a.chemin_dossier))