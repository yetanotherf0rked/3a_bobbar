from ressources.constantes import TICK_DAY,TAILLE,NB_FOOD,ENERGY_FOOD

def velocity_stat(pop):
	return (sum(b.velocity for b in pop)/len(pop),max(b.velocity for b in pop),min(b.velocity for b in pop))

def mass_stat(pop):
	return (sum(b.masse for b in pop)/len(pop),max(b.masse for b in pop),min(b.masse for b in pop))

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
    print(f'masse moyenne : {mstat[0]} masse max : {mstat[0]} masse min : {mstat[0]}')
    vstat =velocity_stat(liste_bobs)
    print(f'vitesse moyenne : {vstat[0]} vitesse max : {vstat[0]} vitesse min : {vstat[0]}')
    print('food :')
    print_bar(NB_FOOD*ENERGY_FOOD,total_food(grille))




