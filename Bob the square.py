__author__ = "Alon B.R."

import pygame
import os
import math
import random
import threading
import time

from vector2 import Vector2
from settings import (
    TILE_SIZE,
    WIDTH,
    HEIGHT,
    TITLE,
    FONT_SIZE,
    FONT,
    FPS,
    dt,
    BG_COLOR,
    ANTI_ALIASING,
    GIANT_FONT,
    GIANT_FONT_SIZE,
    MIDIUM_FONT,
    MIDIUM_FONT_SIZE,
    LOGO,
)
from player import Player
from button import Button
from tile import Tile
from entity import Entity
from enemy import Enemy
from coins_handler import HandleCoins
from coin import Coin
from lava import Lava
from flag import Flag
from star import Star

from sys import exit as stop_executing


def assets(path) -> str:
    return os.path.join("Assets", str(path))


class World:
    def __init__(self, data, TILE_SIZE, game):
        self.TILE_SIZE = TILE_SIZE
        # loading images
        self.grass_img = pygame.transform.scale(
            pygame.image.load(assets("grass.png")), (self.TILE_SIZE, self.TILE_SIZE)
        )

        # loading world
        self.tile_data = []
        self.enemy_data = []
        self.coin_data = []
        self.lava_data = []
        self.flag_data = []
        self.star_data = []
        self.entity_data = []
        y_index = 0
        for y in data:
            x_index = 0
            for x in y:
                if x == 0:
                    pass  # to save elif elif elif
                elif x == 1:
                    self.tile_data.append(
                        Tile(
                            x_index * self.TILE_SIZE,
                            y_index * self.TILE_SIZE,
                            self.grass_img,
                            "grass",
                        )
                    )
                elif x == 2:
                    self.enemy_data.append(
                        Enemy(
                            x_index * self.TILE_SIZE,
                            y_index * self.TILE_SIZE,
                            game.enemy_img,
                            5,
                            100,
                            3,
                            1.25,
                            game.enemy_projectile_img,
                        )
                    )
                elif x == 3:
                    self.coin_data.append(
                        Coin(
                            x_index * self.TILE_SIZE,
                            y_index * self.TILE_SIZE,
                            game.coin_img,
                        )
                    )
                elif x == 4:
                    self.lava_data.append(
                        Lava(
                            x_index * self.TILE_SIZE,
                            (y_index * self.TILE_SIZE) + self.TILE_SIZE // 2,
                            game.lava_img,
                        )
                    )

                elif x == 5:
                    self.flag_data.append(
                        Flag(
                            x_index * self.TILE_SIZE,
                            y_index * self.TILE_SIZE,
                            game.flag_img,
                            game,
                        )
                    )

                elif x == 6:
                    self.star_data.append(
                        Star(
                            x_index * self.TILE_SIZE,
                            y_index * self.TILE_SIZE,
                            game.star_img,
                        )
                    )

                elif x == 7:
                    self.entity_data.append(
                        Entity(
                            x_index * self.TILE_SIZE,
                            y_index * self.TILE_SIZE,
                            game.player_img,
                            4,
                            100,
                            3,
                            1.25,
                        )
                    )

                elif x == "x":
                    self.player_x = x_index * self.TILE_SIZE
                    self.player_y = y_index * self.TILE_SIZE
                x_index += 1
            y_index += 1


