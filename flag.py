__author__ = "Alon B.R."

import pygame

pygame.init()


class Flag:
    def __init__(self, x, y, img, game) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.game = game

    def update(self, window, rect):
        if self.rect.colliderect(rect):
            self.game.next_level()

        window.blit(self.img, self.rect)
