from RotaryElement import *
from Signal import *
from Connection import *
from ReWindow import *
from WayPoint import *

class Parser:
  def __init__(self):
    self.allConns = []
    self.start = None
    self.startPoint = None
    self.elems = {}
    self.allPoints = {}

  def getXY(self, str):
    assert str[0] == "("
    assert str[-1] == ")"

    xy = str[1:-1].split(",")

    assert len(xy) == 2

    return (int(xy[0]),int(xy[1]))

  def getXYZ(self, str):
    assert str[0] == "["
    assert str[-1] == "]"

    xyz = str[1:-1].split(",")

    assert len(xyz) == 3
    assert xyz[0] == "|" or xyz[0] == "-"

    return (int(xyz[1]), int(xyz[2]), xyz[0] == "|")

  def getIO(self, str):
    assert str in ["N", "E", "S", "W"]

    if str == "N":
      return IO.N
    if str == "E":
      return IO.E
    if str == "S":
      return IO.S
    else:
      return IO.W

  def getREPredecessor(self, str):
    if str[0] == "{":
      assert str[1] in ["N","E","S","W"]
      assert str[2] == "}"

      str = str[3:]

    pos = str.find("{")

    assert pos != -1
    assert str[pos+2] == "}"

    io = self.getIO(str[pos+1])
    name = str[:pos]

    assert self.elems.has_key(name)

    conn = self.elems[name]
    return (conn, io)

  def getRESuccessor(self, str):
    assert str[0] == "{"
    assert str[2] == "}"

    io = self.getIO(str[1])

    str = str[3:]
    pos = str.find("{")

    if pos != -1:
      assert str[pos+2] == "}"

      str = str[:pos]

    assert self.elems.has_key(str)

    conn = self.elems[str]
    return (conn, io)

  def getWayPoint(self, x,y):
    if not self.allPoints.has_key((x,y)):
      self.allPoints[(x,y)] = WayPoint(x,y)
    return self.allPoints[(x,y)]

  def parseDraw(self, val):
    rawConns = val.split("-")
    conns = []

    for i in range(0, len(rawConns)-1):
      x = None
      y = None
      x2 = None
      y2 = None
      prePoint = None
      prePoint2 = None
      sucPoint = None

      if rawConns[i][0] == "(":
        x,y = self.getXY(rawConns[i])

        prePoint = self.getWayPoint(x,y)
        prePoint2 = prePoint
      elif rawConns[i][0] == "S":
        x,y = self.start.x,self.start.y

        prePoint = self.getWayPoint(x,y)
        prePoint2 = prePoint
        assert self.start.point == None
        self.start.point = prePoint
      else:
        conn,io = self.getREPredecessor(rawConns[i])
        x,y = conn.getPos(IO.INPUT, io)

        prePoint = conn.points[io]
        prePoint2 = conn.points[(io+1)%4]

      arrow = 0
      if rawConns[i+1][0] == ">":
        arrow = 15
        rawConns[i+1] = rawConns[i+1][1:]

      if rawConns[i+1][0] == "(":
        x2,y2 = self.getXY(rawConns[i+1])

        sucPoint = self.getWayPoint(x2,y2)
      else:
        conn,io = self.getRESuccessor(rawConns[i+1])
        x2,y2 = conn.getPos(IO.OUTPUT, io)

        sucPoint = conn.points[io]

      conns.append(Connection(x,y,x2,y2, arrow))
      conns[-1]

      if sucPoint:
        sucPoint.pre = prePoint2
      if prePoint:
        prePoint.suc = sucPoint

    self.allConns += conns

  def parse(self, file, window):
    for line in open(file):
      line = line.strip()

      if not line or line[0] == "#":
        continue

      vals = line.split("=")
      if len(vals) == 1: # Connection rules
        self.parseDraw(vals[0])
        continue

      # Definitions
      if vals[0] == "S":
        self.start = Signal(window, *self.getXY(vals[1]))
        window.scene.signal = self.start
        window.changedAnimationSpeed(None)
        continue

      # Labels
      if vals[0][0] == "(":
        x,y = self.getXY(vals[0])
        text = vals[1]

        window.scene.add_child(graphics.Label(text, 24, "#000", x = x, y = y,
                               alignment = pango.ALIGN_CENTER))
        continue

      self.elems[vals[0]] = RotaryElement(window.scene, *self.getXYZ(vals[1]))

    allREPoints = {}

    for elem in self.elems.itervalues():
      for i in range(0,4):
        point = elem.points[i]
        allREPoints[(point.x,point.y)] = point

    self.start.allPoints = dict(self.allPoints.items() + allREPoints.items())

    for conn in self.allConns:
      window.scene.add_child(conn)

    window.scene.add_child(self.start)
