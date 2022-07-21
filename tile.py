__author__ = "Alon B.R."

import pygame

pygame.init()


class Tile:
    def __init__(self, x, y, img, tag) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.tag = tag

    def update(self, window):

        window.blit(
            self.img,
            self.rect,
        )
        # pygame.draw.rect(
        # window,
        # (255, 255, 255),
        # self.rect,
        #  2,

    # )
