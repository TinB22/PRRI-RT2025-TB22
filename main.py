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
#    Implementirati interaktivne elemente i zagonetke povezane s tematikom igre - dodati 3 levela +
#    zagonetke (tojanac dropa ljuč za vrata za 2. level gdje su wormovi itd.)
#    dodati to da plavi sprite-ovi heal-aju igrača kada im je u blizini
#    vidjeti kako dodati neki health bar (plavi u boju sprite-ova koji heal-aju)
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

        self.current_level = 1
        self.max_level = 3
        self.game_won = False

        self.running = True
        self.new_game()

    def new_game(self):
        self.map = Map(self, level=self.current_level)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        self.object_handler = ObjectHandler(self)

        if self.sound.theme:
            self.sound.theme.play(-1)

    def show_next_level_screen(self):
        font = pg.font.SysFont("Consolas", 50)
        text = font.render(f"Level {self.current_level} Complete!", True, (0, 255, 180))
        subtext = font.render("Press any key for next level...", True, (200, 200, 200))

        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(RES[0] // 2, RES[1] // 2 - 40)))
        self.screen.blit(subtext, subtext.get_rect(center=(RES[0] // 2, RES[1] // 2 + 40)))
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False

    def check_level_complete(self):
        if all(not npc.alive for npc in self.object_handler.npc_list):
            pg.time.delay(500)
            if self.current_level < self.max_level:
                self.show_next_level_screen()
                self.current_level += 1
                self.new_game()
            else:
                self.game_won = True

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                self.is_paused = not self.is_paused

            self.player.single_fire_event(event)

            if event.type == self.global_event:
                self.global_trigger = True
            else:
                self.global_trigger = False

    def update(self):
        if not self.is_paused and not self.game_won:
            self.raycasting.update()
            self.player.update()
            self.object_handler.update()
            self.weapon.update()
            self.check_level_complete()

        self.object_renderer.draw()
        self.weapon.draw()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps():.1f}")

    def draw_win_screen(self):
        font = pg.font.SysFont("Consolas", 60)
        text = font.render("YOU WON!", True, (0, 255, 180))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(RES[0] // 2, RES[1] // 2)))
        pg.display.flip()
        pg.time.delay(3000)

    def run(self):
        while self.running:
            self.check_events()
            if self.game_won:
                self.draw_win_screen()
                return
            else:
                self.update()


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Consolas", 50)
        self.options = ["Start Game", "Quit"]
        self.selected = 0
        self.running = True
        self.selected_option_action = None

    def draw(self):
        self.screen.fill((10, 10, 10))
        for i, option in enumerate(self.options):
            color = (0, 255, 180) if i == self.selected else (150, 150, 150)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(RES[0] // 2, 250 + i * 80))
            self.screen.blit(text, rect)
        pg.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pg.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pg.K_RETURN:
                        if self.options[self.selected] == "Start Game":
                            self.selected_option_action = "start"
                            self.running = False
                        elif self.options[self.selected] == "Quit":
                            pg.quit()
                            sys.exit()

            self.draw()


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode(RES)

    while True:
        menu = MainMenu(screen)
        menu.run()

        if menu.selected_option_action == "start":
            game = Game()
            game.run()
        else:
            break