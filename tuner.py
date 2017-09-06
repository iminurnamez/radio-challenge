import pygame as pg

from potentiometer import Potentiometer

import prepare


class Tuner(object):
    tuner_img = prepare.GFX["tuner"]
    stick_img = prepare.GFX["tuner-stick"]
    frequency_range = 87.9, 107.9
    def __init__(self, topleft, station_frequencies):
        self.frequencies = station_frequencies
        self.low = self.frequencies[0]
        self.high = self.frequencies[-1]
        self.rect = self.tuner_img.get_rect(topleft=topleft)
        self.stick_rect = self.stick_img.get_rect(topleft=self.rect.topleft)
        self.knob = Potentiometer((self.rect.right + 50, self.rect.centery + 50))
        self.margin = 32
        
    def get_event(self, event):
        self.knob.get_event(event)
        
    def update(self, mouse_pos):
        self.knob.update(mouse_pos)
        low, high = self.low, self.high
        self.frequency = low + ((high - low) * self.knob.output)
        scale = (self.frequency - low) / (high - low)
        self.stick_rect.centerx = self.rect.left + (self.margin // 2) + ((self.rect.w - self.margin)* scale)
        
    def draw(self, surface):
        surface.blit(self.tuner_img, self.rect)
        surface.blit(self.stick_img, self.stick_rect)
        self.knob.draw(surface)