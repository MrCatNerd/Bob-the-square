__author__ = "Alon B.R."

import pygame
from settings import WIDTH, HEIGHT, SCALE, GRAVITY
from vector2 import Vector2
from bullet import Bullet
from os.path import join as join_path

pygame.init()


def assets(path) -> str:
    return join_path("Assets", str(path))


class Player:
    def __init__(self, x, y, img, mass, health) -> None:
        self.death = False
        self.health = health

        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mass = mass
        self.acceleration = (self.mass * GRAVITY) / SCALE
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(1, 0)
        self.bullet_list = []
        self.bullet_img = pygame.transform.scale(
            pygame.image.load(assets("bullet.png")), (40, 20)
        )

        self.jumped = False

        self.reload_time = 50
        self.reload = self.reload_time

        self.dash_power = 17
        self.dash_slide = 1
        self.pressed_dash = False

    def update(self, window, world, dt):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        touching_tiles = [False]
        for tile in world.tile_data:
            if tile.rect.colliderect(
                (self.rect.x, self.rect.y + 1, self.width, self.height)
            ):
                touching_tiles.append(True)
        self.touching_tiles = any(touching_tiles)

        self.velocity.y += self.acceleration
        if keys[pygame.K_SPACE]:
            if self.reload >= self.reload_time:
                self.pressed_dash = True
                self.bullet_list.append(
                    Bullet(self.rect.x, self.rect.y, self.bullet_img, 1)
                )
                self.reload = 0
        if self.reload < self.reload_time:
            self.reload += 1

        if self.pressed_dash is True:
            dx += (self.dash_power - self.dash_slide) * self.direction.x
            self.dash_slide += 1
            if self.dash_slide > self.dash_power:
                self.dash_slide = 1
                self.pressed_dash = False

        if (
            (keys[pygame.K_w] or keys[pygame.K_UP])
            and self.jumped is False
            and self.touching_tiles is True
        ):
            self.velocity.y = -7
            self.jumped = True
        elif self.jumped is True and not (
            keys[pygame.K_w] or keys[pygame.K_UP] and self.jumped
        ):
            self.jumped = False

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        ):
            if self.direction.x == 1:
                self.direction.x = 1
            elif self.direction.x == -1:
                self.direction.x = -1
        else:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 5 * dt
                self.direction.x = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 5 * dt
                self.direction.x = 1

        # handle bullets
        if len(self.bullet_list) > 0:
            for bullet in self.bullet_list:
                bullet.attack(window, self.direction, 10, world)
                if bullet.destroy:
                    self.bullet_list.remove(bullet)

        # add gravity
        self.velocity.y = min(self.velocity.y, 49)
        dy += self.velocity.y
        dx += self.velocity.x

        # check for collision
        for tile in world.tile_data:
            # check collision in y direction
            if tile.rect.colliderect(
                self.rect.x,
                self.rect.y + dy,
                self.width,
                self.height,
            ):
                # check if jumping or falling
                if dy >= 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.velocity.y = 0
                elif dy < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.velocity.y = 0

            # check collision in x direction
            if tile.rect.colliderect(
                self.rect.x + dx, self.rect.y, self.width, self.height
            ):
                if dx >= 0:
                    dx = tile.rect.x - (self.rect.x + self.width)
                if dx < 0:
                    dx = (tile.rect.x + tile.width) - self.rect.x

        if self.death is False and self.health <= 0:
            self.death = True

        self.rect.x += dx
        self.rect.y += dy
        window.blit(self.img, self.rect)
        # pygame.draw.rect(window, (255, 0, 0), self.rect, 2)
