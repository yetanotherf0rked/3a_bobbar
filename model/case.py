import pygame

import ressources.config


class Case:

    def __init__(self, x, y):
        self.config = ressources.config.para
        self.x = x
        self.y = y
        self.food = 0
        self.place = []  # Contenue de la Case
        self.type = "Normal"
        self.floor = None
        self.deco = False
        self.nbPerception = 0

    def draw(self, surface, xdec, ydec, Px_init, Py_init, depx, depy, cx, deco):
        x, y = self.x, self.y
        self.couleur = (38, 37, 42)
        if self.type == "Perception":
            self.couleur = (max(0, 173 - 20 * self.nbPerception), max(0, 205 - 20 * self.nbPerception), 226)
        elif self.config.active_biome:
            if self.floor == "Grass":
                self.couleur = (120,143,1)
            elif self.floor == "Sand":
                self.couleur = (249,198,133)
            elif self.floor == "Water":
                self.couleur = (135,229,255)
            elif self.floor == "Lava":
                self.couleur = (227,101,23)

        pygame.draw.polygon(surface, self.couleur,
                            [(cx + Px_init + depx + xdec * (x - y - 1), Py_init + depy + ydec * (x + y + 1)),
                             (cx + Px_init + depx + xdec * (x - y), Py_init + depy + ydec * (x + y)),
                             (cx + Px_init + depx + xdec * (x - y + 1), Py_init + depy + ydec * (x + y + 1)),
                             (cx + Px_init + depx + xdec * (x - y), Py_init + depy + ydec * (x + y + 2))])
        if self.config.show_Bord_Case:
            pygame.draw.line(surface, (228, 226, 232),
                             (cx + Px_init + depx + xdec * (x - y - 1), Py_init + depy + ydec * (x + y + 1)),
                             (cx + Px_init + depx + xdec * (x - y), Py_init + depy + ydec * (x + y)))
            pygame.draw.line(surface, (228, 226, 232),
                             (cx + Px_init + depx + xdec * (x - y), Py_init + depy + ydec * (x + y)),
                             (cx + Px_init + depx + xdec * (x - y + 1), Py_init + depy + ydec * (x + y + 1)))
        if self.deco and self.config.show_Nature:
            if self.floor == "Grass":
                surface.blit(deco, (Px_init + cx - 16 - 3 + xdec * (x - y) + depx, Py_init + 7 - 45 + ydec * (x + y + 1) + depy))
            if self.floor == "Water":
                surface.blit(deco, (Px_init + cx - 20 + 16 + xdec * (x - y) + depx, Py_init - 30 + 10 + ydec * (x + y + 1) + depy))
        self.nbPerception = 0
        self.type = "Normal"

    def drawMap(self, surface, xdec, Px_init):
        x = int(xdec / 2.5)
        if self.food != 0:
            couleur = (166, 230, 38)
        else:
            couleur = self.couleur
        initx, inity = int(Px_init / 5), int(Px_init / 5)
        pygame.draw.rect(surface, couleur, (initx + self.x * x, inity + self.y * x, x, x))
        if self.config.show_Bord_Case:
            pygame.draw.line(surface, (228, 226, 232), (initx + self.x * x, inity + self.y * x),
                             (initx + self.x * x + x, inity + self.y * x))
            pygame.draw.line(surface, (228, 226, 232), (Px_init / 5 + self.x * x, Px_init / 5 + self.y * x),
                             (Px_init / 5 + self.x * x, Px_init / 5 + self.y * x + x))
        if self.place != []:
            couleur = (255, 255, 255)
            for bob in self.place:
                if bob.bobController.select:
                    couleur = (255, 0, 0)
                    break
            radius = int(x / 2)
            pygame.draw.circle(surface, couleur, (initx + self.x * x + radius + 1, inity + self.y * x + radius + 1),
                               radius)

    def copie(self):
        case = Case(self.x, self.y)
        case.food = self.food
        case.place = [bob.copie() for bob in self.place]
        case.type = self.type
        case.floor = self.floor
        case.deco = self.deco
        self.type = "Normal"
        return case

    def bobCase(self, n, x, y, xdec, ydec):
        if n == 1:
            return [(xdec * (x - y), ydec * (x + y + 1))]
        if n == 2:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]
        if n == 3:
            return [(xdec * (x - y), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]
        if n == 4:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]
        if n == 5:
            return [(xdec * (x - y - 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 - 1 / 4)),
                    (xdec * (x - y), ydec * (x + y + 1)),
                    (xdec * (x - y - 1 / 4), ydec * (x + y + 1 + 1 / 4)),
                    (xdec * (x - y + 1 / 4), ydec * (x + y + 1 + 1 / 4))]
