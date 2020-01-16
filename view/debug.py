import ressources.config


def velocity_stat(pop):
    if len(pop):
        return (sum(b.velocity for b in pop) / len(pop), max(b.velocity for b in pop), min(b.velocity for b in pop))
    return (0, 0, 0)

def mass_stat(pop):
    if len(pop):
        return (sum(b.masse for b in pop) / len(pop), max(b.masse for b in pop), min(b.masse for b in pop))
    return (0, 0, 0)

def perception_stat(pop):
    if len(pop):
        return (sum(b.perception for b in pop) / len(pop), max(b.perception for b in pop), min(b.perception for b in pop))
    return (0, 0, 0)

def memory_stat(pop):
    if len(pop):
        return (sum(b.memory_points for b in pop) / len(pop), max(b.memory_points for b in pop), min(b.memory_points for b in pop))
    return (0, 0, 0)

def total_food(grille):
    s = 0
    for i in range(ressources.config.para.TAILLE):
        for j in range(ressources.config.para.TAILLE):
            s += grille[i][j].food
    return s


def init_stats():
    """initialise les noms des statistiques à afficher sur l'interface GUI
    Les deux premières valeurs sont obligatoirement Day et Tick
    Retourne un tableau de strings."""
    return ["Day",
            "Tick",
            "Population",
            "Food",
            "Mass",
            "Velocity",
            "Perception",
            "Memory"]


def update_stats(grille, liste_bobs, tick):
    """met à jour les statistiques pour la GUI
    Les deux premières valeurs sont obligatoirement Day et Tick
    Retourne un tableau des valeurs des statistiques
    Les valeurs peuvent des nombres (int, float) ou des tuples"""

    return [tick // ressources.config.para.TICK_DAY + 1,
            tick % ressources.config.para.TICK_DAY,
            len(liste_bobs),
            int(total_food(grille) / ressources.config.para.ENERGY_FOOD),
            mass_stat(liste_bobs),
            velocity_stat(liste_bobs),
            perception_stat(liste_bobs),
            memory_stat(liste_bobs)
            ]

def update_stats_graphs(grille, liste_bobs, tick):
    """ retourne un dictionaire avec les statistiques pour l'affichage en Graph"""
    return {'ticks':tick,
            'days': tick / ressources.config.para.TICK_DAY,
            'pop': len(liste_bobs),
            'food': int(total_food(grille) / ressources.config.para.ENERGY_FOOD),
            'mass': mass_stat(liste_bobs),
            'velocity': velocity_stat(liste_bobs),
            'perception': perception_stat(liste_bobs),
            'memory': memory_stat(liste_bobs)
            }