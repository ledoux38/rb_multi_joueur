#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

class Scene:
	"""class qui qui cree l'environnement du jeux"""
	def __init__(self,nom,chaine):

		if not isinstance(nom,str):
			raise TypeError("erreur parametre nom doit etre de type <str> et non de type <{}>".format(type(nom)))
		
		if not isinstance(chaine,str):
			raise TypeError("erreur parametre chaine doit etre de type <str> et non de type <{}>".format(type(chaine)))

		"""instancie la scene.
		attibut:
		nom: nom de la carte 
		chaine: chaine de caractere qui represente le labyrinthe.
		"""

		self.carte = Carte(nom,chaine)
		self.robot = Robot("X",self.carte.get_les_coordonnees_de_la_valeur("X"))
		self.pts_arriver= self.carte.get_les_coordonnees_de_la_valeur("U") 

	def phase_de_deplacement(self):
		"""methode principale qui  gere la phase de deplacement"""

		#affichage de la carte"""
		print(self.carte.representation_labyrinthe_str())

		#demande a l'utilisateur un mouvement pour le robot"""
		direction,num = self.inter_utilisateur_dde_mouvement()

		return (direction, num)

	def coordonnee(self, direction):

		if not isinstance(direction,str):
			raise TypeError("parametre direction doit etre de type <str>")
		
		coordonnee = list(self.robot.mouvement_robot(direction))

		"""on retourne les coordonees"""
		return coordonnee		

	def inter_utilisateur_dde_mouvement(self):
		"""methode qui interagit avec l'utilisateur"""
		while True:
			"""demande la direction"""
			chaine_presentation="""direction: <N><S><E><O>	<Q> Quitter \n votre choix?: """
			direction = input(chaine_presentation)
			try:
				direction, num= self.analyse_entree_utilisateur(direction)
			except ValueError:
				print("erreur lors de la saisi veuiller recommencer")
				continue
			else:
				return (direction, num)

	def analyse_entree_utilisateur(self,chaine):
		"""methode qui verifie la chaine et recuperent les numeros ainqi que les lettres"""

		"""verfication des parametres de la chaine"""
		if not isinstance(chaine,str):
			raise TypeError("erreur typage incorrect le parametre chaine doit etre de type <str> et non de type <{}>".format(type(chaine)))
		chaine_numero = chaine_alpha = str()

		"""verification de la chaine si elle comporte des minuscules"""
		if chaine is not chaine.isupper():
			chaine= chaine.upper()

		"""verfication de chaque caractere"""
		for caractere in chaine:

			"""si caractere est un numero ou sinon si c'est une lettre sinon erreur"""
			if caractere.isdigit():
				chaine_numero += caractere
			
			elif caractere.isalpha():
				if not caractere in "NSEOQ" or not len(chaine_alpha) != 1:
					raise ValueError("erreur nombre de lettre superieur a 1 ou caractere different de NSEOQ")
				else:
					chaine_alpha += caractere
			
			else:
				raise ValueError("le caractere <{}> est incorrect".format(caractere))

		if chaine_numero == "":
			chaine_numero+="1"
			
		return (chaine_alpha,int(chaine_numero))

	def analyse_deplacement(self,coordonnee):
		"""methode qui valide les coordonnee envoyer"""
		
		if not isinstance(coordonnee,list):
			raise ("le parametre coordonnee n'est pas de type <list>")

		"""si valeur renvoyer et differente de "0" alors deplacement autorisé"""
		if self.carte.get_la_valeur_aux_coordonnees(coordonnee) !="O":
			return True
		else:
			return False

	def setCoordonnee(self,coordonnee):
		"""methode qui permute les cases entre le robot et la valeur du labyrinthe"""
			
		if not isinstance(coordonnee,list):
			raise TypeError("list attendu")
			
		"""remplacement du x par encienne valeur"""
		self.carte.set_la_valeur_aux_coordonnee(self.robot.encienCaractere,self.robot.coordonneeYX)
			
		"""recuperation de la nouvelle valeur au coordonnee donnee"""
		self.robot.encienCaractere = self.carte.get_la_valeur_aux_coordonnees(coordonnee)
			
		"""modification de la valeur au coordonnee donnee"""
		self.carte.set_la_valeur_aux_coordonnee(self.robot.valeur,coordonnee)
			
		"""nouvelle coordonnee du robot"""
		self.robot.coordonneeYX = coordonnee

	def verification_victoire(self):
		"""methode qui verifie la victoire"""

		if self.pts_arriver == self.robot.coordonneeYX:
			return True
		else:
			return False

