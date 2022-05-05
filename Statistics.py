from cmd2 import style
import wx
from BaseScreen import *
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from library import User
from datetime import datetime, date, timedelta

class GraphPanel(BasePanel):
    def __init__(self, parent, *args, **kwargs):
        super(GraphPanel, self).__init__(parent, *args, **kwargs) 
        self.initUI()

    def initUI(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes.set_xlabel("Date")
        self.axes.set_ylabel("Time")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def draw(self, data):
        if(not data.empty):
            df = data.groupby('date')['time'].sum()
            x = df.index
            y = df.values   
            self.axes.plot(x, y)
        else:
            pass    
        

class Frame(BaseFrame):

    def getData(self):
        data = pd.read_csv('./data/trainingRecord.csv')
        todayDayOfWeek = datetime.today().weekday()
        firstDayOfWeek = todayDayOfWeek if todayDayOfWeek == 0 else datetime.today() - timedelta(days=todayDayOfWeek)
        lastDayofWeek = todayDayOfWeek if todayDayOfWeek == 6 else datetime.today() + timedelta(days=6-todayDayOfWeek)
        firstDayOfWeek = firstDayOfWeek.strftime("%Y-%m-%d")
        lastDayofWeek = lastDayofWeek.strftime("%Y-%m-%d")
        self.record = data[(data['user_id'] == int(User.id))&(data['date'] >= firstDayOfWeek)&(data['date'] <= lastDayofWeek)]
    
    def initUI(self):
        self.getData()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        graphPanel = GraphPanel(self)

        graphPanel.draw(self.record)
        statisInfo = BasePanel(self)
        statisInfo.SetBackgroundColour(self.main_color)

        mainSizer.Add(graphPanel, 1, wx.EXPAND)
        mainSizer.Add(statisInfo, 0, wx.EXPAND)

        InfoSizer = wx.BoxSizer(wx.VERTICAL)

        timeS = '00:00'
        timeSW = '00:00'
        if(not self.record.empty):
            data = self.record[self.record['date'] == datetime.today().strftime('%Y-%m-%d')]
            todayTime = data.groupby('date')['time'].sum().values[0]
            weekTime = self.record['time'].sum()
            minute = todayTime//60
            second = todayTime%60
            _minute = weekTime//60
            _second = weekTime%60
            timeS = ''
            timeSW = ''
            if(_minute >= 10):
                timeSW += str(_minute)
            else:
                timeSW += f'0{str(_minute)}'

            if(_second >= 10):
                timeSW += f':{str(_second)}'
            else:
                timeSW += f':0{str(_second)}'

            if(minute >= 10):
                timeS += str(minute)
            else:
                timeS += f'0{str(minute)}'

            if(second >= 10):
                timeS += f':{str(second)}'
            else:
                timeS += f':0{str(second)}' 

        listLabels = [f"Today time workout today: {timeS}", "Total calories burn today: 0",  f"Total time workout this week: {timeSW}", "Total calories burn this week: 0"]

        for label in listLabels:
            lbl = wx.StaticText(statisInfo, label = label, style = wx.ALIGN_CENTER_HORIZONTAL)
            lbl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.NORMAL))
            lbl.SetForegroundColour("White")
            InfoSizer.Add(lbl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, border = 20)


        statisInfo.SetSizer(InfoSizer)

        self.SetSizerAndFit(mainSizer)


class App(BaseApp):
    def OnInit(self):
        self.frame = Frame(None, title = 'GymFit')
        self.frame.SetIcon(wx.Icon('./assets/img/fitify.ico'))
        self.frame.Center()
        self.frame.Show()
        self.frame.getApp(self)
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()            