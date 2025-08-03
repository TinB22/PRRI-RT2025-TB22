from sprite_object import *
from collections import deque
import pygame as pg

class Weapon(AnimatedSprite):
    def __init__(self, game, weapon_data):
        # weapon_data dofuravamo iz Game.new_game() ovisno o levelu
        path = weapon_data["path"]
        scale = weapon_data["scale"]
        animation_time = weapon_data["animation_time"]

        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque([
            pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images
        ])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2,
                           HEIGHT - self.images[0].get_height())

        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0

        # parametri oružja
        self.damage = weapon_data["damage"]
        self.reload_time = weapon_data["reload_time"]  # i kolko reload traje u frameovima

        self.shot_delay = weapon_data["shot_delay"]
        self.last_shot_time = 0

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter >= self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def reload(self):
        if not self.reloading:
            self.reloading = True
            self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
