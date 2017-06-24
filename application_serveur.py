#!/usr/bin/python3.5
# -*-coding:Utf-8 -*


from package import serveur as s



if __name__ == '__main__':

	serveur = s.Serveur("127.0.0.1", 12100)

	serveur.app_labyrinthe()