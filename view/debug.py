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




