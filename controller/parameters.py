#Nourriture sur la carte 200
NB_FOOD = 200
#Energy par food 100
ENERGY_FOOD = 100
#Energy par spawn de Bob 100
ENERGY_SPAWN = 100
#Cout d'un déplacement 1 -> velocity**2
ENERGY_MOVE = 1
#Cout sans déplacement 0.5
ENERGY_STAY = 0.5
#Energy_max d'un Bob 200
ENERGY_MAX = 200
#Energy après naissance 50
ENERGY_MOTHER = 50
#Energy enfant 50
ENERGY_SON = 50

class Parameters:

    def __init__(self):
        """ À retenir :
                - une instance parameters de la classe Parameters est déclarée dans constantes.py
                - cette instance permet d'accéder aux paramètres depuis n'importe quel fichier .py
                - on déclare un nouveau paramètre avec make()
                - on accède au paramètre avec get()
                - on modifie le paramètre avec set()


            default :       Dictionnaire initialisateur des paramètres
                            Sert à automatiser l'initialisation des sliders
                            nom_du_paramètre:(valeur_min, valeur_initiale, valeur_max, type=int ou float,
                            show=False si l'on veut cacher le paramètre)

            actual :        Dictionnaire contenant les valeurs des paramètres en temps réel
                            Il est mis à jour avec la méthode gui.update_values()
                            nom_du_paramètre:valeur
        """

        # default : nom_du_paramètre:(valeur_min, valeur_initiale, valeur_max, type=int ou float, True : afficher le paramètre dans le menu)
        self.default = {}

        # actual : nom_du_paramètre:valeur
        self.actual = {}

        # Créez vos paramètres ici
        self.make("Food Number", 2, NB_FOOD, 250)
        self.make("Food Energy", 50, ENERGY_FOOD, 150)
        self.make("Spawn Energy", 50, ENERGY_SPAWN, 150)
        self.make("Energy Cost while Moving", 0.0, ENERGY_MOVE, 5.0, float)
        self.make("Energy Cost at Stay", 0.0, ENERGY_STAY, 5.0, float)
        self.make("Max Energy", 50, ENERGY_MAX, 300)
        self.make("Mother Energy", 25, ENERGY_MOTHER, 75)
        self.make("Son Energy",25, ENERGY_SON, 75)
        # self.make("Tick", show=False)
        # self.make("Day", show=False)
        # self.make("Population", show=False)

        # on initialise les valeurs d'Actual avec les valeurs initiales déclarées ci-dessus
        for k,v in self.default.items():
            self.actual[k] = v[1]

    def make(self, name, min=0, init=0, max=0, type=int, show=True):
        """Initialise un paramètre
             type = int ou float
             show = True génère un slider pour le paramètre
                  = False crée un paramètre mais ne génère pas de slider dans l'interface gui"""
        self.default[name] = (min, init, max, type, show)

    def get(self, param):
        """Retourne la valeur du paramètre dans Actual
            Exemple : bob.energy = parameters.get("Son Energy") renvoie la valeur actuelle du slider Son Energy"""
        return self.actual[param]

    def set(self, param, value):
        """Permet de mettre à jour un paramètre dans le dictionnaire Actual. Utilisée dans gui.update_values()"""
        self.actual[param] = value