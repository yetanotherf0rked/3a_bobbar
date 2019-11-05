from ressources.constantes import TICK_DAY

def velocity_stat(pop):
	return (sum(b.velocity for b in pop)/len(pop),max(b.velocity for b in pop),min(b.velocity for b in pop))

def mass_stat(pop):
	return (sum(b.masse for b in pop)/len(pop),max(b.masse for b in pop),min(b.masse for b in pop))


def drawStats(grille,liste_bobs,tick):
    print(f'Jour : {tick//TICK_DAY} tick:{tick%TICK_DAY}/{TICK_DAY}')
    print(f'population : {len(liste_bobs)}' )
    mstat =mass_stat(liste_bobs)
    print(f'masse moyenne : {mstat[0]} masse max : {mstat[0]} masse min : {mstat[0]}')
    vstat =velocity_stat(liste_bobs)
    print(f'vitesse moyenne : {vstat[0]} vitesse max : {vstat[0]} vitesse min : {vstat[0]}')