class Robot:
	"""la classe robot et une classe qui permet de cree une entité avec une position X et Y et une forme"""
	def __init__(self,valeur,coordonneeYX):
		"""instancie le robot.
		le robot est representer par une valeur ex:: (X)
		et des coordonnes YX
		"""

		"""------------------------- verification parametres ----------------------"""
		if not isinstance(valeur,str):
			raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
				le parametre fourni à valeur doit etre de type <str> et non <{}>""".format(type(coordonneeYX)))

		if not len(valeur) == 1:
			raise ValueError("""erreur parametre <{}> incorrect!
				nombre de caractere autorisé dans le parametre est de 1. EX:"X" """.format(valeur))
		
		if not isinstance(coordonneeYX, list):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
					le parametre fourni à coordonneeYX doit etre de type <list> et non <{}>""".format(type(coordonneeYX)))

		for i in coordonneeYX:
			if not isinstance(i,int):
				raise TypeError("""Erreur lors de l'instanciation de la classe Robot!
		argument dans list doit etre de type int et non <{}>""".format(type(i)))				

		if not len(coordonneeYX) == 2:
			raise ValueError("""erreur parametre <{}> incorrect!
				nombre de d'axe autorisé dans le parametre est de 2. EX:"[X,Y]" """.format(coordonneeYX))
		
		self.valeur = valeur
		self.coordonneeYX = coordonneeYX
		self.encienCaractere = " "

	"""--------------------------------- Attribut -------------------------------------"""

	def mouvement_robot(self,direction):
		"""methode qui demande les coordonnees en fonction de la direction demander"""
		
		if not isinstance(direction,str):
			raise TypeError("erreur type <{}> incorrect! doit etre de type <str>".format(type(direction)))
		
		if len(direction)>1:
			raise ValueError("erreur le parametre <direction> doit etre egual à 1")
		
		y = self.coordonneeYX[0]
		x = self.coordonneeYX[1]
		mouvement = list()
		
		if direction == "N":
			y -=1
		
		elif direction == "S":
			y +=1
		
		elif direction == "E":
			x +=1
		
		elif direction == "O":
			x -=1
		
		else:
			raise ValueError("erreur le caractere du parametre direction est incorrect!")

		mouvement.append(y)
		mouvement.append(x)
		return mouvement

class Carte:
    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
    	"""procedure d'initialisation
    	la classe comporte comme attribut: - nom <str>
    									   - chaine <str>
    	"""

    	if not isinstance(nom,str):
    		raise TypeError("erreur le typage de la variable nom doit etre de type <str> et non <{}>".format(type(nom)))

    	if not isinstance(chaine,str):
    		raise TypeError("erreur le typage de la variable chaine doit etre de type <str> et non <{}>".format(type(chaine)))
    
    	self.nom= nom
    	self.labyrinthe = self.creer_labyrinthe_depuis_chaine(chaine)

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    def creer_labyrinthe_depuis_chaine(self,chaine):
    	""" je cree une list de list pour cree le labyrinthre"""
    	i = chaine + "\n"
    	ligne = []
    	labyrinthe = []


    	for y,x in enumerate(i):
    		if x != "\n":
    			ligne.append(x)

    		else:
    			ligne.append(x)
    			labyrinthe.append(ligne)
    			ligne = []
    	return labyrinthe

    def representation_labyrinthe_tableau(self):
    	"""representation du labyrinthe en tableau"""
    	for x in self.labyrinthe:
    		print(x)

    def representation_labyrinthe_str(self):
    	"""representation du labyrinthe en chaine de caractere"""
    	chaine=str()
    	for x in self.labyrinthe:
    		for y in x:
    			chaine += y  			
    	return chaine

    def get_la_valeur_aux_coordonnees(self,coordonnee):
    	"""on recupere la valeur directement au coordonnee choisi"""
    	valeur = self.labyrinthe[coordonnee[0]][coordonnee[1]]
    	return valeur

    def get_les_coordonnees_de_la_valeur(self,valeur="X"):
    	"""retourne les coordonnee de la valeur trouvé.
    	par defaut la valeur a chercher c'est X"""
    	liste = list()
    	for j,y in enumerate(self.labyrinthe):
    		for v,x in enumerate(y):
    			if x == valeur:
    				liste.append(j)
    				liste.append(v)
    	return liste

    def set_la_valeur_aux_coordonnee(self,valeur,coordonneeYX):
    	"""on modifie la valeur au coordonnée choisi"""
    	self.labyrinthe[coordonneeYX[0]][coordonneeYX[1]] = valeur
