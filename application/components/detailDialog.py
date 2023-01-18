import wx

class Dialog(wx.Dialog):
  def __init__(self, data=None, *args, **kwds):
    kwds["style"] = wx.DEFAULT_DIALOG_STYLE
    wx.Dialog.__init__(self, *args, **kwds)
    self.SetSize((630, 560))
    self.data = data

    fieldsToDisplay = [
      {
        'label': 'Name',
        'key': 'name',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Description',
        'key': 'description',
        'size': (300,200),
        'isLongText': True,
      },
      {
        'label': 'Host',
        'key': 'host_name',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Street',
        'key': 'street',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Room Type',
        'key': 'room_type',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Price',
        'key': 'price',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Cleaning Fee',
        'key': 'cleaning_fee',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Min. Night',
        'key': 'minimum_nights',
        'size': (300,0),
        'isLongText': False,
      },
      {
        'label': 'Amenities',
        'key': 'amenities',
        'size': (300,50),
        'isLongText': True,
      },
      {
        'label': 'Rating (out of 100)',
        'key': 'review_scores_rating',
        'size': (300,0),
        'isLongText': False,
      },
    ]

    self.fields = []
    items = {}

    for field in fieldsToDisplay:
      items['label_{}'.format(field['key'])] = wx.StaticText(self, -1, " {} :".format(field['label']))
      if field['isLongText']:
        items['value_{}'.format(field['key'])] = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
      else:
        items['value_{}'.format(field['key'])] = wx.TextCtrl(self, style=wx.TE_READONLY)
      items['value_{}'.format(field['key'])].SetValue(self.data[field['key']].astype("string").values[0])

      self.fields.append({
        'label': items['label_{}'.format(field['key'])],
        'value': items['value_{}'.format(field['key'])]
      })

    self.doLayout()

  def doLayout(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    hSizers = []

    for field in self.fields:
      newHSizer = wx.BoxSizer(wx.HORIZONTAL)
      newHSizer.Add(field['label'], 1, wx.EXPAND, 1)
      newHSizer.Add(field['value'], 1, wx.EXPAND, 1)
      hSizers.append(newHSizer)

    for sizer in hSizers:
      mainSizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 1)
  
    self.SetSizer(mainSizer)
    self.Layout()