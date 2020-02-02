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
        self.image_sun = pygame.transform.scale(sun, (200, 200))
        self.image_pluie = pygame.transform.scale(pluie, (200, 200))
        self.image_fog = pygame.transform.scale(fog, (200, 200))
        self.image_hail = pygame.transform.scale(grele, (200, 200))
        self.image_sandstorm = pygame.transform.scale(sandstorm, (300, 150))
        self.blit = None