def timer_clock(delay, GAME, command: str, scale=None):  # thread
    if scale is None:
        while GAME.run:
            time.sleep(delay)
            exec(str(command))
    else:
        while GAME.run:
            time.sleep(delay * scale)
            exec(str(command))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game:
    def __init__(self):
        self.LOGO = LOGO
        self.TITLE = TITLE
        self.BG_COLOR = BG_COLOR
        self.FONT_SIZE = FONT_SIZE
        self.FONT = FONT
        self.TILE_SIZE = TILE_SIZE
        self.FPS = FPS
        self.dt = dt
        self.camera = Vector2(0, 0)

        self.level = 1
        self.stars = 0

        self.app = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption(self.TITLE)
        pygame.display.set_icon(LOGO)

        self.clock = pygame.time.Clock()

        self.run = True
        x = "x"
        self.world_data = [
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, x, 6, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 5, 0, 2, 0, 0, 0, 6, 0, 0, 2, 0, 0, 6, 5, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, x, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 3, 0, 1, 4, 4, 4, 4, 4, 4, 4, 1, 6, 1, 6, 5, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 4, 6, 4, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 4, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, x, 1, 2, 0, 6, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 4, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 4, 0, 0, 0, 0, 0, 0, 0, x, 0, 0, 0, 0, 0, 1],
                [1, 4, 0, 0, 0, 0, 1, 4, 4, 1, 0, 0, 0, 0, 0, 1],
                [1, 4, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 6, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 4, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 4, 4, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 4, 1, 0, 0, 1, 4, 4, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 4, 4, 4, 1, 1, 0, 0, 0, 2, 5, 2, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 6, 0, 6, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 4, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 4, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, x, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 5, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 7, 7, 7, 7, 7, 7, x, 7, 7, 7, 7, 7, 7, 7, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        ]

        # loading images
        self.player_img = pygame.transform.scale(
            pygame.image.load(assets("player.png")), (self.TILE_SIZE, self.TILE_SIZE)
        ).convert_alpha()
        self.enemy_img = pygame.transform.scale(
            pygame.image.load(assets("enemy.png")), (self.TILE_SIZE, self.TILE_SIZE)
        ).convert_alpha()

        self.enemy_projectile_img = pygame.transform.scale(
            pygame.image.load(assets("enemy projectile.png")),
            (self.TILE_SIZE, self.TILE_SIZE),
        ).convert_alpha()

        self.coin_img = pygame.transform.scale(
            pygame.image.load(assets("coin.png")), (self.TILE_SIZE, self.TILE_SIZE)
        ).convert_alpha()

        self.lava_img = pygame.transform.scale(
            pygame.image.load(assets("lava.png")),
            (self.TILE_SIZE, self.TILE_SIZE // 2),  # divive by 2 because its lava
        ).convert_alpha()

        self.flag_img = pygame.transform.scale(
            pygame.image.load(assets("flag.png")), (self.TILE_SIZE, self.TILE_SIZE)
        ).convert_alpha()

        self.star_img = pygame.transform.scale(
            pygame.image.load(assets("star.png")), (self.TILE_SIZE, self.TILE_SIZE)
        ).convert_alpha()

        # loading world
        self.world = World(self.world_data[self.level - 1], self.TILE_SIZE, self)

        # loading classes and more
        self.player = Player(
            self.world.player_x, self.world.player_y, self.player_img, 1.15, 3
        )
        # self.entity = Entity(200, HEIGHT // 10, self.player_img, 1, 300, 6, 2)
        self.enemy_attack = False
        self.current_fps = 60

        self.coins_handler = HandleCoins()
        self.coins = self.coins_handler.coins

        self.start_button_img = pygame.transform.scale(
            pygame.image.load(assets("start button.png")), (100, 50)
        ).convert_alpha()

        self.refresh_button_img = pygame.transform.scale(
            pygame.image.load(assets("refresh button.png")), (50, 50)
        )

        self.start_button = Button(WIDTH // 2, HEIGHT // 2, self.start_button_img)
        self.refresh_button = Button(0, HEIGHT - 100, self.refresh_button_img)

    def play(self) -> None:
        threading.Thread(
            target=timer_clock, args=(2, self, "GAME.enemy_attack = True")
        ).start()
        while self.run:
            self.app.fill(self.BG_COLOR)
            if self.start_button.clicked_once:
                for tile in self.world.tile_data:
                    if type(tile) is Tile:
                        tile.update(self.app)

                self.player.update(self.app, self.world, self.dt)
                # self.entity.update(self.app, self.world, self.dt)
                if len(self.world.enemy_data) > 0:
                    for enemy in self.world.enemy_data:
                        enemy.update(self.app, self.world, self.dt)

                        enemy.attack(
                            self.app,
                            self.world,
                            self.player.rect,
                            1,
                            self.enemy_attack,
                            self,
                            self.player.bullet_list,
                        )
                        if enemy.collide_player is True:
                            self.player.health -= 1
                            self.world.enemy_data.remove(enemy)
                        elif enemy.collide_projectile is True:
                            self.player.health -= 1  # projectile deletion is auto

                if len(self.world.lava_data) > 0:
                    for lava in self.world.lava_data:
                        lava.update(self.app, self.player.rect)
                        if lava.touched is True:
                            self.player.death = True

                if len(self.world.coin_data) > 0:
                    for coin in self.world.coin_data:
                        coin.update(self.app, self.player.rect)
                        if coin.touched is True:
                            self.coins += 1
                            self.world.coin_data.remove(coin)

                if len(self.world.star_data) > 0:
                    for star in self.world.star_data:
                        star.update(self.app, self.player.rect)

                        if star.catched is True:
                            self.stars += 1
                            self.world.star_data.remove(star)

                if len(self.world.flag_data) > 0 and self.stars >= 3:
                    for flag in self.world.flag_data:
                        flag.update(
                            self.app,
                            self.player.rect,
                        )

                if len(self.world.entity_data):
                    for entity in self.world.entity_data:
                        entity.update(self.app, self.world, self.dt)

                if self.player.death is True:
                    self.world.__init__(
                        self.world_data[self.level - 1], self.TILE_SIZE, self
                    )

                    self.player.rect.x = self.world.player_x
                    self.player.rect.y = self.world.player_y
                    self.player.velocity.x = 0
                    self.player.velocity.y = 0
                    self.stars = 0
                    self.player.health = 3
                    self.player.death = False

                self.refresh_button.update(self.app, "left", pygame.mouse.get_pos())

                self.reload_shoot_render = FONT.render(
                    f"{self.player.reload}/{self.player.reload_time}",
                    ANTI_ALIASING,
                    WHITE,
                )
                self.app.blit(self.reload_shoot_render, (200, 70))
                self.coins_txt_render = FONT.render(
                    f"coins: {self.coins}", ANTI_ALIASING, WHITE
                )
                self.app.blit(self.coins_txt_render, (300, 70))

                if self.player.death is True:
                    death_message = GIANT_FONT.render(
                        "u ded", ANTI_ALIASING, (255, 255, 255)
                    )
                    self.app.blit(death_message, (WIDTH // 2, HEIGHT // 2))
                if self.level == len(self.world_data):
                    win_render_line1 = MIDIUM_FONT.render(
                        "Congratulations you are",
                        ANTI_ALIASING,
                        (255, 0, 0),
                    )

                    win_render_line2 = MIDIUM_FONT.render(
                        "in your dimention",
                        ANTI_ALIASING,
                        (255, 0, 0),
                    )

                    self.app.blit(win_render_line1, ((WIDTH // 2) - 200, HEIGHT // 2))
                    self.app.blit(
                        win_render_line2, ((WIDTH // 2) - 200, (HEIGHT // 2) + 70)
                    )
            else:
                self.start_button.update(self.app, "left", pygame.mouse.get_pos())

            self.current_fps = round(self.clock.get_fps(), 2)
            self.fps_text = FONT.render(f"FPS {self.current_fps}", ANTI_ALIASING, WHITE)
            self.app.blit(self.fps_text, (70, 70))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    self.coins_handler.write_new(self.coins)
                    stop_executing()
            self.clock.tick(FPS)
            pygame.display.flip()
            if len(self.world.enemy_data) > 0:
                for enemy in self.world.enemy_data:
                    if enemy.out_of_lives:
                        self.world.enemy_data.remove(enemy)

            if self.refresh_button.clicked is True:
                self.world.__init__(
                    self.world_data[self.level - 1], self.TILE_SIZE, self
                )

                self.player.rect.x = self.world.player_x
                self.player.rect.y = self.world.player_y
                self.player.velocity.x = 0
                self.player.velocity.y = 0
                self.stars = 0
                self.player.health = 3
                self.player.death = False

    def next_level(self):
        self.level += 1
        self.level = self.level % (len(self.world_data) + 1)
        self.world = World(self.world_data[self.level - 1], self.TILE_SIZE, self)
        self.player.rect.x = self.world.player_x
        self.player.rect.y = self.world.player_y
        self.player.velocity.y = 0
        self.player.velocity.x = 0
        self.stars = 0


if __name__ == "__main__":
    game = Game()
    game.play()
