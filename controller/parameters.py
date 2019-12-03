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
        """default :        Dictionnaire initialisateur des paramètres
                            Sert à automatiser l'initialisation des sliders
                            Les paramètres sont à initialiser avec la méthode make
                            nom_du_paramètre:(valeur_min, valeur_initiale, valeur_max, type=int ou float,
                            show=False si l'on veut cacher le paramètre)

            actual :        Dictionnaire contenant les paramètres en temps réel
                            C'est lui qui contiendra les valeurs en temps réel
                            nom_du_paramètre:valeur

            make(name, min, init, max, type=int, show=True) :
                            Méthode pour initialiser vos paramètres
                            type = int par défaut
                            show = True génère un slider pour le paramètre

            get(param) :    Retourne la valeur du paramètre dans Actual
                            Exemple d'appel :
                                parameters = Parameters()
                                ...
                                ...
                                bob.energy = parameters.get("Son Energy") #renvoie la valeur du slider Son Energy

            set(param) :    Permet de mettre à jour le dictionnaire Actual
        """

        # default : nom_du_paramètre:(valeur_min, valeur_initiale, valeur_max, type=int ou float, True : afficher le paramètre dans le menu)
        self.default = {}
        # actual : nom_du_paramètre:valeur
        self.actual = {}

        # On initialise les paramètres avec la méthode make
        self.make("Food Number", 2, NB_FOOD, 250)
        self.make("Food Energy", 50, ENERGY_FOOD, 150)
        self.make("Spawn Energy", 50, ENERGY_SPAWN, 150)
        self.make("Energy Cost while Moving", 0.0, ENERGY_MOVE, 5.0, float)
        self.make("Energy Cost at Stay", 0.0, ENERGY_STAY, 5.0, float)
        self.make("Max Energy", 50, ENERGY_MAX, 300)
        self.make("Mother Energy", 25, ENERGY_MOTHER, 75)
        self.make("Son Energy",25, ENERGY_SON, 75)
        # self.make("Tick")
        # self.make("Day")

        # on initialise les valeurs d'Actual aux valeurs initiales contenues dans Default
        for k,v in self.default.items():
            self.actual[k] = v[1]

    def make(self, name, min=0, init=0, max=0, type=int, show=True):
        self.default[name] = (min, init, max, type, show)

    def get(self, param):
        return self.actual[param]

    def set(self, param, value):
        self.actual[param] = value