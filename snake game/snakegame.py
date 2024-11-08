import pygame
from pygame.locals import *
import time
import random

SIZE=40

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen=parent_screen
        self.image=pygame.image.load("apple.jpg").convert()
        self.x=120
        self.y=120

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x=random.randint(1,34)*SIZE
        self.y=random.randint(1,19)*SIZE

class Snake:
    def __init__(self,parent_screen):
        self.parent_screen=parent_screen
        self.block=pygame.image.load("block.jpg").convert()
        self.direction='down'   #it shows the moving direction od snake

        self.length=1
        self.x=[40]#length of snake box
        self.y=[40]

    def move_left(self):
        self.direction='left'

    def move_right(self):
        self.direction='right'

    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        #update head
        if self.direction=='left':
            self.x[0] -=SIZE
        elif self.direction=='right':
            self.x[0] +=SIZE
        elif self.direction=='up':
            self.y[0] -=SIZE
        elif self.direction=='down':
            self.y[0] +=SIZE
        self.draw()
        

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
        #The blit()function in Pygame copies pixels from one surface to another,placing an image onto the screen of a Pygame application
        #(x,y axis)
        #ye method display karegi wo bhi changes kar rahe ho
    
    def increase_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()#Initialize pygame
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()
        self.screen = pygame.display.set_mode((1400, 800))#Set up the game window
        self.snake = Snake(self.screen) # Create an object of Snake   6 is the length of snake
        self.snake.draw()# Initial drawing of the snake
        self.apple=Apple(self.screen)
        self.apple.draw()

    def reset(self):
        self.snake=Snake(self.screen)
        self.apple=Apple(self.screen)

    #collision mei jab snake apple ke uper se jaega to kya hoga
    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1 < x2 + SIZE:     # x1,x2 means snake head
            if y1>=y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.screen.blit(score,(1250,10))
    
    def play_background_music(self):
        pygame.mixer.music.load("bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)
    
    def play_sound(self,sound):
        if sound == "1_snake_game_resources_ding.mp3":
            sound=pygame.mixer.Sound("1_snake_game_resources_ding.mp3")
        elif sound == "1_snake_game_resources_crash.mp3":
            sound=pygame.mixer.Sound("1_snake_game_resources_crash.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("background.jpg")
        self.screen.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        #fir check karna hai ke saare block ka collision ho raha hai ke nhi
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("1_snake_game_resources_ding.mp3")
            self.snake.increase_length()
            self.apple.move()

        #coliding with itself
        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("1_snake_game_resources_crash.mp3")
                raise "Collision Occurred"
            

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.screen.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.screen.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running=True   #infinite time ke window open rahega
        pause=False
        while running:
            for event in pygame.event.get():#agar koi bhi event like mouse ya fir keyboard press karte hai to event hai
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        
                        if event.key == K_UP:
                            self.snake.move_up()
                            
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(0.1)


if __name__=='__main__':
    game=Game()
    game.run()
