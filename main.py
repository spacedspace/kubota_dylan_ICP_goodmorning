# this file was created by Dylan Kubota
# code inspired by game dev Chris Bradfield
# who was inspired by Notch

# import pygame and other files
import pygame as pg
from settings import *
from sprites import *
from utils import *
from math import floor


'''
Data types: boolean, string, int, etc.

Input/events: keyboard, mouse, voice, power button,
eye tracking, camera, gyroscoping, electrostatic,
location, volume, mic, etc.

Process: cursor position, player position, score,
enemy position, aim in FPS, etc.

Output: graphics - things are drawn, sound - , etc.

First game idea: puzzle game with separate txt files for levels with different
objects as powerups to use strategically to reach the exit

GOALS: Reach the level exit

RULES: Can only jump with power up,
powerups are single-use unless multiple are collected

FEEDBACK: Powerups make sounds when picked up,
powerups also make sounds when used

FREEDOM: Affected by gravity, can't jump without powerup,
confined to the walls of the level

MECHANICS: Player can move left and right,
can use powerups picked up throughout the level


'''

# set properties, etc. for objects within Game
class Game:
    # initiate the game, characters, music, etc.
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
        self.high_score = 0
        self.score = 0
    
    # load data from  text files, images, audio, etc.
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "high_score.txt")
        self.img_dir = path.join(self.game_dir, "images")
        self.snd_dir = path.join(self.game_dir, "audio")
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "coin02.wav"))
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_dir, "jump1.mp3"))
        self.map = Map(path.join(self.game_dir, map))


        # save high score to a txt file
        try:
            with open(self.game_save_file, "x", encoding="utf-8") as file:
                file.write("hello world")
            print("file created successfully!")
        except FileExistsError:
            print("high score file already exists")
        
        with open(self.game_save_file, "r") as file:
            try:
                self.high_score = int(file.read())
            except:
                self.high_score = 0
                print("high score set to 0")

    # makes player, walls, mobs, etc.
    def new(self):
        self.load_data("level1.txt")
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()


        # instantiates entities based on the level map
        # walls
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
        # mobs
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "M":
                    Mob(self, col, row)
        
        # coins
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "C":
                    Coin(self, col, row)
        # player
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row)
        # plays background music
        pg.mixer.music.load(path.join(self.snd_dir, "see_me_again_instrumental.mp3"))
        pg.mixer.music.play(loops=-1)


    # runs the game
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    # inputs and happenings after game is closed
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.score > self.high_score:
                    with open(path.join(self.game_dir, self.game_save_file), "w") as f:
                        f.write(str(self.score))
                if self.playing:
                    self.playing = False
                self.running = False
    
    # function to put text on the screen like score or fps
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font("Baskerville Old Face")
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    
    # animations
    def update(self):
        self.all_sprites.update()

    # puts stuff on the screen
    def draw(self):
        # order matters: the first things are on the bottom because they are drawn "first"
        # the last lines are on top
        self.screen.fill(TAN)
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames per second: " + str(floor(1/self.dt)), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Coins: " + str(self.player.coins), 24, WHITE, WIDTH/2, HEIGHT/7)
        self.draw_text("Score: " + str(self.score), 24, WHITE, WIDTH/2, HEIGHT/9)
        self.draw_text("High score: " + str(self.high_score), 24, WHITE, WIDTH/2, HEIGHT/12)
        pg.display.flip()


# makes it so that the game only runs in this file
if __name__ == "__main__":
    g = Game()

# keeps the game running instead of instantly crashing
while g.running:
    g.new()
    g.run()