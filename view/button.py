import pygame
from ressources.sliders import *
from view.gui import *


class Button:
    def __init__(self, txt, location, action, bg=WHITE, fg=BLACK, size=(80, 30),
                 font_name="Verdana", font_size=16):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s // 2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = Gui().round_rect(surface, pygame.Rect(size), bg)

        self.action = action
        # self.config = config.para

    def draw(self, screen):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY  # mouseover color

