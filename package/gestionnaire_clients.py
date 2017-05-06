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
		self._tableau_de_connexions = []

	#def __del__(self):
		"""Méthode appelée quand on souhaite supprimer la classe Gestionnaire_clients
		l'objectif et de pouvoir fermer les connexion une à une du tableau pour ensuite fermer integralement la classe"""
	#	pass



	def __str__(self):
		"""Méthode appelée quand on souhaite afficher la classe robot"""
		msg = "clients: robots("
		for clients in self._tableau_de_connexions:
			msg += "{} ,".format(clients)
		msg += ") \n"

		return msg



	def __getitem__(self, index):
		"""Cette méthode spéciale est appelée quand on fait objet[index]
		Elle redirige vers self._dictionnaire[index]"""
		connexion = self._tableau_de_connexions[index]
		return connexion._information_connexion

		

	def _get_tableau_de_connexions(self):
		return self._tableau_de_connexions



	def _set_tableau_de_connexions(self, nouvelle_connexion):
		#if isinstance(nouvelle_connexion, list):
		#	raise TypeError("""Erreur le parametre nouvelle_connexion n'est pas de type list mais de type {}""".format(type(nouvelle_connexion)))
		self._tableau_de_connexions.append(cn.Connexion(connexion = nouvelle_connexion))



	def ajouter_connexion(self, nouvelle_connexion):
		self._tableau_de_connexions.append(nouvelle_connexion)


	tableau_de_connexions = property(fget = _get_tableau_de_connexions, fset = _set_tableau_de_connexions)



if __name__ == "__main__":

	a = Gestionnaire_clients()
	a.tableau_de_connexions = ["127.0.0.1", 12800]
	a.tableau_de_connexions = ["127.0.0.2", 12800]
	a.tableau_de_connexions = ["127.0.0.3", 12800]
	print(a)
	
	#erreur je lui retourne la class connexions et non l'attribut socket de connexion
	#clients_a_lire, wlist, xlist = sc.select(tableau_des_clients.tableau_de_connexions, [], [], 0.05)