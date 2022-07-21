__author__ = "Alon B.R."

import pygame

pygame.init()


class Lava:
    def __init__(self, x, y, img):
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.touched = False

    def update(self, window, rect):
        if self.rect.colliderect(rect):
            self.touched = True
        elif self.touched is True:
            self.touched = False

        window.blit(self.img, self.rect)
