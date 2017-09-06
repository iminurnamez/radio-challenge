from collections import OrderedDict

import pygame as pg

import prepare
from potentiometer import Potentiometer
from tuner import Tuner


class RadioStation(object):
    def __init__(self, playlist, frequency):
        self.song_times = OrderedDict()
        timestamp = 0
        for p in playlist:
            sound = pg.mixer.Sound(prepare.MUSIC[p])
            self.song_times[timestamp] = prepare.MUSIC[p]
            length = sound.get_length()
            timestamp += length
        self.total_time = timestamp
        self.playlist = playlist
        self.pos = 0.0
        self.last_time = pg.time.get_ticks()
        self.frequency = frequency

    def update(self, dt):
        self.pos += dt/1000.
        self.pos = self.pos % self.total_time

    def set_pos(self):
        for timestamp, song in self.song_times.items():
            if self.pos >= timestamp:
                current_song = self.song_times[timestamp]
                stamp = timestamp
        current_pos = self.pos - stamp
        return current_song, current_pos


class Radio(object):
    static = prepare.SFX["static"]
    sweet_spot = .5
    station_range = 3.0
    bg_image = prepare.GFX["radio-bg"]

    def __init__(self, topleft, music_handler, playlists, frequencies):
        self.rect = self.bg_image.get_rect(topleft=topleft)
        self.handler = music_handler
        self.stations = OrderedDict()
        for p, f in zip(playlists, frequencies):
            s = RadioStation(p, f)
            self.stations[f] = s
        self.tuner_frequency = 1
        self.current_station = self.stations[frequencies[0]]
        self.static_volume = 0.
        self.tuner = Tuner((self.rect.left + 128, self.rect.top + 20), frequencies)
        r = self.tuner.rect
        self.volume_knob = Potentiometer((r.left - 50, r.centery + 50))

    def get_event(self, event):
        self.volume_knob.get_event(event)
        self.tuner.get_event(event)

    def update(self, dt, mouse_pos):
        self.volume_knob.update(mouse_pos)
        self.tuner.update(mouse_pos)
        self.get_signal_strength()
        self.handler.volume = self.volume_knob.output
        self.handler.set_volume()
        for freq in self.stations:
            self.stations[freq].update(dt)

    def get_signal_strength(self):
        f = self.tuner.frequency
        low = None
        high = None
        for freq in self.stations.keys():
            if f >= freq:
                if low is None:
                    low = (freq, f - freq)
                elif f - freq < low[1]:
                    low = (freq, f - freq)
            elif f <= freq:
                if high is None:
                    high = (freq, freq - f)
                elif freq - f < high[1]:
                    high = (freq, freq - f)
            if low is not None and high is not None:
                if low[1] <= high[1]:
                    self.set_static_volume(*low)
                else:
                    self.set_static_volume(*high)
                
    def set_static_volume(self, current_station, freq_distance):
        f = self.tuner_frequency
        if self.stations[current_station] != self.current_station:
            self.current_station = self.stations[current_station]
            song, pos = self.current_station.set_pos()
            self.handler.load(song)
            self.handler.play(pos)
        if freq_distance <= self.sweet_spot:
            self.static_volume = 0.
        elif freq_distance <= self.station_range:
            self.static_volume = min(1.0, (freq_distance - self.sweet_spot) / float(self.station_range))
        elif freq_distance > self.station_range:
            self.static_volume = 1.0
        self.static.set_volume(self.static_volume * self.handler.volume)
        if self.static_volume:
            self.static.play(-1)
        else:
            self.static.stop()

    def draw(self, surface):
        surface.blit(self.bg_image, self.rect)
        self.volume_knob.draw(surface)
        self.tuner.draw(surface)