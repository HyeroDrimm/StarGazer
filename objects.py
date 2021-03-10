import pygame as pg
from settings import *
import json

vec = pg.math.Vector2


class Black_Screen(pg.sprite.DirtySprite):
    def __init__(self, size):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.layer = 3

        self.image.convert_alpha()
        self.image.fill((0, 0, 0))
        self.image.set_alpha(0)


class Player(pg.sprite.DirtySprite):
    def __init__(self, pos, color, number):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.layer = 1

        self.color = color
        self.number = number

        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.left_b = pg.K_a
        self.right_b = pg.K_d
        self.up_b = pg.K_w
        self.card_count = 0


class Platform(pg.sprite.DirtySprite):
    def __init__(self, color, pos, size, layer_num):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.layer = layer_num


class CardPickUp(pg.sprite.DirtySprite):
    def __init__(self, color, pos, layer_num, card_type):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface((70, 70))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.layer = layer_num

        self.card_type = card_type

class Counter(pg.sprite.DirtySprite):
    def __init__(self, pos, color, number, size=(41, 32)):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface((100, 100))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.layer = 2
        self.size = size

        self.value = int(number)

        texture_face = my_font.render(str(number), False, (0, 0, 0))

        self.image.blit(texture_face, size)

    def update_counter(self, number):
        self.image.fill(self.color)
        texture_face = my_font.render(str(number), False, (0, 0, 0))
        self.image.blit(texture_face, self.size)

class PlatformLevel:
    def __init__(self, level_number, number_of_players):

        plf_lvl_data_dir = os.path.join(curr_dir, "assets/platform_level_data/")
        plf_lvl_data_dir = os.path.join(plf_lvl_data_dir, str(level_number) + ".json")

        f = open(plf_lvl_data_dir, "r")
        lvl_data = json.loads(f.read())
        f.close()

        self.level_done = False

        self.counters_list = []
        self.pl = []
        for element in range(number_of_players):
            self.pl.append(Player((lvl_data["players"][element]["x_pos"], lvl_data["players"][element]["y_pos"]), player_color_scheme[element], element + 1))
            self.counters_list.append(Counter(points_count_position[element], player_color_scheme[element], 0))

        for i in range(len(self.pl)):
            self.pl[i].left_b = controls_scheme[i][0]
            self.pl[i].up_b = controls_scheme[i][1]
            self.pl[i].right_b = controls_scheme[i][2]

        self.platform_list = []
        for element in lvl_data["platform"]:
            self.platform_list.append(
                Platform(element["color"], (element["x_pos"], element["y_pos"]), (element["x_size"], element["y_size"]),
                         element["layer"]))

        self.card_list = []
        for element in lvl_data["card"]:
            self.card_list.append(
                CardPickUp(element["color"], (element["x_pos"], element["y_pos"]),
                           element["layer"], element["type"]))

        self.spr_to_up = []
        for element in self.pl:
            self.spr_to_up.append(element)

        for element in self.counters_list:
            self.spr_to_up.append(element)

        for element in self.platform_list:
            self.spr_to_up.append(element)

        for element in self.card_list:
            self.spr_to_up.append(element)

    def update_players(self):
        for i in range(len(self.pl)):
            self.pl[i].dirty = 1

            self.pl[i].acc = vec(0, gravity)

            keys = pg.key.get_pressed()
            if keys[self.pl[i].left_b]:
                self.pl[i].acc.x = -horz_acc
            if keys[self.pl[i].right_b]:
                self.pl[i].acc.x = horz_acc

            self.pl[i].acc.x += self.pl[i].vel.x * player_friction
            self.pl[i].vel.x += self.pl[i].acc.x
            self.pl[i].pos.x += self.pl[i].vel.x + 0.5 * self.pl[i].acc.x

            self.pl[i].rect.center = (self.pl[i].pos.x, self.pl[i].rect.center[1])

            hits = pg.sprite.spritecollide(self.pl[i], self.platform_list, False)
            if hits:
                if self.pl[i].vel.x > 0:
                    self.pl[i].rect.right = hits[0].rect.left
                    self.pl[i].pos = vec(self.pl[i].rect.center)
                if self.pl[i].vel.x < 0:
                    self.pl[i].rect.left = hits[0].rect.right
                    self.pl[i].pos = vec(self.pl[i].rect.center)
                self.pl[i].vel.x = 0

            if keys[self.pl[i].up_b]:
                self.pl[i].rect.bottom += 1
                hits = pg.sprite.spritecollide(self.pl[i], self.platform_list, False)
                self.pl[i].rect.bottom -= 1
                if hits:
                    self.pl[i].vel.y -= player_jump_force

            if self.pl[i].vel.y > 0:
                self.pl[i].vel.y += (fall_grav_multiplier - 1) * gravity
            elif self.pl[i].vel.y < 0 and not keys[self.pl[i].up_b]:
                self.pl[i].vel.y += (low_jump_multiplier - 1) * gravity

            self.pl[i].vel.y += self.pl[i].acc.y
            self.pl[i].pos.y += self.pl[i].vel.y + 0.5 * self.pl[i].acc.y

            self.pl[i].rect.center = (self.pl[i].rect.center[0], self.pl[i].pos.y)

            hits = pg.sprite.spritecollide(self.pl[i], self.platform_list, False)
            if hits:
                if self.pl[i].vel.y > 0:
                    self.pl[i].rect.bottom = hits[0].rect.top
                    self.pl[i].pos = vec(self.pl[i].rect.center)
                if self.pl[i].vel.y < 0:
                    self.pl[i].rect.top = hits[0].rect.bottom
                    self.pl[i].pos = vec(self.pl[i].rect.center)
                self.pl[i].vel.y = 0

            if self.pl[i].vel.y ** 2 < 0.01:
                self.pl[i].vel.y = 0
            if self.pl[i].vel.x ** 2 < 0.01:
                self.pl[i].vel.x = 0

            hits = pg.sprite.spritecollide(self.pl[i], self.card_list, False)
            if hits:
                self.pl[i].card_count += 1
                self.counters_list[i].update_counter(self.pl[i].card_count)
                self.counters_list[i].dirty = 1
                hits[0].rect.center = (10000, 100000)
                hits[0].dirty = 1
                self.card_list.remove(hits[0])
                if len(self.card_list) == 0:
                    self.level_done = True

