#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 

try:
	import package.connexion as cn
except:
	import connexion as cn



class Gestionnaire_clients:
	"""la classe Gestionnaire_clients et une classe qui est crée pour gerer les joueurs ainsi que les connexions.
	avec position X, Y et une forme
	mais aussi garder en mémoire la connexion ainsi que l'adresse (IP/ port)

	ATTRIBUTS:	tableau_de_connexions


	"""
	def __init__(self):
		"""instancie le Gestionnaire_clients.
		le Gestionnaire_clients est representer sous la forme d'un tableau qui contiendra des données de type Connexion
		"""
		self.tableau_de_connexions = []



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		
		msg = "clients: \n"
		
		for num, clients in enumerate(self.tableau_de_connexions):
			
			msg += "{}: {} \n".format(num, clients)

		return msg



	def __iadd__(self, nouvelle_connexion):
		"""Cette méthode spéciale est appelée quand on fait une operation de type +="""
		
		self.ajouter_connexion(nouvelle_connexion)
		
		return self




	def __getitem__(self, index):
		"""Cette méthode spéciale est appelée quand on fait objet[index]
		Elle redirige vers self._dictionnaire[index]"""

		connexion = self.tableau_de_connexions[index]

		return connexion.information_connexion



	def __len__(self):
		"""methode appeler lorsque on veut connaitre la taille du tableau"""
		return len(self.tableau_de_connexions)
		


	def ajouter_connexion(self, nouvelle_connexion):
		"""methode appeler lorsque on veut ajouter une connexion au tableau"""
		
		self.tableau_de_connexions.append(cn.Connexion(connexion = nouvelle_connexion))



	def supprimer_connexion(self, index):
		"""methode appeler lorsque on veut supprimer une connexion au tableau"""
		del self.tableau_de_connexions[index]


if __name__ == "__main__":

	a = Gestionnaire_clients()
	a.tableau_de_connexions += ["127.0.0.1", 12800]
	a.tableau_de_connexions += ["127.0.0.2", 12800]
	a.tableau_de_connexions += ["127.0.0.3", 12800]
	print("aaaaaaaaaaaaaaaaaaaaaaaa")
	print(a)
	print(a[0])
	#print(a)
	
