from sprite_object import *
from collections import deque
import pygame as pg
import os

class Weapon(AnimatedSprite):
    def __init__(self, game, weapon_data):
        self.game = game
        self.weapon_data = weapon_data

        # Infinite ammo postavka
        self.infinite_ammo = weapon_data.get("infinite_ammo", False)
        if self.infinite_ammo:
            self.max_ammo = float("inf")
            self.ammo = float("inf")
        else:
            self.max_ammo = 6
            self.ammo = self.max_ammo

        path = weapon_data["path"]
        scale = weapon_data["scale"]

        super().__init__(game=game, path=path, scale=scale, animation_time=weapon_data["shoot_anim_time"])

        self.images = deque([
            pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images
        ])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2,
                           HEIGHT - self.images[0].get_height())

        # Učitavanje animacija
        self.shoot_images = self.load_images_from_folder(weapon_data["shoot_folder"], scale)
        if weapon_data.get("reload_folder"):
            self.reload_images = self.load_images_from_folder(weapon_data["reload_folder"], scale)
        else:
            self.reload_images = []

        self.state = "idle"
        self.frame_counter = 0
        self.damage = weapon_data["damage"]

        self.shoot_anim_time = weapon_data["shoot_anim_time"]
        self.reload_anim_time = weapon_data["reload_anim_time"]
        self.shot_delay = weapon_data["shot_delay"]
        self.reload_time = weapon_data["reload_time"]
        self.last_shot_time = 0
        self.last_reload_time = 0

    def load_images_from_folder(self, folder, scale):
        images = []
        if folder and os.path.exists(folder):
            for file in sorted(os.listdir(folder)):
                if file.endswith(".png"):
                    img = pg.image.load(os.path.join(folder, file)).convert_alpha()
                    img = pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
                    images.append(img)
        return images

    def start_shoot(self):
        now = pg.time.get_ticks()
        if self.state == "idle" and (self.infinite_ammo or self.ammo > 0) and (now - self.last_shot_time >= self.shot_delay):
            self.state = "shooting"
            self.frame_counter = 0
            self.game.player.shot = True
            self.last_shot_time = now
            if not self.infinite_ammo:
                self.ammo -= 1
            if self.game.sound.shotgun:
                self.game.sound.shotgun.play()

    def reload(self):
        if self.infinite_ammo:
            return
        now = pg.time.get_ticks()
        if self.state == "idle" and (now - self.last_reload_time >= self.reload_time):
            self.state = "reloading"
            self.frame_counter = 0
            self.last_reload_time = now

    def animate(self):
        if self.state == "shooting":
            if self.animation_trigger and self.frame_counter < len(self.shoot_images):
                self.image = self.shoot_images[self.frame_counter]
                self.frame_counter += 1
            elif self.frame_counter >= len(self.shoot_images):
                self.state = "idle"
                self.frame_counter = 0
                self.image = self.images[0]
                self.game.player.shot = False

        elif self.state == "reloading":
            if self.animation_trigger and self.frame_counter < len(self.reload_images):
                self.image = self.reload_images[self.frame_counter]
                self.frame_counter += 1
            elif self.frame_counter >= len(self.reload_images):
                self.state = "idle"
                self.frame_counter = 0
                self.image = self.images[0]
                self.ammo = self.max_ammo

    def draw(self):
        self.game.screen.blit(self.image, self.weapon_pos)

    def update(self):
        if self.state == "shooting":
            self.check_animation_time(custom_time=self.shoot_anim_time)
        elif self.state == "reloading":
            self.check_animation_time(custom_time=self.reload_anim_time)
        else:
            self.check_animation_time()

        self.animate()