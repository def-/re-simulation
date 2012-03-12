from RotaryElement import *

class REPoint:
  def __init__(self, x, y, re, pos):
    self.x = x
    self.y = y
    self.parent = re
    self.pos = pos
    self.pre = self
    self.suc = self

  def stepForward(self, isEntering):
    if isEntering:
      io = self.parent.input(self.pos) # input
      next = self.parent.points[io]
      if next != next.suc:
        return next.suc
      return None # Invalid path
    else:
      return self.parent.points[(self.pos-1)%4].suc

  def stepBackward(self, isEntering):
    if isEntering:
      return self.pre
    else:
      io = self.parent.reverseInput(self.pos) # output
      next = self.parent.points[io]
      if next != next.pre:
        return next.pre
      return None # Invalid path
