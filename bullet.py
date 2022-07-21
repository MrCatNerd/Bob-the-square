__author__ = "Alon B.R."

import pygame
from vector2 import Vector2
from settings import WIDTH, HEIGHT

pygame.init()


class Bullet:  # against enemies
    def __init__(self, x, y, img, strength) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.attacking = False
        self.strength = strength
        self.destroy = False

    def attack(self, window, direction, speed, world):
        if self.attacking is False:
            self.direction = Vector2(direction.get_x(), direction.get_y())
            self.attacking = True
        dx = 0
        dy = 0
        destroy = False

        for enemy in world.enemy_data:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.strength
                destroy = True
                #print(enemy.health)

            for projectile in enemy.projectile_list:
                if self.rect.colliderect(projectile.rect):
                    destroy = True

        for tile in world.tile_data:
            if self.rect.colliderect(tile.rect):
                destroy = True

        dx += speed * self.direction.x
        self.destroy = destroy
        self.rect.x += dx
        self.rect.y += dy
        window.blit(self.img, self.rect)
