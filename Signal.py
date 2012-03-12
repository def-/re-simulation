from lib import graphics, euclid
from lib.pytweener import Easing
from time import sleep
from math import sqrt

from REPoint import *

class Signal(graphics.Sprite):
  def __init__(self, window, x, y, radius=15, speed=100):
    graphics.Sprite.__init__(self, x, y, snap_to_pixel=True, draggable=True)
    self.connect("on-drag-finish", self.on_drag_finish)

    self.graphics.circle(0, 0, float(radius))
    self.graphics.fill("#f00")

    self.window = window
    self.point = None
    self.allPoints = {}
    self.isEntering = True
    self.playing = False
    self.active = False
    self.speed = speed
    self.stepsToGo = 0

  def on_complete(self, sprite):
    self.active = False
    if self.playing:
      self.moveForward(easing=Easing.Linear.ease_in_out)
      self.stepsToGo = 0
    elif self.stepsToGo > 0:
      self.moveForward(easing=Easing.Linear.ease_in_out)
      self.stepsToGo -= 1
    elif self.stepsToGo < 0:
      self.moveBackward(easing=Easing.Linear.ease_in_out)
      self.stepsToGo += 1

  def pause(self):
    self.playing = False

  def playForward(self):
    if self.active or not self.point:
      return

    self.playing = True
    self.on_complete(self)

  def moveForward(self, easing=Easing.Linear.ease_in_out):
    if self.active or not self.point:
      self.stepsToGo += 1
      return

    self.active = True

    self.point = self.point.stepForward(self.isEntering)

    if not self.point:
      self.active = False
      return

    self.isEntering = True
    dist = sqrt((self.x - self.point.x)**2 + (self.y - self.point.y)**2)

    self.animate(duration=dist/self.speed, x=self.point.x, y=self.point.y, on_complete=self.on_complete, easing=easing)

    if dist == 0 and self.playing:
      self.window.clickedPlayPause(None)

  def moveBackward(self, easing=Easing.Linear.ease_in_out):
    if self.active or not self.point:
      self.stepsToGo -= 1
      return

    self.active = True

    self.point = self.point.stepBackward(self.isEntering)

    if not self.point:
      self.active = False
      return

    if isinstance(self.point, REPoint):
      self.isEntering = False
    else:
      self.isEntering = True

    dist = sqrt((self.x - self.point.x)**2 + (self.y - self.point.y)**2)

    self.animate(duration=dist/self.speed, x=self.point.x, y=self.point.y, on_complete=self.on_complete, easing=easing)

  def on_drag_finish(self, scene, event):
    self.goToClosestPoint()

  def goToClosestPoint(self):
    if self.point and self.x == self.point.x and self.y == self.point.y:
      return

    closest = (None,None)
    dist = float("infinity")

    for point in self.allPoints:
      newDist = sqrt((point[0] - self.x)**2 + (point[1] - self.y)**2)
      if newDist < dist:
        closest = point
        dist = newDist

    if not closest:
      return

    self.x = closest[0]
    self.y = closest[1]
    self.point = self.allPoints[closest]

    self.isEntering = True # Predictable
