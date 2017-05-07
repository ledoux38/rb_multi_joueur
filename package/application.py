#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
import package.Gestionnaire_entree_sortie_donnee as ES
import package.module_labyrinthe as utils
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
		 
