import pygame
from ressources.sliders import *
from view.gui import *


class Button:
    def __init__(self, txt, pos, gui, bg=WHITE, fg=BLACK, size=(80, 30),
                 font_name="Verdana", font_size=16):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size
        self.pos = pos

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s // 2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.gui = gui
        self.rect = self.gui.round_rect(self.surface, pygame.Rect(self.pos, self.size), self.bg)

    def draw(self, screen):
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.blit = screen.blit(self.surface, self.rect)

    def mouse_click(self):
        self.bg, self.fg = self.fg, self.bg
