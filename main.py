import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

#    Napraviti projektni plan i GDD (engl. game design document) +
#    Izgraditi i dizajnirati grafičke elemente igre u Cyber Hack stilu +
#    Implementirati RayTracing algoritam za renderiranje svjetlosnih efekata +
#    Implementirati interaktivne elemente i zagonetke povezane s tematikom igre - dodati 3 levela
#    zagonetke (tojanac dropa ljuč za vrata za 2. level gdje su wormovi itd.)
#    Razviti gameplay mehanike pucačine u prvom licu - dodati reload, materijale koje mob-ovi dropaju i stol na kojem se od njih gradi municija
#    Dodati različite vrste oružja i neprijatelja
#    Izraditi dokumentaciju projekta
#    Ideje:
#    - Igra je smještena u računalu, gdje igrač mora očistiti sustav od zlonamjernog softvera
#    - Igrač je antivirusni program koji se bori protiv zlonamjernih softverskih entiteta (virusa [trojanac, worm, malware])
#    - Igrač koristi različite vrste antivirusnih alata (oružja) za borbu protiv zlonamjernog softvera
#    - Biti će to labirint koji igrač prolazi kako bi došao do kraja igre (3 levela [trojanac, worm, malware])
#    - na kraju igrač dolazi do matične ploče i brani je od malware-a (final boss-a)


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.is_paused = False
        self.new_game()
        self.running = True

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        if not self.is_paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()

            if self.player.is_dead:
                self.handle_player_death()
                return

            pg.display.flip()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')
        else:
            pg.display.flip()
            self.clock.tick(FPS)

    def draw(self):
        if not self.is_paused:
            self.object_renderer.draw()
            self.weapon.draw()

    def handle_player_death(self):
        self.is_paused = True
        pg.mixer.music.stop()
        pg.mouse.set_visible(True)

        font = pg.font.SysFont("Consolas", 40)
        text = font.render("YOU DIED – Returning to Menu...", True, (255, 0, 0))
        rect = text.get_rect(center=(RES[0] // 2, RES[1] // 2))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, rect)
        pg.display.flip()
        pg.time.delay(2000)

        self.running = False  

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_paused = not self.is_paused
                    if self.is_paused:
                        pg.mixer.music.pause()
                        pg.mouse.set_visible(True)
                        main_menu_instance = MainMenu(self.screen)
                        main_menu_instance.run()
                        if main_menu_instance.selected_option_action == "quit":
                            pg.quit()
                            sys.exit()
                        else:
                            self.is_paused = False
                            pg.mixer.music.unpause()
                            pg.mouse.set_visible(False)

            elif event.type == self.global_event:
                self.global_trigger = True

            if not self.is_paused:
                self.player.single_fire_event(event)

    def run(self):
        self.running = True 
        while True:
            self.check_events()
            self.update()
            self.draw()


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Consolas", 50)
        self.options = ["Start Game", "Settings", "Credits", "Quit"]
        self.selected = 0
        self.running = True
        self.selected_option_action = None

    def draw(self):
        self.screen.fill((10, 10, 10))
        for i, option in enumerate(self.options):
            color = (0, 255, 180) if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(RES[0] // 2, 200 + i * 80))
            self.screen.blit(text, rect)
        pg.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.selected_option_action = "quit"
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pg.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pg.K_RETURN:
                        if self.options[self.selected] == "Start Game":
                            self.running = False
                            self.selected_option_action = "start_game"
                        elif self.options[self.selected] == "Quit":
                            self.running = False
                            self.selected_option_action = "quit"
                            pg.quit()
                            sys.exit()
                        elif self.options[self.selected] == "Credits":
                            self.show_credits()
                        elif self.options[self.selected] == "Settings":
                            self.show_settings()
                    elif event.key == pg.K_ESCAPE:
                        self.running = False
                        self.selected_option_action = "start_game"

            self.draw()

    def show_credits(self):
        self.screen.fill((10, 10, 10))
        font_small = pg.font.SysFont("Consolas", 30)
        lines = ["Cyber Hack by Tin", "", "Made with Python + Pygame", "", "Press ESC to go back"]
        for i, line in enumerate(lines):
            text = font_small.render(line, True, (0, 255, 180))
            rect = text.get_rect(center=(RES[0] // 2, 200 + i * 40))
            self.screen.blit(text, rect)
        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

    def show_settings(self):
        self.screen.fill((10, 10, 10))
        font_small = pg.font.SysFont("Consolas", 30)
        lines = ["Settings coming soon...", "", "Press ESC to go back"]
        for i, line in enumerate(lines):
            text = font_small.render(line, True, (0, 255, 180))
            rect = text.get_rect(center=(RES[0] // 2, 250 + i * 40))
            self.screen.blit(text, rect)
        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode(RES)

    while True:
        menu = MainMenu(screen)
        menu.run()

        if menu.selected_option_action == "start_game":
            game = Game()
            game.run()
        elif menu.selected_option_action == "quit":
            pg.quit()
            sys.exit()