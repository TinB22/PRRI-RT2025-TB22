from sprite_object import *
from random import randint, random, choice
import math

class NPC(AnimatedSprite):
    def __init__(self, game, path, pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180,
                 health=100, attack_damage=10, speed=0.03, accuracy=0.15):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # animacije
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        # statistike NPC-a
        self.attack_dist = randint(3, 6)
        self.speed = speed
        self.size = 20
        self.health = health
        self.attack_damage = attack_damage
        self.accuracy = accuracy

        # status
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:  # napad samo kad je frame animacije
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        if not self.alive and self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
            self.death_images.rotate(-1)
            self.image = self.death_images[0]
            self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health <= 0:
            self.alive = False
            self.game.sound.npc_death.play()
            
            # ako je ubijen zadnji torjan mob ili worm mob, spawnaj kljuc
            if isinstance(self, Trojan):
                alive_trojans = [npc for npc in self.game.object_handler.npc_list if isinstance(npc, Trojan) and npc.alive]
                if len(alive_trojans) == 0:
                    self.game.object_handler.spawn_key(self.map_pos)

            elif isinstance(self, Worm) and self.game.current_level == 2:
                alive_worms = [npc for npc in self.game.object_handler.npc_list if isinstance(npc, Worm) and npc.alive]
                if len(alive_worms) == 0:
                    self.game.object_handler.spawn_key(self.map_pos)
                    
            elif isinstance(self, MalwareBoss) and self.game.current_level == 3:
                self.game.object_handler.spawn_key(self.map_pos)

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        """Provjera vidi li NPC igrača (preko raycasta)."""
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.theta
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontalni
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # vertikalni
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a
        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)
        return 0 < player_dist < wall_dist or not wall_dist


# preuredene klase za NPC-e
class Trojan(NPC):
    def __init__(self, game, pos):
        super().__init__(game,
                         path='resources/sprites/npc/trojan/0.png',
                         pos=pos, health=150, attack_damage=25, speed=0.05, accuracy=0.35)
        self.attack_dist = 1.0

class Worm(NPC):
    def __init__(self, game, pos):
        super().__init__(game,
                         path='resources/sprites/npc/worm/0.png',
                         pos=pos, health=100, attack_damage=10, speed=0.04, accuracy=0.25)

class MalwareBoss(NPC):
    def __init__(self, game, pos):
        super().__init__(game,
                         path='resources/sprites/npc/malware/0.png',
                         pos=pos, health=350, attack_damage=20, speed=0.045, accuracy=0.25)

def spawn_npcs_by_level(game, level):
    npcs = []
    player_tile = (int(game.player.x), int(game.player.y))
    def is_far_enough(pos):
        dx = abs(pos[0] - player_tile[0])
        dy = abs(pos[1] - player_tile[1])
        return dx > 4 and dy > 4

    empty_positions = [
        (x, y) for x in range(1, game.map.cols-1)
        for y in range(1, game.map.rows-1)
        if (x, y) not in game.map.world_map and is_far_enough((x, y))
    ]

    if level == 1:
        for _ in range(10):
            npcs.append(Trojan(game, choice(empty_positions)))
    elif level == 2:
        for _ in range(10):
            npcs.append(Worm(game, choice(empty_positions)))
    elif level == 3:
        npcs.append(MalwareBoss(game, choice(empty_positions)))

    return npcs