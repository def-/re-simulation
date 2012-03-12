from lib import graphics, euclid
import math
from time import sleep

from REPoint import *

class State:
  H = False
  V = True

class Direction:
  CLOCK = 1
  COUNTERCLOCK = -1

class IO:
  INPUT = True
  OUTPUT = False
  N = 0
  E = 1
  S = 2
  W = 3

class RotaryElement:
  def __init__(self, scene, x, y, state=State.H, width=5):
    self.state = state
    self.x = x
    self.y = y
    self.scene = scene

    size = 100
    rotaryBarLength = 80

    self.points = (REPoint(x-size/4, y-size/4, self, IO.N)  # N input, W output
                 , REPoint(x+size/4, y-size/4, self, IO.E)  # E input, N output
                 , REPoint(x+size/4, y+size/4, self, IO.S)  # S input, E output
                 , REPoint(x-size/4, y+size/4, self, IO.W)) # W input, S output

    self.box = Box(x, y, size, width)
    self.center = Center(self, x, y, float(width)*2)
    self.rotaryBar = RotaryBar(self, x, y, rotaryBarLength, width)

    if state == State.V:
      self.rotaryBar.rotation=math.pi/2
      self.rotaryBar.rotGoal=math.pi/2

    scene.add_child(self.box)
    scene.add_child(self.center)
    scene.add_child(self.rotaryBar)

  def done(self, sprite):
    pass

  def rotate(self, direction):
    self.rotaryBar.rotate(math.pi/2 * direction, on_complete=self.done)
    self.state = not self.state

  def input(self, inp):
    if inp == IO.N:
      if self.state == State.H:
        self.rotate(Direction.COUNTERCLOCK)
        return IO.W
      return IO.S

    if inp == IO.E:
      if self.state == State.V:
        self.rotate(Direction.COUNTERCLOCK)
        return IO.N
      return IO.W

    if inp == IO.S:
      if self.state == State.H:
        self.rotate(Direction.COUNTERCLOCK)
        return IO.E
      return IO.N

    if inp == IO.W:
      if self.state == State.V:
        self.rotate(Direction.COUNTERCLOCK)
        return IO.S
      return IO.E

  def reverseInput(self, outp):
    if outp == IO.W:
      if self.state == State.H:
        self.rotate(Direction.CLOCK)
        return IO.W
      return IO.N

    if outp == IO.N:
      if self.state == State.V:
        self.rotate(Direction.CLOCK)
        return IO.N
      return IO.E

    if outp == IO.E:
      if self.state == State.H:
        self.rotate(Direction.CLOCK)
        return IO.E
      return IO.S

    if outp == IO.S:
      if self.state == State.V:
        self.rotate(Direction.CLOCK)
        return IO.S
      return IO.W

  def getPos(self, typeIO, direction):
    x,y = 0,0

    if direction == IO.N:
      y = -50
      if typeIO == IO.INPUT:
        x = 25
      else:
        x = -25
    elif direction == IO.E:
      x = 50
      if typeIO == IO.INPUT:
        y = 25
      else:
        y = -25
    elif direction == IO.S:
      y = 50
      if typeIO == IO.INPUT:
        x = -25
      else:
        x = 25
    elif direction == IO.W:
      x = -50
      if typeIO == IO.INPUT:
        y = -25
      else:
        y = 25

    return (x + self.x, y + self.y)

class Box(graphics.Sprite):
  def __init__(self, x, y, size, width=5):
    graphics.Sprite.__init__(self, x, y, snap_to_pixel=True)

    self.graphics.rectangle(-size/2, -size/2, size, size, 0)
    self.graphics.fill_stroke(stroke="#000", line_width=width)

class Center(graphics.Sprite):
  def __init__(self, parentRE, x, y, radius=10.):
    graphics.Sprite.__init__(self, x, y, snap_to_pixel=False, interactive=True)
    self.parentRE = parentRE

    self.connect("on-mouse-down", self.on_mouse_down)

    self.graphics.circle(0, 0, radius)
    self.graphics.fill("#000")

  def on_mouse_down(self, sprite, foo):
    self.parentRE.rotate(Direction.COUNTERCLOCK)

class RotaryBar(graphics.Sprite):
  def __init__(self, parentRE, x, y, length, width):
    graphics.Sprite.__init__(self, x, y, pivot_x=0, pivot_y=0, snap_to_pixel=False)

    self.parentRE = parentRE
    self.graphics.move_to(-length/2, 0)
    self.graphics.rel_line_to(length, 0)
    self.graphics.fill_stroke(stroke="#000", line_width=width)

    self.rotGoal = self.rotation

  def rotate(self, radians, on_complete=None):
    #if not self.get_scene().tweener.get_tweens(self):
    self.rotGoal += radians
    self.animate(duration=self.parentRE.scene.durationRotation, rotation=self.rotGoal, on_complete=on_complete)
