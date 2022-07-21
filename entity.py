__author__ = "Alon B.R."

import pygame
from settings import SCALE, GRAVITY
from vector2 import Vector2

pygame.init()


class Entity:
    def __init__(self, x, y, img, speed, movement_range, health, mass) -> None:
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health

        self.movement_range = movement_range
        self.speed = speed
        self.move_counter = 0
        self.move_direction: Vector2 = Vector2(1, 0)

        self.mass = mass
        self.acceleration: float = (self.mass * GRAVITY) / SCALE
        self.velocity = Vector2(0, 0)

    def update(self, window, world, dt) -> None:
        dx = 0
        dy = 0

        # movement
        dx += self.speed * self.move_direction.x
        self.move_counter += abs(self.speed)
        if abs(self.move_counter) > self.movement_range:
            self.move_direction.x *= -1
            self.move_counter *= -1

        self.velocity.y += self.acceleration * dt

        dx += self.velocity.x
        dy += self.velocity.y

        for tile in world.tile_data:
            # check for collision in y
            if tile.rect.colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                if dy >= 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.velocity.y = 0
                elif dy < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.velocity.y = 0

            # check collision in x
            if tile.rect.colliderect(
                self.rect.x + dx, self.rect.y, self.width, self.height
            ):
                if dx >= 0:
                    dx = tile.rect.x - (self.rect.x + self.width)
                if dx < 0:
                    dx = (tile.rect.x + tile.width) - self.rect.x

        self.rect.x += dx
        self.rect.y += dy
        window.blit(self.img, self.rect)
