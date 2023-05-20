import pygame
import random
from pygame import mixer
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
pygame.font.init()
mixer.init()
sound=mixer.Sound('coll_snd.wav')
# global variables 
screen_width = 800
screen_height = 700
block_size = 30#height and length of each block is 30 pixels
play_width = 300  # meaning 300 / 10  (30 width per block)
play_height = 600  # meaning 600 / 20 (30 height per block)
 
top_left_x = (screen_width - play_width) // 2 #creates the block at the center of the playing part of the window 
top_left_y = screen_height - play_height#creates the block at the topmost part of the playing window 
 
 
# represents each shape and the rotations in these arrays 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '......'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]#placing all the shapes and their rotations as nested arrays
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape in the shapes array 
 
 
class Block:
    def __init__(self,x,y,shape):
        self.x=x#each position of a given shape has rows of dots and 0s this represents the x of the position of the 0 encountered wrt to the x and y coords of the topmost left dot "."
        self.y=y#each position of a given shape has rows of dots and 0s this represents the x of the position of the 0 encountered wrt to the x and y coords of the topmost left dot "."
        self.shape=shape
        self.colour=shape_colors[random.randint(0,6)]#gives random colour for the block
        self.rotation=0
 
def create_grid(occ_posn={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]#generates a 2d array where each element in the array has (0,0,0)
    for i in range(len(grid)):#stands for 20 which is the height or y coord 
        for j in range(len(grid[i])):#stand for 10 which is the length of x coord
            if(j,i) in occ_posn:
                prev_box_color = occ_posn[(j,i)]#here we store all the previously present boxes in the grid coordinates in a dictionary
                #and access it's key(it's color) and store it in the variable 
                grid[i][j]=prev_box_color#we access that particular element in the grid nested array and change its color to the colour stored in the key(prev_box_color)
    return grid 

def convert_shape_format(shape):
    positions=[]
    format=shape.shape[shape.rotation % len(shape.shape)]#here we create an object of name shape and we access its property shape which is a nested array 
    # and it consists of various rotaions of the given shape and it can be made to perform the same rotations on presing key by % operator  
    for i,line in enumerate(format):
        row=list(line)#the format has multiple lines with dots and zeros here we choose only one row
        for j, column in enumerate(row):#here pass through row and check for zero 
            if column=='0':
                positions.append((shape.x+j,shape.y+i))#shape.x and shape.y represent the grid coord values of the topmost left dot and adds that jth and ith value and produces the actual posn of the block in the grid coordinate terms
                #after finding actual coords it appends it to the positions array , this procedure occurs for each of the zero present and their coordinates are added to the array
    #for i,pos in enumerate(positions):
        #positions[i]=(pos[0],pos[1])
    return positions

def valid_space(shape, grid):
    ok_pos=[[(j,i) for j in range(10) if grid[i][j]==(0,0,0)]for i in range(20)]#adds the positions of (0,0,0) or the black space into the ok posns
    ok_pos=[j for sub in ok_pos for j in sub]# flattens 2d array int 1d by changing nested lists into tuples 
    formatted=convert_shape_format(shape)#puts the positons of the boxes of the given shape in the formatted 
    for pos in formatted:
        if pos not in ok_pos:#chceks if a given the grid coords of the boxes of the shape is not in ok_pos, which means the place is not empty, and box cannot be drawn
                return False
    return True
 
def check_lost(positions):
    for pos in positions:
        x,y=pos
        if(y<2):#if y is less than 2 in the grid coord then you have lost the game 
            return True
    return False 

 
def get_shape():
    return Block (5,0,random.choice(shapes))#creates a shape using the class Block 
 
def draw_text_middle(text, size, color, screen):
    font=pygame.font.SysFont("freesansbold.ttf",size,bold=True)
    loser=font.render(text,1,color)
    screen.blit(loser,(top_left_x+play_width/2-(loser.get_width()/2),top_left_y+play_height/2-loser.get_height()))
   
def draw_grid_lines(screen,grid):#draws grid lines using two nested loops 
    start_x=top_left_x
    start_y=top_left_y
    for i in range(len(grid)):
        pygame.draw.line(screen,(128,128,128),(start_x,start_y+i*block_size),(start_x+play_width,start_y+i*block_size))#draws 20 horizontal lines as y is constant in both coords specified but x changes 
        for j in range(len(grid[i])):
            pygame.draw.line(screen,(128,128,128),(start_x+j*block_size,start_y),(start_x+j*block_size,start_y+play_height))#draws 10 vertical lines as x is constant in both the coordonates and y changes 
    pygame.display.update()


def draw_grid(screen,grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen,grid[i][j],(top_left_x+j*block_size,top_left_y+i*block_size,block_size,block_size),0)#draws multiple retangles all throught out the screen 
            #which ever column that is present it multiplies by block size to get x postion in the grid as draw.rect() does not take in the grid coords  
            # and does the same for the rows as well, so now we have the x,y coord required to draw the retangle and 
            #the height and width for the rect is given by both the block_size
    pygame.draw.rect(screen,(255,0,0),(top_left_x,top_left_y,play_width,play_height),4)#draws the outer rectangle of the play area within which the entire block will be moving 
    draw_grid_lines(screen,grid)
    pygame.display.update()

def clear_rows(grid, locked,score):
    counter = 0
    index_last_before_row=0
    for i in range(len(grid)-1,-1,-1):
        row=grid[i]
        if (0,0,0) not in row:#finds out at which ith row is full
            counter+=1#iterates counter and tells us the number of rows deleted and by how much elements above must move
            index_last_before_row=i#tells us from which row we must push down 
            for j in range(len(row)):
                try:
                    del locked[(j,i)]#we clear those allocated positions
                except:
                    continue
    if counter>0:
        score+=counter
        sound.play()
        for key in sorted(list(locked),key=lambda x: x[1])[::-1]: 
            x,y = key
            if y<index_last_before_row:
                newKey = (x,y+counter)#adds the number of rows by which we must push down 
                locked[newKey]=locked.pop(key)#removes the last row of locked that contains the non vacant positions, access the key of this dictionary by the using the value newkey which stores the modified grid coords for the occupied blocks 
    return score , counter
def draw_screen(screen,grid,score,counter):
    screen.fill((0,0,0))
    score+=counter
    font=pygame.font.SysFont('freesansbold.ttf',60)
    heading = font.render('Tetris',1,(255,255,255))
    f=pygame.font.SysFont('freesansbold.ttf',40)
    screen_score=f.render('Score: '+str(score),1,(255,255,255))
    sx=top_left_x+play_width+50#gets the posn where the text next shape must be displayed
    sy=top_left_y+play_height/2-100
    screen.blit(heading,(top_left_x+play_width/2-heading.get_width()/2,30))#places the heading in the middle of the screen 
    screen.blit(screen_score,(20,20))
    draw_grid(screen,grid)
    pygame.display.update()
score =0
counter=0
def game_play(screen):
    occ_posn={}#initially occupied positions is none
    grid=create_grid(occ_posn)
    change_piece=False
    run=True
    global score
    current_piece=get_shape()#gets a shape for the user to play with
    next_piece=get_shape()
    clock=pygame.time.Clock()
    fall_time=0
    fall_vel=0.3
    level_time=0
    while run:
        grid=create_grid(occ_posn)
        fall_time+=clock.get_rawtime() 
        clock.tick()
        if level_time//1000>30:
            level_time=0
            if level_time>0.11:
                level_time-=0.005
        if fall_time/1000>fall_vel:
            fall_time=0
            current_piece.y+=1
            if not(valid_space(current_piece,grid)) and current_piece.y>0:
                current_piece.y-=1
                change_piece=True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    current_piece.x-=1
                    if not(valid_space(current_piece,grid)):
                        current_piece.x+=1#if the space where the block must move is not valid then we add 1 as in this case we subtract to there is no change in the block posn
                if event.key==pygame.K_RIGHT:
                    current_piece.x+=1
                    if not(valid_space(current_piece,grid)):
                        current_piece.x-=1#if the space where the block must move is not valid then we subtract 1 as in this case we add to there is no change in the block posn
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                    if not(valid_space(current_piece,grid)):
                        current_piece.y-=1#we perform the opposite of the function performed in the previous if statement to neutralize it 
                if event.key==pygame.K_DOWN:
                    current_piece.y+=1
                    if not(valid_space(current_piece,grid)):
                        current_piece.y-=1#we perform the opposite of the function performed in the previous if statement to neutralize it 
                pygame.display.update()
        shape_pos=convert_shape_format(current_piece)#stores the grid posns of the blocks 
        for i in range(len(shape_pos)):
            x,y=shape_pos[i]
            if y>-1:
                grid[y][x]=current_piece.colour#stores that rgb values for that coordinate in the grid 
        if change_piece:
            for pos in shape_pos:
                p=(pos[0],pos[1])
                occ_posn[p]=current_piece.colour
            next_piece = get_shape()
            current_piece = next_piece 
            change_piece=False
        score , counter=clear_rows(grid,occ_posn,score)
        if check_lost(occ_posn):
            draw_text_middle("You Lose!", 80, (255, 255, 255), screen)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
        draw_screen(screen,grid,score,counter)
        pygame.display.update()

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Tetris')
game_play(screen)