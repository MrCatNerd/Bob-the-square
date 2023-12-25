__author__ = "Alon B.R."

import pygame

pygame.init()


class Button:
    def __init__(self, x, y, img) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.clicked = False
        self.clicked_once = False

        self.click_encoder = {
            "left": 0,
            "middle": 1,
            "right": 2,
            "side1": 3,
            "side2": 4,
            "side3": 5,
        }

    def update(
        self, window, click_type: str, point: tuple[int | float, int | float]
    ) -> None:
        x, y = point

        if (
            x > self.rect.x
            and x <= (self.rect.x + self.width)
            and y > self.rect.y
            and y <= (self.rect.y + self.height)
            and pygame.mouse.get_pressed()[self.click_encoder[click_type]]
        ):
            self.clicked = True
            self.clicked_once = True
        elif self.clicked is True:
            self.clicked = False

        window.blit(self.img, self.rect)
