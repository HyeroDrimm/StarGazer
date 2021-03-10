import os
import pygame as pg

star_speed = 0.05
star_number = 50

window_name = "StarGazer"

gravity = 0.7
fall_grav_multiplier = 2.5
low_jump_multiplier = 3
player_jump_force = 23

horz_acc = 0.7
player_friction = -0.03

curr_dir = ""

controls_scheme = [[pg.K_a, pg.K_w, pg.K_d], [pg.K_LEFT, pg.K_UP, pg.K_RIGHT], [pg.K_j, pg.K_i, pg.K_l], [pg.K_KP4, pg.K_KP8, pg.K_KP6]]
player_color_scheme = [(200, 200, 0), (200, 0, 0), (0, 200, 0), (0, 0, 200)]

points_count_position = [(384, 80), (768, 80), (1152, 80), (1536, 80)]

choose_tile_scale_factor = 2

def set_dir():
    return os.path.dirname(__file__)
