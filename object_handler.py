from sprite_object import *
from npc import spawn_npcs_by_level
from random import randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_positions = set()

        # Spawn mobova prema trenutnom levelu
        self.spawn_npc()

        # Dodavanje static i dinamic sprite-ova
        self.add_default_sprites()

    def add_default_sprites(self):
        add_sprite = self.add_sprite
        anim_path = 'resources/sprites/animated_sprites/'

        # Dodavanje static i dinamic sprite-ova
        add_sprite(AnimatedSprite(self.game))
        add_sprite(AnimatedSprite(self.game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(self.game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(self.game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(self.game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(self.game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(self.game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(self.game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(self.game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(self.game, path=anim_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(self.game, path=anim_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(self.game, path=anim_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(self.game, path=anim_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(self.game, path=anim_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(self.game, path=anim_path + 'red_light/0.png', pos=(9.5, 20.5)))

    def spawn_npc(self):
        """Spawna NPC-e ovisno o levelu i osigurava da nisu na zidovima."""
        level = getattr(self.game, "current_level", 1)
        self.npc_list = spawn_npcs_by_level(self.game, level)

        # Filtriraj spawn tako da se mob ne spawn-a na zidu
        self.npc_positions = {
            npc.map_pos for npc in self.npc_list if npc.map_pos not in self.game.map.world_map
        }

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list}
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
