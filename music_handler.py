from itertools import cycle
from collections import OrderedDict

import pygame as pg

import tools, prepare
from radio import Radio


class MusicHandler(object):
    def __init__(self, songs_list):
        self.base_volumes = OrderedDict(songs_list)
        self.playlist = cycle(self.base_volumes.keys())
        self.current_song = next(self.playlist)
        self.volume = 1.0
        self.controls = {
                pg.K_s: self.stop,
                pg.K_SPACE: self.play,
                pg.K_p: self.pause,
                pg.K_RIGHT: self.next_song,
                pg.K_UP: self.volume_up,
                pg.K_DOWN: self.volume_down}
        self.paused = False
        self.next_song()

    def stop(self):
        pg.mixer.music.stop()

    def play(self, pos=0):
        if self.paused:
            pg.mixer.music.unpause()
        else:
            if pos:
                pg.mixer.music.play(1, pos)

    def pause(self):
        pg.mixer.music.pause()

    def next_song(self):
        self.current_song = next(self.playlist)
        pg.mixer.music.load(prepare.MUSIC[self.current_song])
        self.set_volume()
        if not self.paused:
            pg.mixer.music.play()

    def volume_up(self, amount=.05):
        self.volume += amount
        if self.volume > 1.0:
            self.volume = 1.0
        self.set_volume()

    def volume_down(self, amount=.05):
        self.volume -= amount
        if self.volume < 0:
            self.volume = 0
        self.set_volume()

    def set_volume(self):
        volume = self.volume * self.base_volumes[self.current_song]
        pg.mixer.music.set_volume(volume)

    def load(self, song):
        pg.mixer.music.load(song)

    def set_pos(self, pos):
        pg.mixer.music.set_pos(pos)

    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key in self.controls:
                self.controls[event.key]()
