from lib import graphics, euclid
import math

class Connection(graphics.Sprite):
  def __init__(self, x, y, x2, y2, arrowSize=20, width=5):
    graphics.Sprite.__init__(self, 0, 0, snap_to_pixel=True)

    x = float(x)
    y = float(y)
    x2 = float(x2)
    y2 = float(y2)
    arrowSize = float(arrowSize)
    width = float(width)

    slopy = math.atan2(y - y2, x - x2)
    cosy = math.cos(slopy)
    siny = math.sin(slopy)

    yDraw = y
    xDraw = x
    y2Draw = y2
    x2Draw = x2

    # Specialized solution
    if abs(x-x2) < 1e-6:
      if y2 > y:
        yDraw -= width / 2
        y2Draw += width / 2
      else:
        yDraw += width / 2
        y2Draw -= width / 2
    elif abs(y-y2) < 1e-6:
      if x2 > x:
        xDraw -= width / 2
        x2Draw += width / 2
      else:
        xDraw += width / 2
        x2Draw -= width / 2

    # Line
    self.graphics.move_to(xDraw, yDraw)
    self.graphics.line_to(x2Draw, y2Draw)
    self.graphics.fill_stroke(stroke="#000", line_width=width)

    # Arrow
    self.graphics.move_to(x2, y2)
    self.graphics.line_to(x2 + (arrowSize * cosy - arrowSize / 2 * siny),
                          y2 + (arrowSize * siny + arrowSize / 2 * cosy))
    self.graphics.line_to(x2 + (arrowSize * cosy + arrowSize / 2 * siny),
                          y2 - (arrowSize / 2 * cosy - arrowSize * siny))

    self.graphics.fill("#000")

    # Fix start and end point; ugly solution
    #self.graphics.circle(x, y, width / 2)
    #self.graphics.circle(x2, y2, width / 2)
    #self.graphics.fill("#000")

    self.xStart = x
    self.yStart = y
    self.xEnd = x2
    self.yEnd = y2

  def getStartPos(self):
    return (self.xStart,self.yStart)

  def getEndPos(self):
    return (self.xEnd, self.yEnd)
