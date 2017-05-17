#!/usr/bin/python3.5
# -*-coding:Utf-8 -* 
import copy
try:
	import package.elements_de_carte as el_carte
except:
	import elements_de_carte as el_carte

class Tableau:

	def __init__(self, tableau = None):
		self.tableau = copy.deepcopy(tableau)



	def __getitem__(self, index):
		"""Méthode appelée quand on souhaite retourner le tableau"""		
		if isinstance(index, tuple):
			y,x = index
			return self.tableau[y][x]
		else:
			return self.tableau[index]



	def __setitem__(self, index, valeur):
		"""Méthode appelée quand on souhaite modifier le tableau"""
		print("__setitem__ appeler")
		y,x = index
		self.tableau[y][x] = valeur

	def __copy__(copy):
		print("copy")
		objet = Tableau_carte()
		objet.tableau = typeAttribut(copy.tableau)
		return objet


	def __str__(self):
		"""Méthode appelée quand on souhaite afficher le tableau via un print()"""
		return self.tableau_en_str()



	def tableau_en_str(self):
		"""Méthode appelée quand on souhaite recuperer le tableau en chaine de caractere"""
		chaine=str()
		for j,y in enumerate(self.tableau):
			for v,x in enumerate(y):
				chaine += str(self.tableau[j][v])
			chaine +="\n"
		return chaine



if __name__ == "__main__":
	i = [[el_carte.Mur(),el_carte.Mur()],[el_carte.Mur(),el_carte.Mur()]]
	a = Tableau_carte(i)
	print(a)

	print("\n")
	print(a.retour_tableau_en_str())