class LevelChooser:
    def __init__(self):
        x_shift = 550
        self.player_count_tiles = [[ChoseTile((200 + x_shift, 500), 1), ChoseTile((600 + x_shift, 500), 2)], [ChoseTile((200 + x_shift, 900), 3), ChoseTile((600 + x_shift, 900), 4)]]
        self.player_count_tiles[0][0].scale_sprite(choose_tile_scale_factor)
        self.player_count_banner = VictoryBanner((950, 200), (255, 255, 255), "Ile graczy", size=(700, 200), text_position=(190, 70))

        self.map_tiles = [[ChoseTile((200 + x_shift, 500), 1), ChoseTile((600 + x_shift, 500), 2)], [ChoseTile((200 + x_shift, 900), 3), ChoseTile((600 + x_shift, 900), 4)]]
        self.map_tiles[0][0].scale_sprite(choose_tile_scale_factor)
        self.map_banner = VictoryBanner((950, 200), (255, 255, 255), "Która mapa", size=(700, 200), text_position=(150, 70))

        for i in range(len(self.map_tiles)):
            for j in range(len(self.map_tiles[i])):
                self.map_tiles[i][j].rect.center = (10000, 10000)
        self.map_banner.rect.center = (10000, 10000)

        self.chosen_x = 0
        self.chosen_y = 0

        self.player_count = 0
        self.map = 0

        self.player_count_faze = True
        self.map_faze = False

        self.spr_to_up = []
        for element in self.player_count_tiles:
            self.spr_to_up.extend(element)
        for element in self.map_tiles:
            self.spr_to_up.extend(element)
        self.spr_to_up.append(self.map_banner)
        self.spr_to_up.append(self.player_count_banner)

    def update(self, up_bool, down_bool, left_bool, right_bool, enter_bool):
        if self.player_count_faze:
            if up_bool:
                if self.chosen_y != 0:
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_y -= 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)

            elif down_bool:
                if self.chosen_y != len(self.player_count_tiles) - 1:
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_y += 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)
            elif left_bool:
                if self.chosen_x != 0:
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_x -= 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)
            elif right_bool:
                if self.chosen_x != len(self.player_count_tiles[self.chosen_y]) - 1:
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_x += 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.player_count_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)
            if enter_bool:
                self.player_count = self.player_count_tiles[self.chosen_y][self.chosen_x].value

                self.chosen_y = 0
                self.chosen_x = 0
                self.player_count_faze = False
                self.map_faze = True

                self.player_count_banner.rect.center = (10000, 10000)
                self.player_count_banner.dirty = 1
                for i in range(len(self.player_count_tiles)):
                    for j in range(len(self.player_count_tiles[i])):
                        self.player_count_tiles[i][j].rect.center = (10000, 10000)
                        self.player_count_tiles[i][j].dirty = 1

                self.map_banner.go_to_hard_pos()
                self.map_banner.dirty = 1
                for i in range(len(self.map_tiles)):
                    for j in range(len(self.map_tiles[i])):
                        self.map_tiles[i][j].dirty = 1
                        self.map_tiles[i][j].go_to_hard_pos()

        elif self.map_faze:
            if up_bool:
                if self.chosen_y != 0:
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_y -= 1
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)

            elif down_bool:
                if self.chosen_y != len(self.map_tiles) - 1:
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_y += 1
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)
            elif left_bool:
                if self.chosen_x != 0:
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_x -= 1
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)
            elif right_bool:
                if self.chosen_x != len(self.map_tiles[self.chosen_y]) - 1:
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(1 / choose_tile_scale_factor)

                    self.chosen_x += 1
                    self.map_tiles[self.chosen_y][self.chosen_x].dirty = 1
                    self.map_tiles[self.chosen_y][self.chosen_x].scale_sprite(choose_tile_scale_factor)
            if enter_bool:
                self.map = self.map_tiles[self.chosen_y][self.chosen_x].value


pg.font.init()
my_font = pg.font.SysFont('RocknRoll One', 60)

class ChoseTile(pg.sprite.DirtySprite):
    def __init__(self, pos, text, size=(100, 100), text_position=(40, 30)):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.layer = 1

        self.hard_pos = pos
        self.value = int(text)

        texture_face = my_font.render(str(text), False, (0, 0, 0))

        self.image.blit(texture_face, text_position)

    def scale_sprite(self, scale):
        self.image = pg.transform.scale(self.image, (int(self.image.get_height() * scale), int(self.image.get_width() * scale)))
        prev_pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = prev_pos

    def go_to_hard_pos(self):
        self.rect.center = self.hard_pos


my_font2 = pg.font.SysFont('RocknRoll One', 100)

class VictoryBanner(pg.sprite.DirtySprite):
    def __init__(self, pos, color, text, size=(800, 500), text_position=(150, 210)):
        pg.sprite.DirtySprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hard_pos = pos
        self.layer = 1

        texture_face = my_font2.render(str(text), False, (0, 0, 0))

        self.image.blit(texture_face, text_position)

    def go_to_hard_pos(self):
        self.rect.center = self.hard_pos
