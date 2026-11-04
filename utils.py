import pygame as pg
from settings import *
from math import floor

class Map:
    def __init__(self, filename):
        # map and how to navigate it
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())
        
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class Spritesheet:
    def __init__(self, filename):
        # allows for the use of images 
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # makes the image a variable you can use on screen
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image

class Timer:
    def __init__(self):
        self.event_time = 0
        self.current_time = 0
        self.delta = 0
    
    def ticking(self):
        # gets current time and difference between current time and when the event happened
        self.current_time = floor(pg.time.get_ticks()/1000)
        self.delta = self.current_time - self.event_time