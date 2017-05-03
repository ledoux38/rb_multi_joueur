#!/usr/bin/python3.5
# -*-coding:Utf-8 -*


import socket as st
import threading as tg
import time 

def ouverture_connexion(adresse, port):
	connexion = st.socket(st.AF_INET, st.SOCK_STREAM)
	connexion.connect((adresse, port))
	return connexion

def reception_donnee(connexion, poids_donnee = 1024, encodage = "utf-8"):
	message_recu = connexion.recv(poids_donnee)
	return message_recu.decode(encodage)

def emission_donnee(message_a_envoyer, connexion, encodage = "utf-8"):
	message_a_envoyer = message_a_envoyer.encode(encodage)
	connexion.send(message_a_envoyer)

def dialogue_utilisateur(texte_a_afficher = "", reponse = True):
	print(texte_a_afficher)

	if reponse:
		reponse_utilisateur = input(" > ")
		return reponse_utilisateur

def fermeture_connexion(connexion):
	connexion.close()



if __name__ == "__main__":
	version = 2

	if version == 0:
		connexion_serveur = st.socket(st.AF_INET, st.SOCK_STREAM)
		connexion_serveur.connect(("localhost", 12800))

		message_recu = connexion_serveur.recv(1024)
		print(message_recu)

		connexion_serveur.close()

	if version == 1:
		#version basique d'un echange de donnée avec un client

		print("connexion au serveur...")
		connexion_serveur = st.socket(st.AF_INET, st.SOCK_STREAM)

		try:
			connexion_serveur.connect(("localhost", 12800))
			connexion = True
		except ConnectionRefusedError:
			print("erreur le serveur est temporairement inaccessible...")
			connexion = False

		
		
		if connexion:

			message_a_envoyer = str()

			while message_a_envoyer != b"fin":
				message_a_envoyer = input(" > ")
				message_a_envoyer = message_a_envoyer.encode()
				connexion_serveur.send(message_a_envoyer)

				message_recu = connexion_serveur.recv(1024)
				print(message_recu.decode())

			print("fermeture de la connection")

			connexion_serveur.close()

	if version == 2:
		connexion_au_serveur = ouverture_connexion("localhost", 12800)

		message_a_envoyer = str()
		while message_a_envoyer != b"fin":
			message_a_envoyer = dialogue_utilisateur("utilisateur dit: \n")
			emission_donnee(message_a_envoyer, connexion_au_serveur)
			message_recu = reception_donnee(connexion_au_serveur)
			dialogue_utilisateur(message_recu, reponse = False)

		fermeture_connexion(connexion_au_serveur)


		