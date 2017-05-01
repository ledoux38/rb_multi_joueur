#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
from package.class_ES import ES_Donnee
from package.module_labyrinthe import Scene
import os

def app_labyrinthe():
	application = True
	while application:

		caracteres= "NCQ"
		question= """bienvenue au jeux du labyrinthe! \n
		 Nouvelle partie? <{}> \n
		 Charger une partie? <{}> \n
		 Quitter? <{}>""".format(caracteres[0],caracteres[1],caracteres[2])
		reponse= choix_utilisateur(chaine_question=question,choix_caractere=caracteres)
		adresse_dossier_cartes,adresse_dossier_sauvegarde= "./cartes/","./sauvegarde/"

		# si utilisateur repond "n" nouvelle partie
		if reponse == "N":
			#je propose a l'utilisateur de charger une carte
			chaine, nom= chargement_donnee(adresse_dossier_cartes)

		# sinon si utilisateur repond "c" charger partie
		elif reponse == "C":
			
			#si il y a des fichier dans le dossiers sauvegarde je charge les données 
			if ES_Donnee.static_presence_fichier(adresse_dossier_sauvegarde):
				chaine, nom= chargement_donnee(adresse_dossier_sauvegarde)
			
			#sinon il ya pas de carte dans le dossier sauvegarde et je charge dans le dossier "./cartes/"			
			else:

				print("sauvegarde non trouvé! \n nouvelle partie")		
				chaine, nom= chargement_donnee(adresse_dossier_cartes)				
		
		#sinon si l'utilisateur repond <Q> c'est quil veut quitter l'application
		elif reponse == "Q":
			
			print("reponse")
			caracteres = "ON"
			question = "Voulez vous vraiment quitter? <{}> ou <{}>: ".format(caracteres[0],caracteres[1])
			
			if choix_utilisateur(chaine_question=question,choix_caractere=caracteres) == "O":
				application= False
				continue
			else:
				application= True
				continue
		
		labyrinthe= Scene(nom= nom,chaine= chaine)
		partie= True
		os.system("clear")
		
		while partie:
			#la fonction labyrinthe revoie deux parametres, une direction et un numero
			commande,num= labyrinthe.phase_de_deplacement()
			if commande == "Q":
				caracteres = "ON"
				question = "Voulez vous retourner au menu principal? <{}> ou <{}>: ".format(caracteres[0],caracteres[1])
			
				if choix_utilisateur(chaine_question=question,choix_caractere=caracteres) == "O":
					sauvegarde_donnee(adresse_dossier_sauvegarde,labyrinthe.carte.representation_labyrinthe_str())
					partie= False
				continue

			cpt= 0
			while cpt<num:

				coordonnee= labyrinthe.coordonnee(commande)

				#verification si on peut ce deplacer à ces coordonnees
				if labyrinthe.analyse_deplacement(coordonnee):
					
					#validation ok modification des valeurs aux coordonnees donnees
					labyrinthe.setCoordonnee(coordonnee)
					
					#je verifie si le robot a atteint la sortie
					if labyrinthe.verification_victoire():
						os.system("clear")
						print(labyrinthe.carte.representation_labyrinthe_str())
						print("Victoire!! \n retour au menu principale")
						os.remove(adresse_dossier_sauvegarde+"save.txt")
						partie= False
						break
					else:
						sauvegarde_donnee(adresse_dossier_sauvegarde,labyrinthe.carte.representation_labyrinthe_str())
						os.system("clear")
				cpt+= 1
		
def validation_de_la_saisie(reponse, sequence_choix = "NCQ",longueur_reponse = 1):
	if not isinstance(reponse,str) or not isinstance(sequence_choix,str):
		raise TypeError("str attendu")
	if reponse in sequence_choix and len(reponse) is longueur_reponse:
		return True
	else:
		return False

def verification_saisie_majuscule(chaine):
	"""fonction qui permet de convertir des lettre en majuscule"""
	#verification du typage du parametre
	if not isinstance(chaine,str):
		raise TypeError("str attendu")
	#si lettre en minuscule
	if chaine is not chaine.isupper():
		chaine= chaine.upper()
	return chaine

def choix_utilisateur(chaine_question,choix_caractere = "NCQ", chaine_input = "votre reponse? ",longueur = 1):
	"""classe qui propose des choix a l'utilisateur"""
	if not isinstance(chaine_question,str) or not isinstance(choix_caractere, str) or not isinstance(longueur,int):
		raise TypeError("erreur de typage dans un des parametres transmit")
	
	while True:
		print("{}".format(chaine_question))
		reponse = input(chaine_input)
		reponse = verification_saisie_majuscule(chaine = reponse)
		
		if validation_de_la_saisie(reponse = reponse,sequence_choix = choix_caractere,longueur_reponse = longueur):
			return reponse
		
		else:
			print("erreur lors de la saisie <{}> inccorect".format(reponse))

def elaboration_liste_carte(liste_carte):
	if not isinstance(liste_carte,list):
		raise TypeError("list attendu")
	sequence= str()
	chaine= "Votre choix?\n"
	for num,carte in enumerate(liste_carte):
		chaine += str(" -{} <{}>:\n".format(carte,num))
		sequence += str(num)
	return (chaine,sequence)

def chargement_donnee(adresse_dossier):
	"""methode qui charge les donnee dans un dossiers specifier
	par la variable "adress_dossier" """

	#verification que le typage de la variable adresse dossier soit une str
	if not isinstance(adresse_dossier,str):
		raise TypeError("str attendu")
	#instanciation de la classe Chargement
	try:
		charg_carte = ES_Donnee(adresse_dossier)
		
		#si fichier = 0 je leve une exception
		if len(charg_carte._get_liste_donnee())<= 0:
			raise FileNotFoundError("erreur aucun fichier trouvé à l'adresse <{}>".format(adresse_dossier))
		
		#sinon si fichier = 1 je charge directement le fichier
		elif len(charg_carte._get_liste_donnee()) == 1:
			chaine_labyrinthe= charg_carte.chargement_donnee(charg_carte._liste[0])
			nom_labyrinthe= charg_carte._liste[0]
		
		#else: nombre de fichier sup à 1 je prepare une liste et propose a l'utilisateur de choisir
		else:
			chaine, sequence_verification =elaboration_liste_carte(charg_carte._liste)
			numero= int(choix_utilisateur(chaine_question= chaine,choix_caractere = sequence_verification))
			chaine_labyrinthe= charg_carte.chargement_donnee(charg_carte.liste[numero])
			nom_labyrinthe= charg_carte._liste[numero]
		
		#je retourne le labyrinthe version chaine et sont nom
		return (chaine_labyrinthe, nom_labyrinthe)
	
	except FileNotFoundError as e:
		print (e)

def sauvegarde_donnee(adresse_dossier,carte):
	if not isinstance(adresse_dossier,str):
		raise TypeError("erreur le parametre <adresse_dossier> doit etre de type <str> et pas de type <{}>".format(type(adresse_dossier)))

	if not isinstance(carte,str):
		raise TypeError("erreur le parametre <carte> doit etre de type <str> et pas de type <{}>".format(type(adresse_dossier)))
		
	try:
		donnee= ES_Donnee(adresse_dossier)
		donnee.sauvegarde_donnee("save.txt",carte)
	except Exception as e:
		raise e

 
