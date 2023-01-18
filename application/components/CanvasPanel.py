import wx
import pandas as pd
import matplotlib
from numpy import arange, sin, pi
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import seaborn as sns
import matplotlib.pyplot as plt

class CanvasPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)

    # Simplified init method.
    self.CreateCtrls()
    self.DoLayout()

  def CreateCtrls(self):
    self.figure = Figure(figsize=(4, 3))
    self.axes = self.figure.add_subplot(111)

    #------------

    self.canvas = FigureCanvas(self, -1, self.figure)

    #------------

    # self.toolbar = NavigationToolbar2Wx(self.canvas)
    # self.toolbar.Realize()


  def DoLayout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP)
    self.SetSizer(sizer)
    self.Fit()

  def SetGraph(self, func):
    self.graph = func

  def DrawCleanliness(self, cleanliness):
    mask, labels = cleanliness
    dirty = mask.value_counts()
    if dirty.count() > 0:
      axesLabels = list(labels)
      self.axes.plot(1, 0)
      self.axes.clear()
      self.axes.pie(dirty, labels=axesLabels, autopct='%.2f')
      self.figure.suptitle("Comments related to cleanliness")
      self.canvas.draw()

  def DrawAnalysisProperties(self, analysisProperties):
    if analysisProperties.count() > 0:
      self.axes.clear()
      self.axes.pie(analysisProperties, labels = analysisProperties.index, autopct='%.2f')
      circle = plt.Circle((0,0), 0.3, color='white')
      self.axes.add_artist(circle)
      self.figure.suptitle("Cancellation Policy")
      self.canvas.draw()

  def DrawPriceChart(self, listingSummary):
     if listingSummary.shape[0] > 0:
      sns.boxplot(x="neighbourhood", y="price", data=listingSummary, ax=self.axes)
      self.figure.suptitle("Locations and the Price")
      self.figure.tight_layout()
      self.axes.set_yscale('log')
      self.canvas.draw()
