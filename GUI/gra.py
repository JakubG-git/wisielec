from curses import KEY_ENTER
from importlib.resources import path
from pickle import FALSE
import pygame as pg
import string
from pygame.locals import *
from random import random as rd
from random import randint as ri
import os
pg.init()           
pg.display.set_caption("Wisielec")
FRAMES_PER_SECOND = 60
WIDTH, HEIGHT = 600, 600
FONT = pg.font.SysFont("Arial", 30)
DISPLAY = pg.display.set_mode((WIDTH, HEIGHT))
CLOCK = pg.time.Clock()
CLICK = False
MENU_BUTTONS_PNG = pg.image.load(os.path.join("imgs", "blue_button00.png"))


MENU_TEXT = ["1.Nowa gra",
        "2.Zapisz gre",
        "3.Wczytaj gre",
        "4.Statystyki",
        "5.Wyjdz"]



class Obiekt:
    def __init__(self, slowo = "", zycie = 1, pudla = [], trafienia = []):
        self.slowo = slowo
        self.zycie = zycie
        self.pudla = pudla
        self.trafienia = trafienia
        self.alfabet = string.ascii_lowercase # tu wybieramy alfabet
    def save(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.slowo + '\n')
            f.write(str(self.zycie) + '\n')
            f.write(str(self.pudla) + '\n')
            f.write(str(self.trafienia) + '\n')
            f.close()
    def load(self, file_name):
        with open(file_name, 'r') as f:
            self.slowo = f.readline()[:-1]
            self.zycie = int(f.readline()[:-1])
            self.pudla = [i for i in f.readline()[:-1] if i in self.alfabet]
            self.trafienia = [i for i in f.readline()[:-1] if i in self.alfabet]
            f.close()
    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.slowo, self.zycie, self.pudla, self.trafienia) # debbuging

