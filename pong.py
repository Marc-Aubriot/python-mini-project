import pygame
from pygame.locals import *
import random
     

class Player_One:

    def __init__(self) -> None:
        self.coordinates = (50, 50)
        self.form = (20, 150)
        self.body = pygame.Rect(self.coordinates[0], self.coordinates[1], self.form[0], self.form[1])
        self.speed = 15
        self.direction = 'none'

    def change_direction(self, direction):
        if direction == "up":
            self.direction = "up"
        elif direction == "down":
            self.direction = "down"
        elif direction == "none":
            self.direction = "none"

    def update_position(self):
        if self.direction == "up" and self.coordinates[1] > 2:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - self.speed)
        elif self.direction == "down" and self.coordinates[1] < (798 - self.form[1]):
            self.coordinates = (self.coordinates[0], self.coordinates[1] + self.speed)
        else:
            self.coordinates = (self.coordinates[0], self.coordinates[1])
        self.body = pygame.Rect(self.coordinates[0], self.coordinates[1], self.form[0], self.form[1])

class Ball:
    
    def __init__(self) -> None:
        self.coordinates = (400,400)
        self.form = (40, 40)
        self.body = pygame.Rect(self.coordinates[0], self.coordinates[1], self.form[0], self.form[1])
        self.Xspeed = 6
        self.Yspeed = 0

    def check_collision(self, player1, borders, wall, game_end):
        if pygame.Rect.colliderect(self.body, player1.body):            # collision avec le joueur
            self.Yspeed = random.randint(1, 4) * random.choice((1, -1))
            self.Xspeed = self.Xspeed * -1
        elif pygame.Rect.colliderect(self.body, wall.body):             # collision avec le mur   
            self.Xspeed = self.Xspeed * -1
        elif pygame.Rect.colliderect(self.body, borders.top_body):      # collision avec la bordure top
            self.Yspeed = random.randint(1, 4) * 1
        elif pygame.Rect.colliderect(self.body, borders.bot_body):      # collision avec la bordure bot
            self.Yspeed = random.randint(1, 4) * -1
        elif pygame.Rect.colliderect(self.body, game_end.body):   # collision avec la ligne de game over
            return True

    def update_position(self):
        self.coordinates = (self.coordinates[0] + self.Xspeed, self.coordinates[1] + self.Yspeed)
        self.body = pygame.Rect(self.coordinates[0], self.coordinates[1], self.form[0], self.form[1])

class Wall:
    
    def __init__(self) -> None:
        self.coordinates = (775,0)
        self.body = pygame.Rect(self.coordinates[0], self.coordinates[1], 25, 800)

class Border:

    def __init__(self) -> None:
        self.top_coordinates =  (0,0)
        self.top_body = pygame.Rect(self.top_coordinates[0], self.top_coordinates[1], 800, 1)
        self.bot_coordinates = (0, 799)
        self.bot_body = pygame.Rect(self.bot_coordinates[0], self.bot_coordinates[1], 800, 1)

class Loose_Line:
    
    def __init__(self) -> None:
        self.coordinates = (0, 0)
        self.body = pygame.Rect(self.coordinates[0], self.coordinates[1], 2, 800)

class Score:
    pass

class Game:

    def __init__(self) -> None:
        self.instance = pygame.init()
        self.title = pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.background_color = pygame.Color(0, 0, 0) #BLACK
        self.bar_color = pygame.Color(255, 255, 255) #WHITE
        self.ball_color = pygame.Color(255, 0, 0) #RED
        self.wall_color = pygame.Color(0, 255, 0) #GREEN
        self.screen_width = 800
        self.screen_height = 800
        self.screen_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.player1 = Player_One()
        self.ball = Ball()
        self.wall = Wall()
        self.borders = Border()
        self.game_over_line = Loose_Line()
        self.display.fill(self.background_color)

    def inputs(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.player1.change_direction("up") 
                    elif event.key == K_DOWN:
                        self.player1.change_direction("down") 
                else:
                    self.player1.change_direction("none")

    def logic(self):
        self.player1.update_position()
        if self.ball.check_collision(self.player1, self.borders, self.wall, self.game_over_line):
            self.game_over()
        self.ball.update_position()

    def draw(self):
        pygame.display.flip()                                                      # Refresh on-screen display
        self.clock.tick(60)                                                        # wait until next frame (60fps)
        pygame.draw.rect(self.display, self.background_color, self.screen_rect)    # efface l'écran
        pygame.draw.rect(self.display, self.bar_color, self.player1.body)          # affiche player 1
        pygame.draw.rect(self.display, self.ball_color, self.ball.body)            # affiche la balle
        pygame.draw.rect(self.display, self.wall_color, self.wall.body)            # affiche le mur

    def start(self):
        while True:
            # Process player inputs
            self.inputs()

            # Do logical  updates 
            self.logic()

            # Render the graphics here
            self.draw()

    def game_over(self):
        print('game over')

# game init
game = Game()
game.start()