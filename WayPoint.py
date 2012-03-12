class WayPoint:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.pre = self
    self.suc = self

  def stepForward(self, isEntering):
    return self.suc

  def stepBackward(self, isEntering):
    return self.pre
