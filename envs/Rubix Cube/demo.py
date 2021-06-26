import pygame
from pygame.locals import *
import sys

 
display_window = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Rubics Cube Solver')                        #set title of window
 
map_data = [[[1,1,1],
             [1,1,1],
             [1,1,1]],
            [[1,1,1],
             [1,1,1],
             [1,1,1]],
            [[1,1,1],
             [1,1,1],
             [1,1,1]]]
 
wall = pygame.image.load('wall.png')
 
width, height = 64, 64


for height_no, c_height in enumerate(map_data):
    print(height_no,height)
    for row_no, row in enumerate(c_height):
        print(row_no,row)
        for col_no, col in enumerate(row):
            print(col_no,col)
            tileImage = wall
            print("col no, height_no=",col_no,height_no)
            temp_x = (row_no - height_no) * width // 2
            temp_y = (col_no - height_no) * height // 2
            print("temp_x,temp_y=",temp_x,temp_y)
            x = (temp_x - temp_y) 
            y = (temp_x + temp_y) // 2
            print("x,y=",x,y)
            centered_x = display_window.get_rect().centerx + x
            centered_y = display_window.get_rect().centery + y
            display_window.blit(tileImage, (centered_x, centered_y))       #display the wall


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
 
    pygame.display.flip()