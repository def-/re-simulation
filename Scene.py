from lib import graphics
import gtk
import rsvg
import cairo
import pango
import pangocairo

class Scene(graphics.Scene):
  def __init__(self):
    graphics.Scene.__init__(self, background_color="#fff", scale=False)
    self.connect("on-enter-frame", self.on_enter_frame)

    #self.mouse_cursor=gtk.gdk.LEFT_PTR
    self.durationRotation = 1
    self.scaleFactor = 1
    self.shiftX = 0
    self.shiftY = 0

    self.fileSVG = None
    self.disconnectHandler = None
    self.signal = None

  def exportSVG(self, file):
    self.disconnectHandler = self.connect("on-finish-frame", self.doExportSVG)
    self.fileSVG = file

  def on_enter_frame(self, scene, context):
    self.matrix = cairo.Matrix(self.scaleFactor, 0, 0, self.scaleFactor, self.shiftX * self.scaleFactor, self.shiftY * self.scaleFactor)
    self.inverseMatrix = cairo.Matrix() * self.matrix
    self.inverseMatrix.invert()
    context.set_matrix(self.matrix)

  def doExportSVG(self, scene, context):
    self.disconnect(self.disconnectHandler)

    surface = context.get_target()

    svgSurface = cairo.SVGSurface(file(self.fileSVG, "w"),
                                  5000,
                                  5000) # TODO: Fix me
    svgContext = cairo.Context(svgSurface)
    pangoContext = pangocairo.CairoContext(svgContext)

    for sprite in self.all_visible_sprites():
      sprite._draw(pangoContext)

    svgSurface.finish()

  def input(self, inp):
    self.thing.input(inp)

  def test(self):
    self.signal.move(self.conn1)
