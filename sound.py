import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'

        # Učitaj sve zvukove
        self.shotgun = self.load_sound('shotgun.wav')
        self.npc_pain = self.load_sound('npc_pain.wav')
        self.npc_death = self.load_sound('npc_death.wav')
        self.npc_attack = self.load_sound('npc_attack.wav', volume=0.2)
        self.player_pain = self.load_sound('player_pain.wav')
        self.theme = self.load_sound('theme.mp3', volume=0.4)
    

    def load_sound(self, filename, volume=1.0):
        try:
            sound = pg.mixer.Sound(self.path + filename)
            sound.set_volume(volume)
            return sound
        except FileNotFoundError:
            print(f"[WARNING] Sound file not found: {filename}")
            return None
