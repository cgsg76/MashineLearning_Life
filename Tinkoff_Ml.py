from graphics import *
import random

W = 30
H = 30
Zoom = 20
Field = []
FieldState = []
NewFieldState = []
Win = GraphWin('LIFE', W * Zoom, H * Zoom)
Run = True

# 0 - empty, 1 - rock, 2 - fish, 3 - shrimp
Colores = [color_rgb(26, 51, 128), color_rgb(153, 153, 153), color_rgb(255, 255, 0), color_rgb(255, 0, 0)]

def Color(x, y):
  Field[y][x].setFill(Colores[NewFieldState[y][x]])

def GetNeigh(x, y, c):
  if x > -1 and x < W and y > -1 and y < H:
    return int(FieldState[y][x] == c)
  return 0

# New status
def NewState(x, y):
  FishSum = -1
  ShrimpSum = -1 #Because we add self
  State = FieldState[y][x]
  if State == 1:
    return

  for j in range(-1, 2):
    for i in range(-1, 2  ):
      FishSum   += GetNeigh(x + i, y + j, 2)
      ShrimpSum += GetNeigh(x + i, y + j, 3)

  if State == 0:
    if FishSum == 3:
      NewFieldState[y][x] = 2
      Color(x, y)
      return
    if ShrimpSum == 3:
      NewFieldState[y][x] = 3
      Color(x, y)
      return

  if (State == 2 and (FishSum < 2 or FishSum > 3)) or (State == 3 and (ShrimpSum < 2 or ShrimpSum > 3)):
    NewFieldState[y][x] = 0
    Color(x, y)
  return

def Move():
  for y in range(H):
    for x in range(W):
      NewState(x, y)
  FieldState = NewFieldState

for y in range(H):
  Field.append([Rectangle(Point(y * Zoom, 0), Point((y + 1) * Zoom, Zoom))])
  for x in range(1, W):
    Field[y].append(Rectangle(Point(y * Zoom, x * Zoom), Point((y + 1) * Zoom, (x + 1) * Zoom)));

for y in range(H):
  NewFieldState.append([3 - (random.randint(0, 5) % 4)])
  Color(0, y)
  for x in range(1, W):
    NewFieldState[y].append(3 - (random.randint(0, 5) % 4))
    Color(x, y)

FieldState = NewFieldState

for y in range(H):
  for x in range(W):
    Field[y][x].draw(Win)

while not Win.isClosed():
  Move()
  time.sleep(1)
  key = Win.checkKey()
  if key == 'space': #pause
    key = Win.checkKey()
    while key != 'space':
      key = Win.checkKey()
  elif key == "Escape": #exit
    break