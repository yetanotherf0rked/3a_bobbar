class Config():

    def __init__(self):
        self.show_Minimap = True
        self.fullscreen = False
        self.show_Perception = False
        self.show_Bord_Case = False
        self.historique = False
        self.family_Reproduction = False
        self.family_Agression = False
        self.affichage = True
        self.active_biome = True
        self.settings = False
        self.show_Nature = True
        self.show_Food_ProgressBar = True
        self.restart = False
        self.weather = "Sun"

        # Tick par jour 100
        self.TICK_DAY = 100
        # Population initiale 100
        self.NB_POP = 100
        # Taille de la carte 100
        self.TAILLE = 100
        # Nourriture sur la carte 200
        self.NB_FOOD = 200
        # Energy par food 100
        self.ENERGY_FOOD = 100
        # Energy par spawn de Bob 100
        self.ENERGY_SPAWN = 100
        # Cout d'un déplacement 1 -> velocity**2
        self.ENERGY_MOVE = 1
        # Cout sans déplacement 0.5
        self.ENERGY_STAY = 0.5
        # Energy_max d'un Bob 200
        self.ENERGY_MAX = 200
        # Energy après naissance 50
        self.ENERGY_MOTHER = 50
        # Energy enfant 50
        self.ENERGY_SON = 50
        # Taux de mutation de la vitesse
        self.MUT_VELOCITY = 0.1
        # Taux de mutation de la masse
        self.MUT_MASSE = 0.1
        # taux de mutation de la perception
        self.MUT_PERCEPT = 1
        # taux de mutation de la memoire
        self.MUT_MEMORY = 1
        # Deplacement step
        self.DEP_STEP = 20
        # Energie min nescessaire pour la reproduction sexuée
        self.ENERGY_MIN_REPRO = 150
        # energie enfant de la reproduction sexuée
        self.ENERGY_SON_REPRO = 100
        # Energie dépensée lors de la reproduction sexuée
        self.ENERGY_REPRO = 150

        self.DIFF_AGE_FOR_REPRODUCTION = 500  # valeur en tick
        self.DISTANCE_TO_BE_IN_SAME_FAMILY=2

        self.HISTORIQUE_MAX = 1  # nombre de jour stocker en historique si besoin

        # self.WEATHER_ENERGY_COEFF = self.ENERGY_MAX * 1/(16 * self.TICK_DAY)
        # self.WEATHER_PERCEPTION_COEFF = 1/2
        # self.WEATHER_VELOCITY_COEFF = 2

        #parametres des graphiques
        self.show_graph = False
        self.g_animation = False
        self.g_parameters = {'x':"ticks",
                            'pop':True,
                            'energy':False,
                            'mass':False,
                            'velocity':False,
                            'memory':False,
                            'perception':False,
                            'food':False,
                            'age':False}
        self.g_update_rate = 1
        self.g_updated =False

        # Chargement des images
        self.image_BOB = "ressources/images/polar_bear_white.png"
        self.image_FOOD = "ressources/images/biere.png"
        self.image_LOGO = "ressources/images/logo_round_210.png"
        self.image_EARTH1 = "ressources/images/terre1 clair.png"
        self.image_EARTH2 = "ressources/images/terre2 clair.png"
        self.image_EARTH3 = "ressources/images/terre3 clair.png"
        self.image_EARTH4 = "ressources/images/terre4 clair.png"
        self.image_EARTH5 = "ressources/images/terre 1.png"
        self.image_EARTH7 = "ressources/images/Grass.png"
        self.image_EARTH6 = "ressources/images/terre 3.png"
        self.image_EARTH_WOW = "ressources/images/terrespec.png"
        self.image_REDBOB = "ressources/images/polar_bear_red.png"
        self.image_SOLEIL = "ressources/images/Soleil300x300.png"
        self.image_LUNE = "ressources/images/lune.png"
        self.image_EMPTY_BEER = "ressources/images/empty_beer_icon.png"
        self.image_TREE = "ressources/images/tree2.png"
        self.image_GRASS = "ressources/images/grass.png"


para = Config()
