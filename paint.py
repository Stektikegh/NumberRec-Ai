import pygame
import sys
import math
import torch
from idk import guess_number

pygame.init()

screen_width, screen_height = 560, 580

screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
PIXEL = 20

class Dot():
  def __init__(self, x, y):
    self.width = PIXEL
    self.color = BLACK
    self.x = x
    self.y = y
  def draw(self):
    pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

def pixelate(value):
  return math.floor(value/PIXEL)*PIXEL

dots = []
PIXELCANVAS = 28
for i in range(PIXELCANVAS):
  dots.append([])
  for j in range(PIXELCANVAS):
    dots[i].append(Dot(j*PIXEL, i*PIXEL))


def clear():
  for i in range(PIXELCANVAS):
    for j in range(PIXELCANVAS):
      dots[i][j].color = BLACK

font = pygame.font.Font(None, 20)

mouse_pressed = False

def color_neighbooring(x, y):
  if dots[int(y/20)][int(x/20)+1].color == BLACK:
    dots[int(y/20)][int(x/20)+1].color = GRAY
    
  if dots[int(y/20)][int(x/20)-1].color == BLACK:
    dots[int(y/20)][int(x/20)-1].color = GRAY
    
  if dots[int(y/20)-1][int(x/20)+1].color == BLACK:
    dots[int(y/20)-1][int(x/20)+1].color = GRAY
    
  if dots[int(y/20)+1][int(x/20)-1].color == BLACK:
    dots[int(y/20)+1][int(x/20)-1].color = GRAY
  

def color(x, y):
  dots[int(y/20)][int(x/20)].color = WHITE
  color_neighbooring(x, y)

def update():

  mouseX = pygame.mouse.get_pos()[0]
  mouseY = pygame.mouse.get_pos()[1]
  pygame.draw.rect(screen, WHITE, (pixelate(mouseX), pixelate(mouseY), PIXEL, PIXEL))
  if left_pressed:
    try:
      color(mouseX, mouseY)
    except:
      pass
  if right_pressed:
    try:
      dots[int(mouseY/20)][int(mouseX/20)].color = BLACK
    except:
      pass
  for row in range(PIXELCANVAS):
    for dot in dots[row]:
      dot.draw()

  
  # create the tensor
  tensor = [[]]
  for i in range(PIXELCANVAS):
    tensor[0].append([])
    for j in range(PIXELCANVAS):
      if dots[i][j].color == WHITE:
        tensor[0][i].append(255)
      elif dots[i][j].color == GRAY:
        tensor[0][i].append(100)
      else:
        tensor[0][i].append(0)
  tensor = torch.tensor(tensor).type(torch.float)

  number = guess_number(tensor=tensor)

  # doing the labeling stuff
  
  text_surface = font.render(f"number is {number}", True, WHITE)
  screen.blit(text_surface, (10, 560))


running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      print("Closing Window ...")
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_c:
        print('Clearing ...')
        clear()
    
  left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()  
  screen.fill(BLACK)
  update()
  pygame.display.flip()


pygame.quit()
sys.exit()