import pygame

import ressources.config
class Meteo_picto():

    def __init__(self):
        self.config = ressources.config.para
        pluie = pygame.image.load(self.config.image_PLUIE).convert_alpha()
        sun = pygame.image.load(self.config.image_SUN).convert_alpha()
        fog = pygame.image.load(self.config.image_FOG).convert_alpha()
        grele = pygame.image.load(self.config.image_GRELE).convert_alpha()
        sandstorm = pygame.image.load(self.config.image_SANDSTORM).convert_alpha()
        self.image_sun = pygame.transform.scale(sun, (100, 100))
        self.image_pluie = pygame.transform.scale(pluie, (100, 100))
        self.image_fog = pygame.transform.scale(fog, (100, 100))
        self.image_hail = pygame.transform.scale(grele, (100, 100))
        self.image_sandstorm = pygame.transform.scale(sandstorm, (100, 100))
        self.blit = None