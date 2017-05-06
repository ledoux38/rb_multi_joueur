#!/usr/bin/python3.5
# -*-coding:Utf-8 -*


import socket as st
import select as sc

try:
	import package.connexion as cn
except:
	import connexion as cn


try:
	import package.gestionnaire_clients as gs
except:
	import gestionnaire_clients as gs


if __name__ == "__main__":
	version = 3

	#version tres basique d'un code de serveur
	if version == 0:
		
		connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
		connexion_principale.bind(("", 12800))

		connexion_principale.listen(5)

		connexion_client, info_client = connexion_principale.accept()

		print("info_client: {}".format(info_client))

		connexion_client.send(b"je viens de recevoir et d'accepter la connexion")

		connexion_client.close()
	
	#version basique d'un echange de donnée avec un client
	if version == 1:

		try:
			connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
			connexion_principale.bind(("", 12800))
			connexion_principale.listen(5)

		except ConnectionRefusedError:
			print("erreur lors du l'initialisation du serveur")

		print("serveur lancé \n en attente d'une connexion au port: 12800")
		connexion_client, info_client = connexion_principale.accept()

		message_recu = str()
		while message_recu != b"fin":

			message_recu = connexion_client.recv(1024)
			#print(connexion_client)
			print(message_recu.decode())

			message_a_envoyer = "5/5"
			message_a_envoyer = message_a_envoyer.encode()
			connexion_client.send(message_a_envoyer)

		print("fermeture de la connexion")

		connexion_client.close()
	
	#version basique d'un echange de donnée avec plusieurs clients
	if version == 2:

		try:
			connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
			connexion_principale.bind(("", 12800))
			connexion_principale.listen(5)


		except ConnectionRefusedError:
			print("erreur lors du l'initialisation du serveur")

		serveur_lance = True
		print("serveur lancé \n en attente d'une connexion au port: 12800")
		clients_connectes = []

		while serveur_lance:

			connexions_demandees, wlist, xlist = sc.select([connexion_principale], [], [], 0.05)
			#print (connexions_demandees, wlist, xlist, type(connexions_demandees), type(wlist), type(xlist))

			for connexion in connexions_demandees:
				connexions_clients, infos_connexion = connexion.accept()
				clients_connectes.append(connexions_clients)

			clients_a_lire = []

			try:
				clients_a_lire, wlist, xlist = sc.select(clients_connectes, [], [], 0.05)
			except select.error:
				pass

			else:
				for client in clients_a_lire:
					message_recu = client.recv(1024)
					message_recu = message_recu.decode()

					print("recu {}".format(message_recu))
					client.send(b"5/5")
					if message_recu == "fin":
						serveur_lance == False

		print("fermeture des connexions")

		for client in clients_connectes:
			client.close()

		connexion_principale.close()

	#version basique d'un echange de donnée avec plusieurs clients
	if version == 3:

		try:
			connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
			connexion_principale.bind(("", 12803))
			connexion_principale.listen(5)


		except ConnectionRefusedError:
			print("erreur lors du l'initialisation du serveur")

		serveur_lance = True
		print("serveur lancé \n en attente d'une connexion au port: 12800")
		tableau_des_clients = gs.Gestionnaire_clients()
		
		#clients_connectes = []

		while serveur_lance:

			connexions_demandees, wlist, xlist = sc.select([connexion_principale], [], [], 0.05)
			#print (connexions_demandees, wlist, xlist, type(connexions_demandees), type(wlist), type(xlist))

			for connexion in connexions_demandees:
				connexions_clients, infos_connexion = connexion.accept()
				#print(clients_connectes, type(clients_connectes))
				tableau_des_clients.ajouter_connexion(connexions_clients)
				#clients_connectes.append(connexions_clients)
				print(tableau_des_clients._tableau_de_connexions[0])
				print(type(tableau_des_clients._tableau_de_connexions[0]))
			clients_a_lire = []

			try:
				clients_a_lire, wlist, xlist = sc.select(tableau_des_clients.tableau_de_connexions, [], [], 0.05)
				#clients_a_lire, wlist, xlist = sc.select(clients_connectes, [], [], 0.05)
				#print(clients_connectes, type(clients_connectes))
			except sc.error:
				pass

			else:
				for client in clients_a_lire:
					message_recu = client.recv(1024)
					message_recu = message_recu.decode()

					print("recu {}".format(message_recu))
					client.send(b"5/5")
					if message_recu == "fin":
						serveur_lance == False

		print("fermeture des connexions")

		for client in clients_connectes:
			client.close()

		connexion_principale.close()

	if version == 4:

		tableau = []
		tableau.append(cn.Connexion())
		print(tableau[0])

