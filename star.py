import random
import pygame as pg
from settings import *

color_table = ((255, 255, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255))

class Star:
    size = 0
    velocity = 0
    position = (0, 0)
    color = (0, 0, 0)

    def __init__(self, width, height, color, star_speed):
        self.size = random.uniform(2, 7)
        self.position = (width, height)
        self.velocity = (self.size + random.uniform(0, 1)) * star_speed
        self.color = color

    def transform_by_vector2d(self, width_change, height_change):
        self.position = (self.position[0] + width_change, self.position[1] + height_change)

class Constellation:
    star_list = []

    def __init__(self, star_number, star_speed, screen_width, screen_height):
        for i in range(0, star_number):
            self.star_list.append(Star(random.uniform(0, screen_width), random.uniform(0, screen_height), color_table[random.randint(0, len(color_table) - 1)], star_speed))
        self.bb = BlackBackground()

    def transform_by_vector2d(self, movement_vector, deltaTime, screen_width, screen_height):
        for i in self.star_list:
            i.position = (i.position[0] + i.velocity * movement_vector[0] * deltaTime,
                          i.position[1] + i.velocity * movement_vector[1] * deltaTime)

            if i.position[0] > screen_width or i.position[1] > screen_height or i.position[0] < 0 or i.position[1] < 0:
                i.position = (abs(i.position[0] - screen_width), abs(i.position[1] - screen_height))

    def update(self):
        self.bb.image.fill((0, 0, 0))
        for i in self.star_list:
            self.transform_by_vector2d((0, star_speed), 1, 1920, 1080)
            pg.draw.circle(self.bb.image, i.color, (int(i.position[0]), int(i.position[1])), int(i.size))
        self.bb.dirty = 1

class BlackBackground(pg.sprite.DirtySprite):
    def __init__(self):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface((1920, 1080))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.layer = 0

