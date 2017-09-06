from math import pi, degrees

import pygame as pg

import prepare
from angles import get_distance, get_angle


class Potentiometer(object):
    def __init__(self, pos):
        self.pos = pos
        self.grabbed = False
        self.hovered = False
        self.base_image = self.image = prepare.GFX["knob"]
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = self.last_angle = 0
        self.radius = self.rect.w // 2
        self.min_angle, self.max_angle = pi, 0
        
        self.angle = .5 * pi
        self.adjust_output()
    
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovered:
                self.grab(event.pos)
        elif event.type == pg.MOUSEBUTTONUP:
            self.grabbed = False
        
            
    def grab(self, pos):
        self.grabbed = True        
            
    def rotate(self):
        self.image = pg.transform.rotate(self.base_image, degrees(self.angle))
        self.rect = self.image.get_rect(center=self.pos)
        
    def adjust_output(self):
        self.output = 1.0 - (self.angle / float(self.min_angle))
        
    def update(self, mouse_pos):

        self.hovered = get_distance(self.pos, mouse_pos) <= self.radius
        if self.grabbed:
            angle = get_angle(self.pos, mouse_pos)
            if self.angle < .5 * pi:
                if angle > self.min_angle:
                    angle = self.max_angle 
            else:
                if angle > self.min_angle:
                    angle = self.min_angle
            self.angle = angle
        if self.angle != self.last_angle:
            self.rotate()
            self.adjust_output()
        self.last_angle = self.angle
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)