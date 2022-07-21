__author__ = "Alon B.R."

import pygame
from os.path import join

pygame.init()

WIDTH = 800
HEIGHT = 800
TITLE = "SmartGameJam2022"
FPS = 60
LOGO = pygame.image.load(join("Assets", "logo.png"))
FONT_SIZE = 25
MIDIUM_FONT_SIZE = 50
GIANT_FONT_SIZE = 100
FONT = pygame.font.SysFont("calibri", FONT_SIZE)
MIDIUM_FONT = pygame.font.SysFont("calibri", MIDIUM_FONT_SIZE)
GIANT_FONT = pygame.font.SysFont("calibri", GIANT_FONT_SIZE)
ANTI_ALIASING = True
BG_COLOR: tuple = (0, 0, 0)
dt = 1
SCALE = 50
GRAVITY = 9.8
TILE_SIZE = 50
