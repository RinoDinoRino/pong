'''
Pong
'''
import pygame #imports pygame
import os #import os module. Use this to create a directory shortcut
from random import choice, randrange, randint #imports random range, and random integer, and choice. Choice allows random selection from a list.  ->https://stackoverflow.com/questions/55399338/how-to-choose-randomly-between-two-values
pygame.mixer.pre_init(22050, -16, 2, 800) #need to preload sound settings.
pygame.init() #allows imports
pygame.mixer.init(22050, -16, 2, 800) #loaded sound setting. Could not use default as the default buffer is 4k which comes too late for the sound.

# Colors for the game (RGB)
white = (255, 255, 255) #for all other colors
black = (0, 0, 0) # for the background


#windows dimensions, changeable
width, height = 800, 600  #sets width and height

#setting directory, and saving sound. Will implement if have time
directory = os.getcwd() # Opens current directory https://www.tutorialspoint.com/python/os_getcwd.htm
collision_sound = directory + "/sounds/ping_pong_8bit_plop.ogg"  #Found sounds online, learned opening directory trick on stack overflow
pointscored_sound = directory + "/sounds/ping_pong_8bit_beeep.ogg"  # Found sounds online


pygame.display.set_caption("Pong") # sets window title to pong (got from our failed last attempt)