class Gra:
    def __init__(self, slowo = "Gra"):
        self.obiekt = Obiekt(slowo)
        self.wczytana_gra = False
        self.wygrana = False
        self.przegrana = False
    def __init__(self, Obiekt = Obiekt()):
        self.obiekt = Obiekt
        self.wczytana_gra = False
        self.wygrana = False
        self.przegrana = False

    def draw_text(self, text, font, color, x, y):
        textsurface = font.render(text, True, color)
        textrect = textsurface.get_rect()
        textrect.center = (x, y)
        DISPLAY.blit(textsurface, textrect)

    def save(self, n = 0):
        self.obiekt.save(f"save{n}.txt")
    
    def load(self, n = 0):
        self.obiekt.load(f"save{n}.txt")
        self.wczytana_gra = True
    
    def random_word(self) -> str:
        with open("polski.txt", 'r') as f:
            slowa = f.readlines()
            f.close()
        return slowa[int(len(slowa) * (rd()))][:-1]

    def stats(self):
        DISPLAY.fill((0,0,0))
        self.draw_text(f"Życia: {self.obiekt.zycie}", FONT, (0,128,0), WIDTH/2, HEIGHT/2)
        self.draw_text(f"Pudła: {self.obiekt.pudla}", FONT, (0,128,0), WIDTH/2, HEIGHT/2 + 30)
        self.draw_text(f"Trafienia: {self.obiekt.trafienia}", FONT, (0,128,0), WIDTH/2, HEIGHT/2 + 60)
        pg.display.update()
        pg.time.wait(1000)
    
    def menu(self):
        CLICK = False
        menu_options = list()
        for i in range(5):
            menu_options.append(pg.Rect(WIDTH/2 - 200/2, HEIGHT/3 - 30/2+ i * 60, 200, 35))
        menu_running = True
        while menu_running:
            DISPLAY.fill((0,0,0))
            self.draw_text("Witaj w grze Wisielec!", FONT, (255,255,255), WIDTH/2, 30)
            mouse_x, mouse_y = pg.mouse.get_pos()
            for index, option in enumerate(menu_options):
                if option.collidepoint((mouse_x, mouse_y)):
                    if CLICK:
                        self.select(index)

            for index, option in enumerate(menu_options):
                DISPLAY.blit(MENU_BUTTONS_PNG, (option.x, option.y))
                self.draw_text(MENU_TEXT[index], FONT, (0, 0, 0),WIDTH/2, HEIGHT/3 + index * 60  )
            CLICK = False
            for event in pg.event.get():
                if event.type == QUIT:
                    menu_running = False
                    pg.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu_running = False
                        pg.quit()
                        exit()
                    #print(event.unicode)
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        CLICK = True
            pg.display.update()
            CLOCK.tick(FRAMES_PER_SECOND)

    def start(self):
        self.menu()

    def win_loss_check(self):
        if self.obiekt.zycie == 0:
            DISPLAY.fill((0,0,0))
            self.draw_text("Przegrana!", FONT, (0,128,0), WIDTH/2, HEIGHT/2)
            self.draw_text(self.obiekt.slowo, FONT, (255, 255, 255), WIDTH/2, HEIGHT/2 + 30)
            pg.display.update()
            pg.time.wait(1000)
            self.przegrana = True
        if len(self.obiekt.trafienia) == len(self.obiekt.slowo):
            DISPLAY.fill((0,0,0))
            self.draw_text("Wygrana!", FONT, (0,128,0), WIDTH/2, HEIGHT/2)
            pg.display.update()
            pg.time.wait(1000)
            self.wygrana = True


    def print_word(self):
        if not self.wygrana and not self.przegrana:
            odgadniente_slowo  = [literka if literka in self.obiekt.trafienia else "_" for literka in self.obiekt.slowo]
            for index, letter in enumerate(odgadniente_slowo):
                self.draw_text(f"{letter} ", FONT, (255,255,255), WIDTH/2 + 30 * index - len(odgadniente_slowo) * 13, HEIGHT/4 + HEIGHT/3)
            pg.display.update()
            pg.time.wait(100)

    def hit_n_miss(self, litera):
        if litera in self.obiekt.slowo and (litera not in self.obiekt.trafienia):
            for letter in self.obiekt.slowo:
                if litera == letter:
                    self.obiekt.trafienia.append(litera)
        elif litera not in self.obiekt.slowo:
            self.obiekt.pudla.append(litera)
            self.obiekt.zycie -= 1
        
    def new_game(self):
        if self.wygrana or self.przegrana:
            self.wygrana, self.przegrana = False, False
            self.obiekt = Obiekt("Nowa Gra")
        game_running = True
        if not self.wczytana_gra:
            self.select_word()
        DISPLAY.fill((0,0,0))
        pg.display.update()
        while (self.obiekt.zycie > 0 and (not self.wygrana) and (not self.przegrana) and game_running):
            DISPLAY.fill((0,0,0))
            self.win_loss_check()
            for event in pg.event.get():
                if event.type == QUIT:
                    game_running = False
                    pg.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.save(10 + ri(0, 90))
                        game_running = False
                    if event.key == K_KP_MINUS:
                        self.load()
                    if event.key == K_KP_PLUS:
                        self.save()
                    else:
                        self.hit_n_miss(event.unicode)
            self.win_loss_check()
            self.print_word()
            pg.display.update()
            CLOCK.tick(FRAMES_PER_SECOND)



    def quit(self):
        DISPLAY.fill((0,0,0))
        self.draw_text(f"Żegnaj", FONT, (0,128,0), WIDTH/2, HEIGHT/2)
        pg.display.update()
        pg.time.wait(1000)
        pg.quit()
        exit()

    def select(self, selection):
        if selection == 0:
            self.wczytana_gra = False
            self.new_game()
        elif selection == 1:
            self.save()
        elif selection == 2:
            self.load()
            self.wczytana_gra = True
            self.new_game()
            self.wczytana_gra = False
        elif selection == 3:
            self.stats()
        elif selection == 4:
            self.quit()

    def select_word(self):
        selected = False
        manual = False
        DISPLAY.fill((0,0,0))
        self.draw_text(f"Wybierz tryb", FONT, (0,128,0), WIDTH/2, HEIGHT/2)
        self.draw_text(f"1. Losowe słowo / 2. Własne słowo", FONT, (0,128,0), WIDTH/2, HEIGHT/2 + 30)
        pg.display.update()
        while not selected:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        selected = True
                    if event.key == K_2:
                        selected = True
                        manual = True
            CLOCK.tick(FRAMES_PER_SECOND)
        if manual:
            end = False
            while not end:
                for event in pg.event.get():
                    if event.type == QUIT:
                        end = True
                        pg.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if (event.key == K_ESCAPE or event.key == K_RETURN or event.key == K_KP_ENTER)and len(self.obiekt.slowo) > 2:
                            end = True 
                        else:  
                            self.obiekt.slowo += event.unicode
                DISPLAY.fill((0,0,0))            
                self.draw_text(f"Wybrałeś: {self.obiekt.slowo}", FONT, (0,128,0), WIDTH/2, HEIGHT/2)
                pg.display.update()
                CLOCK.tick(FRAMES_PER_SECOND)
        else:
            self.obiekt.slowo = self.random_word()
            DISPLAY.fill((0,0,0))  
            pg.display.update()
            CLOCK.tick(FRAMES_PER_SECOND)
        self.obiekt.zycie = len(self.obiekt.slowo)





if __name__ == "__main__":
    gra = Gra()
    gra.start()
