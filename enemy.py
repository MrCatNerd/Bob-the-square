__author__ = "Alon B.R."

import pygame
from entity import Entity

# import math
from vector2 import Vector2
from settings import WIDTH, HEIGHT

pygame.init()

"""
class Projectile:
    def __init__(self, x, y, img) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.pmx = self.rect.x
        self.pmy = self.rect.y

        self.dx = 0
        self.dy = 0

        self.distance = 0
        self.speed = 5

        self.destroy = False

    def update(self, window, world, rect):
        if self.rect.colliderect(rect):
            self.destroy = True
        elif self.destroy is True:
            self.destroy = False
        else:
            for tile in world.tile_data:
                if self.rect.colliderect(tile.rect) and self.destroy is False:
                    self.destroy = True

        if not self.distance:
            mx, my = rect.x, rect.y  # pygame.mouse.get_pos()

            self.radians = math.atan2(my - self.pmy, mx - self.pmx)
            self.distance = int(math.hypot(mx - self.pmx, my - self.pmy))

            self.dx = math.cos(self.radians)
            self.dy = math.sin(self.radians)

            self.pmx = mx
            self.pmy = my

        if self.distance:
            self.distance -= 1
            self.rect.x += self.dx
            self.rect.y += self.dy

        window.blit(self.img, self.rect)
        if self.distance:
            pygame.draw.circle(window, (255, 0, 0), (self.pmx, self.pmy), 5, 0)
"""


class Projectile:
    def __init__(self, x, y, img) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.attacking = False
        self.collide_player = False
        self.collide_tiles = False
        self.out_of_screen = False
        self.destroy = False

    def attack(self, window, world, rect, direction: Vector2, speed, bullet_list):
        if self.attacking is False:
            self.direction = Vector2(direction.get_x(), direction.get_y())
            self.attacking = True

        dx = 0
        dy = 0

        dx += speed * self.direction.x
        dy += speed * self.direction.y

        if self.rect.colliderect(rect):
            self.collide_player = True
        elif self.collide_player is True:
            self.collide_player = False

        collide_tiles_list = [False]
        for tile in world.tile_data:
            if self.rect.colliderect(tile.rect):
                collide_tiles_list.append(True)
        self.collide_tiles = any(collide_tiles_list)

        if (self.rect.x + self.width < 0 or self.rect.x > WIDTH) or (
            self.rect.y + self.height < 0 or self.rect.y > HEIGHT
        ):
            self.out_of_screen = True
        elif self.out_of_screen is True:
            self.out_of_screen = False

        touching_bullets_list = [False]
        for bullet in bullet_list:
            if self.rect.colliderect(bullet.rect):
                touching_bullets_list.append(True)
        self.destroy = any(touching_bullets_list)

        self.rect.x += dx
        self.rect.y += dy

        window.blit(self.img, self.rect)
        # pygame.draw.rect(window, (255, 0, 255), self.rect, 3)


class Enemy(Entity):
    def __init__(
        self, x, y, img, speed, movement_range, health: int, mass, projectile_img
    ):
        super().__init__(x, y, img, speed, movement_range, health, mass)
        self.collide_player = False
        self.collide_projectile = False
        self.projectile_img = projectile_img
        self.projectile_list = []

    # update is in subclass

    def attack(self, window, world, rect, speed, attack, game, bullet_list) -> None:
        if self.rect.colliderect(rect):
            self.collide_player = True

        if attack is True:
            self.projectile_list.append(
                Projectile(self.rect.x, self.rect.y, self.projectile_img)
            )

        if len(self.projectile_list) > 0:
            for projectile in self.projectile_list:
                projectile.attack(
                    window, world, rect, self.move_direction, speed, bullet_list
                )
                if projectile.collide_tiles is True or projectile.destroy is True:
                    self.projectile_list.remove(projectile)

                elif projectile.collide_player is True:
                    self.collide_projectile = True
                    self.projectile_list.remove(projectile)
        game.enemy_attack = False

    @property
    def out_of_lives(self) -> bool:
        return not (self.health > 0)
