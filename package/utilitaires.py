#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

try:
	import package.Gestionnaire_entree_sortie_donnee as ES
except:
	import Gestionnaire_entree_sortie_donnee as ES

#import package.module_labyrinthe as utils
import os
import collections
def validation_de_la_saisie(reponse, list_action, longueur_reponse = 1):
	"""Verifie que la saisie du joueur est correcte"""

	if not isinstance(reponse,str) or not isinstance(sequence_choix,str):
		raise TypeError("str attendu")

	if reponse in sequence_choix and len(reponse) is longueur_reponse:
		return True

	else:
		return False


def conversion_saisie_en_majuscule(chaine):
	"""fonction qui permet de convertir des lettre en majuscule"""
	#verification du typage du parametre
	if not isinstance(chaine,str):
		raise TypeError("str attendu")
	#si lettre en minuscule
	if chaine is not chaine.isupper():
		chaine= chaine.upper()
	return chaine


#non utilisée
def choix_utilisateur(chaine_question, choix_caractere = "NCQ", chaine_input = "votre reponse? ",longueur = 1):
	"""fonction qui propose des choix a l'utilisateur"""
	if not isinstance(chaine_question,str) or not isinstance(choix_caractere, str) or not isinstance(longueur,int):
		raise TypeError("erreur de typage dans un des parametres transmit")

	for caractere in choix_caractere:
		chaine_question += "<{}> ".format(choix_caractere)

	while True:
		print("{}".format(chaine_question))
		reponse = input(chaine_input)
		reponse = verification_saisie_majuscule(chaine = reponse)
		
		if validation_de_la_saisie(reponse = reponse,sequence_choix = choix_caractere,longueur_reponse = longueur):
			return reponse
		
		else:
			print("erreur lors de la saisie <{}> inccorect".format(reponse))



def interation_utilisateur(phrase_principale, action, phrase_de_fin= "votre reponse? "):
	"""fonction qui propose des choix a l'utilisateur"""

	if not isinstance(phrase_principale, str):
		raise TypeError("erreur parametre <phrase_principale> type str ")

	if not isinstance(phrase_de_fin, str):
		raise TypeError("erreur parametre <phrase_de_fin> type str ")

	if isinstance(action, dict):

		#rajout dans la phrase_principale les cle et description des cles
		for cle, valeur in action.items():
			phrase_principale += "\n<{}>: {} ".format(cle, valeur)

		#tant que la saisie du resultat n'est pas correcte par rapport aux cles je recommence
		while True:
			print("{}".format(phrase_principale))
			reponse = input(phrase_de_fin)
			reponse = conversion_saisie_en_majuscule(chaine = reponse)

			if reponse in str(action.keys()):
				return reponse
			else:
				print("Erreur dans la saisie")

	elif isinstance( action, list):

		for num, valeur in enumerate(action):
			phrase_principale += "\n<{}>: {} ".format(num, valeur)

		#tant que la saisie du resultat n'est pas correcte par rapport aux cles je recommence
		while True:
			print("{}".format(phrase_principale))
			reponse = input(phrase_de_fin)
			reponse = conversion_saisie_en_majuscule(chaine = reponse)

			if int(reponse) >= 0 and int(reponse) <=(len(action) -1 ):
				return reponse
			else:
				print("Erreur dans la saisie")

	else:
		raise TypeError("erreur parametre <action> doit etre de type <dict> ou <list> ")



def interation_utilisateurV2(phrase_principale, action, phrase_de_fin= "votre reponse? "):
	"""classe qui propose des choix a l'utilisateur"""

	if not isinstance(phrase_principale, str):
		raise TypeError("erreur parametre <phrase_principale> type str ")

	if not isinstance(phrase_de_fin, str):
		raise TypeError("erreur parametre <phrase_de_fin> type str ")

	if isinstance(action, dict):

		#rajout dans la phrase_principale les cle et description des cles
		for cle, valeur in action.items():
			phrase_principale += "\n<{}>: {} ".format(cle, valeur)

		#tant que la saisie du resultat n'est pas correcte par rapport aux cles je recommence
		while True:
			print("{}".format(phrase_principale))
			reponse = input(phrase_de_fin)
			reponse = conversion_saisie_en_majuscule(chaine = reponse)

			if reponse in str(action.keys()):
				return reponse
			else:
				print("Erreur dans la saisie")


	elif isinstance( action, list):

		for num, valeur in enumerate(action):
			phrase_principale += "\n<{}>: {} ".format(num, valeur)

		#tant que la saisie du resultat n'est pas correcte par rapport aux cles je recommence
		while True:
			print("{}".format(phrase_principale))
			reponse = input(phrase_de_fin)
			reponse = conversion_saisie_en_majuscule(chaine = reponse)

			if int(reponse) >= 0 and int(reponse) <=(len(action) -1 ):
				return reponse
			else:
				print("Erreur dans la saisie")

	else:
		raise TypeError("erreur parametre <action> doit etre de type <dict> ou <list> ")



def listes_cartes(liste_carte):
	#recupere une liste de fichier et la convertie en dict
	if not isinstance(liste_carte,list):
		raise TypeError("type list attendu")

	dic= dict()

	for num,carte in enumerate(liste_carte):
		dic[num] = carte

	return (dic)



def chargement_donnee(adresse_dossier):
	"""methode qui charge les données d'un dossier"""

	#verification que le typage de la variable <adresse_dossier> est de type str
	if not isinstance(adresse_dossier,str):
		raise TypeError("str attendu")

	#instanciation de la classe Chargement
	try:
		charg_carte = ES.Gestionnaire_entree_sortie_donnee(adresse_dossier)

	except FileNotFoundError:
		raise FileNotFoundError("dossier non trouvé à adresse < {} >".format(adresse_dossier))

		#si nonmbre de fichiers inferieur ou egal à zero je leve une exception
	if len(charg_carte._get_liste_donnee())<= 0:
		raise FileNotFoundError("erreur aucun fichier trouvé à l'adresse <{}>".format(adresse_dossier))
		
	#sinon si nombre de fichiers egal à un je charge directement le fichier
	elif len(charg_carte._get_liste_donnee()) == 1:
		chaine_labyrinthe= charg_carte.chargement_donnee(charg_carte._liste[0])
		nom_labyrinthe= charg_carte._liste[0]
		
	#sinon nombres de fichiers sup à 1 je prepare une liste et propose a l'utilisateur de choisir
	else:
		numero = int(interation_utilisateur( phrase_principale = "choix d'une carte:", action = listes_cartes( charg_carte._liste ) ) ) 
		chaine_labyrinthe = charg_carte.chargement_donnee( charg_carte.liste[numero] )
		nom_labyrinthe = charg_carte._liste[numero]
		
	#je retourne le labyrinthe version chaine et sont nom
	return (nom_labyrinthe, chaine_labyrinthe)
	


def sauvegarde_donnee(adresse_dossier,carte):
	if not isinstance(adresse_dossier,str):
		raise TypeError("erreur le parametre <adresse_dossier> doit etre de type <str> et pas de type <{}>".format(type(adresse_dossier)))

	if not isinstance(carte,str):
		raise TypeError("erreur le parametre <carte> doit etre de type <str> et pas de type <{}>".format(type(adresse_dossier)))
		
	try:
		donnee= ES.Gestionnaire_entree_sortie_donnee(adresse_dossier)
		donnee.sauvegarde_donnee("save.txt",carte)
	except Exception as e:
		raise e

 

if __name__ == "__main__":
	c = {"Q":"quitter", "A": "Annuler"}
	b = collections.OrderedDict(c)

	a = interation_utilisateur("bonjour", b)

