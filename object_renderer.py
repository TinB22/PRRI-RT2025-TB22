import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()

        # Učitaj pod i nebo
        self.floor_texture = self.get_texture('resources/textures/floor_prri.png', (WIDTH, HALF_HEIGHT))
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.floor_offset = 0

        # Efekti
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)

        # Health display
        self.digit_size = 80
        self.health_display_y_offset = 20
        self.health_display_x_start = 20
        self.digit_images = [
            self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
            for i in range(10)
        ]
        self.digits = dict(zip(map(str, range(10)), self.digit_images))

        # Slike za win/lose
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health_str = str(self.game.player.health)
        for i, char in enumerate(health_str):
            if char in self.digits:
                self.screen.blit(
                    self.digits[char],
                    (self.health_display_x_start + i * self.digit_size, self.health_display_y_offset)
                )
    
    def draw_ammo(self):
        font = pg.font.SysFont("Consolas", 30)
        text = font.render(f"Ammo: {self.weapon.ammo}/{self.weapon.max_ammo}", True, (255, 255, 0))
        self.screen.blit(text, (20, HEIGHT - 50))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        # nebo se pomiče s micanjem miša
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        # pod statičan (jednostavna slika/tekstura)
        self.screen.blit(self.floor_texture, (0, HALF_HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        try:
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res)
        except FileNotFoundError:
            print(f"[WARNING] Texture not found: {path}")
            return pg.Surface(res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/wall_prri.png'),
            2: self.get_texture('resources/textures/wall_prri-modified.png'),
            3: self.get_texture('resources/textures/wall_prri.png'),
            4: self.get_texture('resources/textures/firewall_prri.png'),
            5: self.get_texture('resources/textures/motherboard_prri.png'),
        }
