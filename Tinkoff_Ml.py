from graphics import *
import random, time

W = 30
H = 30
Zoom = 20
Field = []
FieldState = []
NewFieldState = []
DrawQueue = []
Win = GraphWin('LIFE', W * Zoom, H * Zoom)
LastTime = time.process_time()

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
  FishSum = 0
  ShrimpSum = 0
  State = FieldState[y][x]
  if State == 1:
    return

  for j in range(-1, 2):
    for i in range(-1, 2):
      if i != 0 or j != 0:
        FishSum   += GetNeigh(x + i, y + j, 2)
        ShrimpSum += GetNeigh(x + i, y + j, 3)

  if State == 0:
    if FishSum == 3:
      NewFieldState[y][x] = 2
      DrawQueue.append([x, y])
      return
    if ShrimpSum == 3:
      NewFieldState[y][x] = 3
      DrawQueue.append([x, y])
      return

  if (State == 2 and (FishSum < 2 or FishSum > 3)) or (State == 3 and (ShrimpSum < 2 or ShrimpSum > 3)):
    NewFieldState[y][x] = 0
    DrawQueue.append([x, y])
  return

def DrawField():
  global LastTime
  for coord in DrawQueue:
    Color(coord[0], coord[1])
  DrawQueue.clear()
  LastTime = time.process_time()

def Move():
  for y in range(H):
    for x in range(W):
      NewState(x, y)
  DrawField()
  FieldState = NewFieldState

def Restart():
  for y in range(H):
    for x in range(W):
      DrawQueue.append([x, y])
      FieldState[y][x] = NewFieldState[y][x] = random.randint(0, 3)
  DrawField()

#create array
for y in range(H):
  Field.append([Rectangle(Point(y * Zoom, 0), Point((y + 1) * Zoom, Zoom))])
  for x in range(1, W):
    Field[y].append(Rectangle(Point(y * Zoom, x * Zoom), Point((y + 1) * Zoom, (x + 1) * Zoom)));

for y in range(H):
  NewFieldState.append([random.randint(0, 3)])
  Color(0, y)
  for x in range(1, W):
    NewFieldState[y].append(random.randint(0, 3))
    Color(x, y)

FieldState = NewFieldState

for y in range(H):
  for x in range(W):
    Field[y][x].draw(Win)

IsPause = False

while not Win.isClosed():
  if not IsPause and time.process_time() - LastTime > .7:
    Move()
  key = Win.checkKey()
  if key == 'space': #pause
    IsPause = not IsPause
  elif key == 'r' or key == 'R' or key == 'К' or key == 'к': #restart, working with caps lock and Russian keyboard
    Restart()
  elif key == "Escape": #exit
    break
