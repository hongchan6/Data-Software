import wx
import wx.adv
import time
from data import getSuburb, getPropertyList, viewPropertyDetail, analysisCleanliness, analysisProperties, displayPriceDistribution
from components.datatable import DataTable
from components.detailDialog import Dialog
from components.CanvasPanel import CanvasPanel

suburbOptions = getSuburb()

class appGui(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title)
    self.parent = parent
    self.setProperties()
    self.initialize()
    self.CenterOnScreen(wx.BOTH)
    self.Layout()
    self.Show(True)

  def setProperties(self):
    self.SetSize((1200, 800))
    self.SetMinSize((1200, 800))
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = wx.Panel(self)
    self.panel.SetSizerAndFit(self.sizer)
    self.grid = wx.grid.Grid(self.panel, -1)
    self.current = 0

  def initialize(self):
    self.state = { 'filter': '', 'suburb': '', 'dateFrom': '', 'dateTo': '' }
    self.prevState = self.state.copy()
    self.searchFields()
    df = getPropertyList(self.state, self.prevState)
    self.cleanliness = analysisCleanliness(df)
    self.analysisProperties = analysisProperties(df)
    self.listingSummary = displayPriceDistribution(df)
    self.rowCount = df.shape[0]
    self.table = DataTable(df[['id', 'name', 'neighbourhood']][0:20])
    self.df = df
    self.drawCanvas()
    self.resultList()
    self.prevState = self.state.copy()

  def setState(self, field, value):
    self.state[field] = value

  # Top Search Inputs UI
  def searchFields(self):
    hbox = wx.BoxSizer(wx.HORIZONTAL) 

    # add text input
    hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
    label1 = wx.StaticText(self.panel, -1, "Keywords: ") 
    txtbox1 = wx.TextCtrl(self.panel) 
    self.Bind(wx.EVT_TEXT,self.OnKeyTyped, txtbox1) 

    hbox1.Add(label1, 1, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox1.Add(txtbox1, 1,wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 

    hbox.Add(hbox1) 

    # add suburb select
    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    label2 = wx.StaticText(self.panel, -1, "Suburbs: ") 
    suburbSelect = wx.Choice(self.panel, choices=suburbOptions)
    self.Bind(wx.EVT_CHOICE, self.OnSelect, suburbSelect)

    hbox2.Add(label2, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox2.Add(suburbSelect,1,wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 

    hbox.Add(hbox2) 

    # add date picker
    hbox3 = wx.BoxSizer(wx.HORIZONTAL)
  
    label = wx.StaticText(self.panel, -1, "Date: ") 
    dashLabel = wx.StaticText(self.panel, -1, " - ") 
    dateFrom = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_SPIN)
    dateTo = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_SPIN)
    initialDate = wx.DateTime(7,11,2018)
    dateFrom.SetValue(initialDate)
    
    # Set default Search Values
    defaultSurburb = suburbSelect.GetString(0)
    self.setState('suburb', defaultSurburb)
    defaultDateFrom = initialDate.Format("%Y-%m-%d")
    defaultDateTo = dateTo.GetValue().Format("%Y-%m-%d")
    self.setState('dateFrom', defaultDateFrom)
    self.setState('dateTo', defaultDateTo)
    # self.prevState = self.state.copy()

    hbox3.Add(label, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox3.Add(dateFrom, 1, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox3.Add(dashLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox3.Add(dateTo, 1, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    self.Bind(wx.adv.EVT_DATE_CHANGED, self.onPickDateFrom, dateFrom)
    self.Bind(wx.adv.EVT_DATE_CHANGED, self.onPickDateTo, dateTo)
    hbox.Add(hbox3) 

    # add button
    hbox4 = wx.BoxSizer(wx.HORIZONTAL)
    searchBtn = wx.Button(self.panel, label="Search")
    self.Bind(wx.EVT_BUTTON, self.onSearch, searchBtn)
    hbox4.Add(searchBtn, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox.Add(hbox4)

    self.sizer.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)

  # Main function to update UI upon data changes
  def refresh_data(self):
    df = getPropertyList(self.state, self.prevState)
    self.cleanliness = analysisCleanliness(df)
    self.analysisProperties = analysisProperties(df)
    self.listingSummary = displayPriceDistribution(df)
    self.canvas.DrawCleanliness(self.cleanliness)
    self.canvas2.DrawAnalysisProperties(self.analysisProperties)
    self.canvas3.DrawPriceChart(self.listingSummary)
    self.rowCount = df.shape[0]
    self.totalPage = self.rowCount // 20
    self.currentPage = self.current // 20 if self.current // 20 + 1 > self.totalPage else self.current // 20 + 1
    df = df[['id', 'name', 'neighbourhood']][self.current: self.current+20]
    self.df = df
    rows = 20 if self.rowCount > 20 or self.rowCount == 0 else self.rowCount
    self.totalLabel.SetLabel("Page: {} / {} Total: {}".format(self.currentPage, self.totalPage, self.rowCount)) 
    # Clear / Update the table list data
    for i in range(0, rows):
      for j in range(0, 3):
        if (self.rowCount == 0):
          self.grid.SetCellValue(i, j + 1, '')
        else:
          cell = df.iloc[i]
          self.grid.SetCellValue(i, j + 1, str(cell[j]))
    if rows < 20:
      for i in range(rows, 20):
        for j in range(0, 3):
          self.grid.SetCellValue(i, j + 1, '')

  # Draw table list UI
  def resultList(self):
    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    hbox3 = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(self.panel, -1, "List of matched properties") 

    self.grid.SetTable(self.table, takeOwnership=True)
    self.grid.HideCol(col=0)
    self.grid.AutoSizeColumns()
    self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onSelectRow, self.grid)

    hbox1.Add(label,1,wx.EXPAND)
    hbox2.Add(self.grid, 1, wx.EXPAND)

    prevBtn = wx.Button(self.panel, label="Prev")
    nextBtn = wx.Button(self.panel, label="Next")
    self.Bind(wx.EVT_BUTTON, self.onPrev, prevBtn)
    self.Bind(wx.EVT_BUTTON, self.onNext, nextBtn)

    self.totalPage = self.rowCount // 20
    self.currentPage = self.current // 20 if self.current // 20 + 1 > self.totalPage else self.current // 20 + 1
    self.totalLabel = wx.StaticText(self.panel, -1, "Page: {} / {} Total: {}".format(self.currentPage, self.totalPage, self.rowCount)) 

    hbox3.Add(prevBtn, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox3.Add(self.totalLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 
    hbox3.Add(nextBtn, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL,5) 

    self.sizer.Add(hbox3, flag=wx.EXPAND | wx.ALL, border=5)
    self.sizer.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=5)
    self.sizer.Add(hbox2, flag=wx.EXPAND | wx.ALL, border=5)
  
  def drawCanvas(self):
    hbox = wx.BoxSizer(wx.HORIZONTAL)

    vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.canvas = CanvasPanel(self.panel)
    # self.canvas.SetGraph(analysisCleanliness)
    self.canvas.DrawCleanliness(self.cleanliness)
    vbox1.Add(self.canvas,1,wx.EXPAND)
   
    vbox2 = wx.BoxSizer(wx.VERTICAL)
    self.canvas2 = CanvasPanel(self.panel)
    self.canvas2.DrawAnalysisProperties(self.analysisProperties)
    vbox2.Add(self.canvas2,1,wx.EXPAND)
    
    vbox3 = wx.BoxSizer(wx.VERTICAL)
    self.canvas3 = CanvasPanel(self.panel)
    self.canvas3.DrawPriceChart(self.listingSummary)
    vbox3.Add(self.canvas3,1,wx.EXPAND)

    hbox.Add(vbox1,1,wx.EXPAND)
    hbox.Add(vbox2,1,wx.EXPAND)
    hbox.Add(vbox3,1,wx.EXPAND)
  
    self.sizer.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)

  def onSearch(self, event):
    self.refresh_data()
    self.prevState = self.state.copy()
  
  def onNext(self, event):
    next = self.current + 20
    if (next <= self.rowCount):
      self.current = next
      self.refresh_data()
      self.prevState = self.state.copy()
  
  def onPrev(self, event):
    prev = self.current -20
    if (prev >= 0):
      self.current = prev
      self.refresh_data()
      self.prevState = self.state.copy()

  def onPickDateFrom(self, event):
    sel_date = event.GetDate()
    self.setState('dateFrom', sel_date.Format("%Y-%m-%d"))

  def onPickDateTo(self, event):
    sel_date = event.GetDate()
    self.setState('dateTo', sel_date.Format("%Y-%m-%d"))

  def OnKeyTyped(self, event):
    txt = event.GetString()
    self.setState('filter', txt)

  def OnSelect(self, event):
    val = event.GetString()
    self.setState('suburb', val)

  def onSelectRow(self, event):
    rowId = event.GetRow()
    selectedId = self.df.iloc[rowId]['id']
    self.selectedProperty = viewPropertyDetail(selectedId)
    Dialog(self.selectedProperty, self).ShowModal()

# if __name__ == '__main__':
#   app = wx.App()
#   frame = appGui(None, -1, 'My application')
#   app.MainLoop()