class Player:
    def __init__(self, x_cord, speed ,move_up, move_down):
        self.rect = pygame.Rect(x_cord, height//2, 10, 80) #Creates the blocker. height//2 tells it to start in middle. Rect(left, top, width, height) -> https://www.pygame.org/docs/ref/rect.html
        self.key_up = move_up #defines what key to move up
        self.key_down = move_down #defines what key to move down
        self.score = 0 #their score
        self.speed = speed #sets player speed

    def move(self, surface): #also used to update. Limits player bounds
        if pygame.key.get_pressed()[self.key_up]: #used to see if player pushed their respective key down -> https://github.com/search?q=pygame.key.get_pressed&type=Code&l=Python
            if self.rect.top > 0:#limit movement by the top of box
                self.rect.y -= self.speed #move on the y axis by their speed. Negative moves up
        if pygame.key.get_pressed()[self.key_down]: #checks if player pushed their respective down key
            if self.rect.bottom < height: #move limited by the bottom height
                self.rect.y += self.speed #move only by their speed

        pygame.draw.rect(surface, white, self.rect) #draws each player

class Ball(pygame.sprite.Sprite):            #To make the ball from a sprite. Found documation on pygame https://www.pygame.org/docs/ref/sprite.html
    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)       #call parent class constructor from pygame. Found in documentaion of pygame
        self.rect = pygame.Rect(width//2, randrange(12, height-12), 12, 12) #  Used Rect Arguments to provide cordinates.Random int used to have random y cord->https://stackoverflow.com/questions/27770602/pygame-rect-what-are-the-arguments
        self.direction_x = direction #moves in x direction, and y direction at the same pace
        self.direction_y = direction #moves in x direction, and y direction at the same pace
        self.speed = 1

    def ball_movement(self, surface): #track ball.
        if self.rect.bottom > height or self.rect.top < 0:
            pygame.mixer.music.load(collision_sound) #load sound to be used
            pygame.mixer.music.play() #play sound
            self.direction_y *= -1

        self.rect.x += self.direction_x * self.speed #track ball for updating screen
        self.rect.y += self.direction_y * self.speed #track ball for updating screen. BUG: This way of calculating y will exponentially increase ball y movement due to speed and direction being capable of multiplying exponentially.

        pygame.draw.rect(surface, white, self.rect) #draw instead of blit because  not transfering image ->https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect

class Game():
    def __init__(self):
        self.window = pygame.display.set_mode((width, height))      #"Initialize a window or screen for display"     https://www.pygame.org/docs/ref/display.html#pygame.display.list_modes, # why 2 parantheses(debugging) https://stackoverflow.com/questions/24189241/pygame-error-typeerror-must-be-2-item-sequence
        self.ball = Ball(choice([1, -1])) #when the game start, the ball will randomly decide to go left or right
        self.player1 = Player(10 , 4, pygame.K_w, pygame.K_s) #Constructs player 1 object
        self.player2 = Player(width-10, 4, pygame.K_UP, pygame.K_DOWN) #constructs player 2 object
        self.clock = pygame.time.Clock() #game clock required to use tick method which controls framerate
        self.menu = Menu(self.window) #Initalizes Menu window


    def play_board(self):
        self.window.fill(black) #fill window as black
        self.ball.ball_movement(self.window)  #draws location of the current ball location
        self.player1.move(self.window)  #draws player 1 and their movements
        self.player2.move(self.window) #draws player 2 nd their movement
        self.draw_score() # draw the score_font
        self.collision() #checks for collision
        self.track_score() #tracks_score
        pygame.draw.rect(self.window, white, (width // 2, 0, 2, height)) #draws middle line
        pygame.display.update() #updates window for all new items ->https://www.pygame.org/docs/ref/display.html#pygame.display.update


    def collision(self):
        if pygame.sprite.collide_rect(self.player1, self.ball):  #checks for collision w/P1 ->https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_rect
            pygame.mixer.music.load(collision_sound) #load sound to be used
            pygame.mixer.music.play() #play sound
            self.ball.direction_x *= -1 #opposite x direction if collision_sound
            #self.ball.direction_y =    #change how ball moves in y direction
            self.ball.speed += 0.4 # increase ball speed

        if pygame.sprite.collide_rect(self.ball, self.player2):  #checks for collision w/P2 -> collide_rect(left, right) ->https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_rect
            self.ball.direction_x *= -1 #opposite x direction if collision_sound
            pygame.mixer.music.load(collision_sound) #load sound to be used
            pygame.mixer.music.play() #play sound
            #self.ball.direction_y =      #can change how the ball behaves later
            self.ball.speed += 0.4 # increase ball speed, ball direction/

        def start(self):
            select_screen = self.menu.start() #start at menu
            self.clock.tick(150) #control framerate, we think

    def track_score(self): #checks if the ball hit the side borders, and gives score arcodinly
        if self.ball.rect.left <= 0:
            pygame.mixer.music.load(pointscored_sound) #Load Sound
            pygame.mixer.music.play() #Play Sound
            self.player2.score += 1 #Increment PLayer 2 score by 1
            self.ball = Ball(1) #tell ball to start the next round moving right

        if self.ball.rect.right >= width:
            pygame.mixer.music.load(pointscored_sound) #Load scored sound
            pygame.mixer.music.play() #play loaded sound
            self.player1.score += 1 #Increment PLayer 1 score by 1
            self.ball = Ball(-1) #tell ball to start the next round moving left


    def draw_score(self):
        #turn player score into string
        p1_score = str(self.player1.score)
        p2_score = str(self.player2.score)

        #create socre font and the object
        score_font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 80) #creates a font that is appropiate for score
        p1_score = score_font.render(p1_score, True, white)
        p2_score = score_font.render(p2_score, True, white)

        #Blits objects onto screen. Basically redraws items
        p1_score_rect = p1_score.get_rect(center=(width // 2 - 200, 50))
        p2_score_rect =p2_score.get_rect(center=(width // 2 + 200, 50))
        self.window.blit(p1_score, p1_score_rect)
        self.window.blit(p2_score, p2_score_rect)


    def main(self): # Required to run the game
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.play_board()
            self.clock.tick(150) # Controls framerate so its universal across computers

    def start(self):
        self.menu.begin_game()
        self.main()
        self.play_board()

class Menu:
    def __init__(self, window):
        self.window = window #window of the game
        #self.clock = pygame.time.Clock() # control framerate, worry bout later

    def begin_game(self):
        pvp_font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 30) #Font(filename, size) https://www.pygame.org/docs/ref/font.html#pygame.font.Font
        pvp_text = pvp_font.render("Player vs Player", True, white) #draws texts on a surface -> https://www.pygame.org/docs/ref/font.html
        pvp_rect = pvp_text.get_rect(center=(width//2, 425)) #where the text gets drawn, center tells the text to be drawn cenetered at a position. -> https://www.pygame.org/docs/ref/surface.html

        title_font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 150) #Font(filename, size) https://www.pygame.org/docs/ref/font.html#pygame.font.Font
        title_text = title_font.render("Pong", True, white) #render(text, antialias, color, background=None)  ->https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
        title_rect = title_text.get_rect(center=(width // 2, 100)) #creates the title, center makes the title centered at position https://www.pygame.org/docs/ref/surface.html

        space_font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 45) #creates a font size for press space
        press_space = space_font.render("Press SPACE to start", True, white) #tells user to push space
        press_space_rect = press_space.get_rect(center=(width // 2, 230)) #draws string in the middle

        running = True   #keep main menu running
        while running:
            self.window.fill(black) #fills whole window black ->https://www.pygame.org/docs/ref/surface.html
            self.window.blit(title_text, title_rect) #blit allows objects to be drawn upone
            self.window.blit(pvp_text, pvp_rect) # creates the push space
            self.window.blit(press_space, press_space_rect)
            for event in pygame.event.get(): #Gathers events, required for pygrame.key.get_pressed
                if event.type == pygame.QUIT:
                    running = False
            if pygame.key.get_pressed()[pygame.K_SPACE]: #When space is pushed, we break out of running loop.
                break
            pygame.display.update() #Continously updates display


if __name__ == '__main__': #allow you to import its code without execution... It also indicates the starting point of the script when executing ->https://dev.to/wangonya/what-s-the-use-of-if-name-main-in-python-3eo5
    game = Game() #game variable defined as game class
    game.start() #starts the game
