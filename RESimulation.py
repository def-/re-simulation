#!/usr/bin/env python
# - coding: utf-8 -

import gtk
import cairo
import pango

from RotaryElement import *
from Connection import *
from Signal import *
from Scene import *
from Parser import *

class ReWindow:
  def __init__(self):
    self.play = False
    self.file = None

    self.builder = gtk.Builder()
    self.builder.add_from_file("re.ui")
    self.builder.connect_signals(self)

    self.window = self.builder.get_object("reWindow")

    simulationBox = self.builder.get_object("simulationBox")

    self.scene = Scene()

    simulationBox.pack_start(self.scene, True, True, 0)

    self.window.connect('key-press-event', self.catchButton)
    self.window.connect("delete_event", lambda *args: gtk.main_quit())
    self.window.show_all()

  def catchButton(self, window, event):
    print event.keyval

    if event.keyval == 65365:
      self.clickedStepBack(None)
    if event.keyval == 65366:
      self.clickedStepForward(None)
    if event.keyval == 46:
      self.clickedPlayPause(None)

  def clickedRewind(self, widget, data=None):
    print "rewind clicked"
    self.reset()

  def clickedStepForward(self, widget, data=None):
    print "forward clicked"
    if self.scene.signal:
      self.scene.signal.moveForward()

  def clickedStepBack(self, widget, data=None):
    print "back clicked"
    if self.scene.signal:
      self.scene.signal.moveBackward()

  def clickedPlayPause(self, widget, data=None):
    if not self.scene.signal:
      return

    if self.play:
      print "pause clicked"
      self.play = False
      labelText = "gtk-media-play"

      self.builder.get_object("playPauseButton").set_label(labelText)

      self.scene.signal.pause()
    else:
      print "play clicked"
      self.play = True
      labelText = "gtk-media-pause"

      self.builder.get_object("playPauseButton").set_label(labelText)

      self.scene.signal.playForward()

  def changedAnimationSpeed(self, widget, data=None):
    print "animation speed changed"
    if self.scene.signal:
      adj = self.builder.get_object("animationSpeedAdjustment")
      self.scene.signal.speed = adj.value
      self.scene.durationRotation = 50 / adj.value

  def clickedZoomIn(self, widget, data=None):
    self.scene.scaleFactor *= 1.1
    self.scene.redraw()
    print "zoom in clicked"

  def clickedZoomOut(self, widget, data=None):
    self.scene.scaleFactor *= 1./1.1
    self.scene.redraw()
    print "zoom out clicked"

  def clickedLeft(self, widget, data=None):
    self.scene.shiftX += 50 / self.scene.scaleFactor
    self.scene.redraw()
    print "left clicked"

  def clickedRight(self, widget, data=None):
    self.scene.shiftX -= 50 / self.scene.scaleFactor
    self.scene.redraw()
    print "right clicked"

  def clickedUp(self, widget, data=None):
    self.scene.shiftY += 50 / self.scene.scaleFactor
    self.scene.redraw()
    print "up clicked"

  def clickedDown(self, widget, data=None):
    self.scene.shiftY -= 50 / self.scene.scaleFactor
    self.scene.redraw()
    print "down clicked"

  def reset(self):
    if self.play:
      self.clickedPlayPause(None, None)

    self.scene.clear()

    if (self.file):
      parser = Parser()
      parser.parse(self.file, self)

    self.scene.redraw()

  def openFile(self, object):
    print "open"
    dialog = gtk.FileChooserDialog(None,
                                   self.window,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)

    filter = gtk.FileFilter()
    filter.set_name("Rotary Element Simulations")
    filter.add_pattern("*.res")
    dialog.add_filter(filter)

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        self.file = dialog.get_filename()
        self.reset()
    elif response == gtk.RESPONSE_CANCEL:
        print 'Closed, no files selected'
    dialog.destroy()

  def exportFile(self, object):
    print "export"
    dialog = gtk.FileChooserDialog(None,
                                   self.window,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)

    filter = gtk.FileFilter()
    filter.set_name("Scalabe Vector Graphics")
    filter.add_pattern("*.svg")
    dialog.add_filter(filter)

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
      self.scene.exportSVG(dialog.get_filename())
    elif response == gtk.RESPONSE_CANCEL:
      print 'Closed, no files selected'
    dialog.destroy()

if __name__ == '__main__':
  window = ReWindow()
  gtk.main()
