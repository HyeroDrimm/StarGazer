import ctypes
import ui
from objects import *
from settings import *
from star import Constellation


class Game:
    def __init__(self):
        global curr_dir
        curr_dir = set_dir()

        ctypes.windll.user32.SetProcessDPIAware()
        self.screen_width, self.screen_height = (
            ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

        pg.init()
        self.screen = pg.display

        self.screen.set_mode((self.screen_width, self.screen_height), pg.FULLSCREEN)
        self.screen.set_caption(window_name)
        self.screen_surface = self.screen.get_surface()

        pg.mixer.music.load('assets/loop.wav')
        self.win_sound = pg.mixer.Sound('assets/win.wav')
        pg.mixer.music.play(-1)

        self.getTicksLastFrame = 0
        self.clock = pg.time.Clock()

        self.running = True
        self.deltaTime = 0

        self.fps_counter = ui.fps_counter

        self.sprites_to_update = []
        self.sprites_to_update_layers = []
        self.background = pg.Surface((self.screen_width, self.screen_height))
        self.all_sprites = pg.sprite.LayeredDirty()

        self.lvl = PlatformLevel(0, 1)
        self.lvl_chooser = LevelChooser()
        self.victory_banner = VictoryBanner((500, 500), (255, 255, 255), 'something is wrong...')
        self.constellation = Constellation(star_number, star_speed, 1920, 1080)

        self.sprites_to_update.extend(self.lvl_chooser.spr_to_up)
        self.sprites_to_update.append(self.constellation.bb)

        self.up_bool = False
        self.down_bool = False
        self.left_bool = False
        self.right_bool = False
        self.enter_bool = False
        self.choose_bool = True

        self.prepare_draw()

    def game_loop(self):
        while self.running:
            self.events()
            self.update_delta_time()
            if self.choose_bool:
                self.lvl_chooser.update(self.up_bool, self.down_bool, self.left_bool, self.right_bool, self.enter_bool)

            self.platformer_loop()
            self.constellation.update()

            if self.lvl_chooser.map:
                self.lvl = PlatformLevel(self.lvl_chooser.map, self.lvl_chooser.player_count)
                self.sprites_to_update = self.lvl.spr_to_up
                self.sprites_to_update.append(self.constellation.bb)
                self.prepare_draw()
                self.choose_bool = False
                self.lvl_chooser.map = 0
            if self.lvl.level_done:
                pg.mixer.music.fadeout(700)
                pg.mixer.Sound.play(self.win_sound)
                self.lvl.pl.sort(key=player_sort_by_points, reverse=True)

                if len(self.lvl.pl) > 1 and self.lvl.pl[0].card_count == self.lvl.pl[1].card_count:
                    self.victory_banner = VictoryBanner((950, 600), (255, 255, 255),
                                                        'Remis!!!')
                else:
                    self.victory_banner = VictoryBanner((950, 600), self.lvl.pl[0].color,
                                                    'Gracz ' + str(self.lvl.pl[0].number) + ' wygrał!!!')
                self.sprites_to_update = [self.victory_banner]
                self.sprites_to_update.append(self.constellation.bb)
                self.prepare_draw()
                self.lvl.level_done = False
            self.draw()
            self.fps_counter.clock.tick(60)
            # self.screen_surface.blit(self.fps_counter.get_fps(self.fps_counter), (10, 10))

            self.clear_variables()

        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.up_bool = True
                if event.key == pg.K_s:
                    self.down_bool = True
                if event.key == pg.K_a:
                    self.left_bool = True
                if event.key == pg.K_d:
                    self.right_bool = True
                if event.key == pg.K_RETURN:
                    self.enter_bool = True

    def prepare_draw(self):
        self.all_sprites = pg.sprite.LayeredDirty(self.sprites_to_update)
        self.screen_surface.blit(self.background, (0, 0))
        self.all_sprites.clear(self.screen, self.background)
        for element in self.sprites_to_update:
            self.all_sprites.change_layer(element, element.layer)

    def draw(self):
        for element in self.sprites_to_update_layers:
            self.all_sprites.change_layer(element, element.update_layer)
        self.all_sprites.update()
        rects = self.all_sprites.draw(self.screen_surface)
        pg.display.update(rects)

    def clean_sprite_update_list(self):
        self.sprites_to_update = []
        self.sprites_to_update_layers = []

    def platformer_loop(self):
        self.lvl.update_players()

    def update_delta_time(self):
        t = pg.time.get_ticks()
        self.deltaTime = (t - self.getTicksLastFrame) / 15
        self.getTicksLastFrame = t

    def clear_variables(self):
        self.up_bool = False
        self.down_bool = False
        self.left_bool = False
        self.right_bool = False
        self.enter_bool = False


def player_sort_by_points(x):
    return x.card_count


g = Game()
g.game_loop()
