from ressources.config import TICK_DAY,TAILLE,NB_FOOD,ENERGY_FOOD

def velocity_stat(pop):
	return (sum(b.velocity for b in pop)/len(pop),max(b.velocity for b in pop),min(b.velocity for b in pop))

def mass_stat(pop):
	return (sum(b.masse for b in pop)/len(pop),max(b.masse for b in pop),min(b.masse for b in pop))

def perception_stat(pop):
	return (sum(b.perception for b in pop)/len(pop),max(b.perception  for b in pop),min(b.perception  for b in pop))

def memory_stat(pop):
	return (sum(b.memory_points for b in pop)/len(pop),max(b.memory_points for b in pop),min(b.memory_points for b in pop))

def total_food(grille):
    s=0
    for i in range(TAILLE):
        for j in range(TAILLE):
            s+=grille[i][j].food
    return s

def print_bar(maxd, dat, size=50):
    length = int(dat)*size//maxd
    for _ in range(length):
        print('█',end='')
    for _ in range(size-length) :
        print(' ',end='')
    print(f'{dat}/{maxd}')

def drawStats(grille, liste_bobs, tick):
    print(f'Jour : {tick//TICK_DAY}')
    print_bar(TICK_DAY, tick%TICK_DAY)
    print(f'population : {len(liste_bobs)}' )
    mstat =mass_stat(liste_bobs)
    print(f'masse moyenne : {mstat[0]:.3f} masse max : {mstat[1]:.3f} masse min : {mstat[2]:.3f}')
    vstat =velocity_stat(liste_bobs)
    print(f'vitesse moyenne : {vstat[0]:.3f} vitesse max : {vstat[1]:.3f} vitesse min : {vstat[2]:.3f}')
    pstat=perception_stat(liste_bobs)
    print(f'perception moyenne : {pstat[0]:.3f} perception max : {pstat[1]:.3f} perception min : {pstat[2]:.3f}')
    memstat=memory_stat(liste_bobs)
    print(f'mémoire moyenne : {memstat[0]:.3f} mémoire max : {memstat[1]:.3f} mémoire min : {memstat[2]:.3f}')
    print('food :')
    print_bar(NB_FOOD*ENERGY_FOOD,total_food(grille))



# Affichage du tick, du day et de la population
#            day,
#            tick,
#            len(self.listebob),
#            total_food(self.grille),
#            mass_stat(self.listebob),
#            velocity_stat(self.listebob),
#            perception_stat(self.listebob),
#            memory_stat(self.listebob),

# food_text = thorpy.make_text("Total Food", FONT_SIZE, WHITE)
# mass_text = thorpy.make_text("Mass (moy, min, max)", FONT_SIZE, WHITE)
# velocity_text = thorpy.make_text("Velocity (moy, min, max)", FONT_SIZE, WHITE)
# perception_text = thorpy.make_text("Perception (moy, min, max)", FONT_SIZE, WHITE)
# memory_text = thorpy.make_text("Memory (moy, min, max)", FONT_SIZE, WHITE)
# food_number = thorpy.make_text("  ", FONT_SIZE, WHITE)
# mass_number = thorpy.make_text("  ", FONT_SIZE, WHITE)
# velocity_number = thorpy.make_text("  ", FONT_SIZE, WHITE)
# perception_number = thorpy.make_text("  ", FONT_SIZE, WHITE)
# memory_number = thorpy.make_text("  ", FONT_SIZE, WHITE)
# self.box_food_display = thorpy.Box(elements=[food_text, food_number])
# self.box_mass_display = thorpy.Box(elements=[mass_text, mass_number])
# self.box_velocity_display = thorpy.Box(elements=[velocity_text, velocity_number])
# self.box_perception_display = thorpy.Box(elements=[perception_text, perception_number])
# self.box_memory_display = thorpy.Box(elements=[memory_text, memory_number])
