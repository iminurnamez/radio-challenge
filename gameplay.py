import pygame as pg

import tools, prepare
from labels import Label
from state_engine import GameState
from music_handler import MusicHandler, Radio
from potentiometer import Potentiometer
from tuner import Tuner


songs = [("buckin_the_dice", 1.0),
             ("christmas-eve-at-midnight", 1.0),
             ("puzzle-1-a", 1.0),
             ("betcha_nickel", 1.0),
             ("ace_in_the_hole", 1.0),
             ("Lights", 1.0),
             ("Ultraspeed", 1.0)
             ]
playlists = [
        ["buckin_the_dice", "betcha_nickel", "ace_in_the_hole"],
        ["christmas-eve-at-midnight", "puzzle-1-a"],
        ["Lights", "Ultraspeed"],
        ["crypt-Loop", "WrongRiteTheme", "WTF!Ghost!"]]
frequencies = [90.1, 94.9, 100.3, 105.7]


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.music_handler = MusicHandler(songs)
        self.radio = Radio((200, 200), self.music_handler,
                                 playlists, frequencies)
        self.make_labels(frequencies)
                                
    def make_labels(self, frequencies):
        self.labels = pg.sprite.Group()
        names = ["WOLD", "WMLW", "WEDM", "WTCH"]
        cx, top = prepare.SCREEN_RECT.centerx, 20
        for name, num in zip(names, frequencies):
            Label("{} {}".format(name, num), {"midtop": (cx, top)}, self.labels,
                    font_size=24, text_color="antiquewhite", 
                    font_path=prepare.FONTS["weblysleekuisl"])
            top += 30
            
    def startup(self, persitent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.music_handler.get_event(event)
        self.radio.get_event(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.radio.update(dt, mouse_pos)
        
    def draw(self, surface):
        self.radio.draw(surface)
        self.labels.draw(surface)