import pygame, sys, random
from pygame.math import Vector2

#"A class is like a blueprint while an instance is a copy of the class with actual values"(geeksforgeeks)
#self used to represent instance.
class SNAKE:
    #init is used to initiate a class
    #"The self parameter is a reference to the current instance of the class, and is used to access variables that belongs to the class"(w3schools)

    def __init__(self):
        #describes the starting point, direction of snake
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        #To make the snake appear on the display surface
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            #fill in the blocks in snake
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block == True:
            #if snake eats the apple, we need to add an extra block to the snake
            #syntax for insert: list_name.insert(index, element)
            body_copy = self.body[:]
            #here, we're adding two vectors to get the new position of snake
            body_copy.insert(0, body_copy[0] + self.direction)
            #now we replace the old values in self.body to the new position
            self.body = body_copy[:]
        else:
            #if snake doesn't eat the apple, it needs to remove one block from the end and add one block to the head of the snake in the direction
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        #we use the following line to prevent the blocks from being added repeatedly
        self.new_block = False

    def add_block(self):
        #This becomes True when the snake eats the apple
        self.new_block = True


class FRUIT:

    def __init__(self):
        #used to create a fruit at a random position
        self.randomize()

    def draw_fruit(self):
        #apple is filled - to appear on the display
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)


    def randomize(self):
        #creates random x and y coordinates for the apple within range of the display
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        #checks if snake is moving, collides or "eats" apple, collides with wall/itself and then updates the snake
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        #if snake "collides" with apple, we randomize a new apple and increase length of snake
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            #checks for collision with wall
            self.game_over()

        for block in self.snake.body[1:]:
            #checks for collison with itself
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()



#initializes pygame
pygame.init()

cell_size=40
cell_number=20

#to create a display window
screen=pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))

#in order to make sure that the game runs at almost the same speed on different computers
#time.Clock() returns processor time
clock=pygame.time.Clock()

main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
#screen is updated every 150 milliseconds to check for user input

pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    #event loop: loop that looks for different events - event refers to some kind of user input
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            #pygame.quit() is the opposite of pygame.init()
            pygame.quit()
            #only using pygame.quit() is not enough, might lead to some complications as other parts of program might keep running
            #sys->another python module ->needs to be imported
            #sys - This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            #Used to change direction of snake when user presses up,down,left or right keys
            #need to be careful about opposite direction cases
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)


    #fill colour in the screen
    screen.fill((175,215,70))

    #used to draw all the elements
    main_game.draw_elements()

    #used to update display
    pygame.display.update()


    #clock.tick() just sets up how fast game should run or how often while loop should update itself, run through itself
    #clock.tick(framerate)
    clock.tick(60)
