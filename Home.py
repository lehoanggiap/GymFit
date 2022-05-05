import wx
from BaseScreen import *
from library import BitmapImage,User,setInterval
from Statistics import App as StatisticsApp
import pandas as pd
from threading import Timer
import threading
from datetime import datetime


class HomeMenu(wx.Menu):
    def __init__(self, parentFrame):
        super(HomeMenu, self).__init__()
        self.OnInit()
        self.parentFrame = parentFrame

    def OnInit(self):
        logOutItem = wx.MenuItem(parentMenu=self, id = wx.ID_NEW, text = "&Log out")
        # self.Append(logOutItem) 
        self.Bind(wx.EVT_MENU, handler = self.onLogOut, source = logOutItem)

        exitItem = wx.MenuItem(parentMenu=self, id = wx.ID_EXIT, text = "&Quit")
        self.Append(exitItem) 
        self.Bind(wx.EVT_MENU, handler = self.onExit, source = exitItem)


    def onLogOut(self, evt):
        self.parentFrame.Close()  
        # LoginApp.OnInit(self.parentFrame.app) 

    def onExit(self, evt):
        self.parentFrame.Close()  


class PageMenu(HomeMenu):
    def OnInit(self):
        resultItem = wx.MenuItem(parentMenu = self, id = wx.ID_OPEN, text = "&Training statistics")
        self.Append(resultItem)
        self.Bind(wx.EVT_MENU, handler = self.onOpen, source = resultItem)

    def onOpen(self, evt):
        StatisticsApp.OnInit(self.parentFrame.app)

class Frame(BaseFrame):
    currentIndex = 0
    currentTime = 0
    trainingTime = 0
    def getData(self):
        info = pd.read_csv('./data/users_info.csv')
        infoUser = info[info['user_id'] == int(User.id)]
        height = (infoUser['height'].values[0])/100
        weight = infoUser['weight'].values[0]
        age = infoUser['age'].values[0]
        _BMIv = weight/(height*height)
        data = pd.read_csv('./data/exercises.csv')
        exercisesData = data[(data['minBMI'] <= _BMIv)&(data['maxBMI'] >= _BMIv)&(data['minage'] <= age)&(data['maxage']>= age)]

        self.dictExercises = []
        self.listExercises = []
        self.totalTime = 0
        for index, row in exercisesData.iterrows():
            self.totalTime += row['time']
            self.dictExercises.append({'name': row['exercise'], 'time': row['time']})
            self.listExercises.append(row['exercise'] + ": " + str(row['time']))

        
    def initUI(self):
        self.getData()

        menuBar = wx.MenuBar()
        homeMenu = HomeMenu(parentFrame = self)
        menuBar.Append(homeMenu, '&Home')
        pageMenu = PageMenu(parentFrame = self)
        menuBar.Append(pageMenu, '&Page')


        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        exercises = BasePanel(self)
        exercises.SetBackgroundColour(self.main_color)
        mainSizer.Add(exercises, 1 , wx.EXPAND)

        #exercises Sizer
        minute = self.totalTime//60
        second = self.totalTime%60
        timeS = ''
        if(minute >= 10):
            timeS += str(minute)
        else:
            timeS += f'0{str(minute)}'

        if(second >= 10):
            timeS += f':{str(second)}'
        else:
            timeS += f':0{str(second)}'    

        exsSizer = wx.BoxSizer(wx.VERTICAL)
        lblTotalTime = wx.StaticText(exercises, label = f"Total time: {timeS}", style = wx.ALIGN_CENTER_HORIZONTAL)
        lblTotalTime.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.NORMAL))
        lblTotalTime.SetForegroundColour("White")
        exsSizer.Add(lblTotalTime, 0, wx.EXPAND|wx.TOP, border = 30)


        self.listboxExs = wx.ListBox(exercises, -1, choices = self.listExercises, style = wx.LB_NEEDED_SB|wx.LB_SORT)
        self.listboxExs.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.NORMAL))
        exsSizer.Add(self.listboxExs, 0, wx.ALL|wx.EXPAND, border = 40)

        self.btnStart = wx.ToggleButton(exercises, label = 'Start training')
        exsSizer.Add(self.btnStart, 0, wx.CENTER|wx.TOP, border = 30)
        self.btnStart.Bind(wx.EVT_TOGGLEBUTTON, self.onStartTraining)

        activeEx = BasePanel(self)
        activeEx.SetBackgroundColour("White")
        mainSizer.Add(activeEx, 1, wx.EXPAND)

        
        #active exercise Sizer
        activeSizer = wx.BoxSizer(wx.VERTICAL)

        self.lblActiveName = wx.StaticText(activeEx, label = f"{self.dictExercises[self.currentIndex]['name']}", style = wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.lblActiveName.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.NORMAL))
        self.lblActiveName.SetForegroundColour(self.main_color)
        activeSizer.Add(self.lblActiveName, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, border = 20)

        bmp = BitmapImage.create('./assets/img/stretching.jpg', 300, 200)
        activeImage = wx.StaticBitmap(activeEx, -1, bmp)
        activeSizer.Add(activeImage, 0 , wx.EXPAND)

        lblIntro = wx.StaticText(activeEx, label = "This a brief introduction for this exercise", style = wx.ALIGN_CENTER_HORIZONTAL)
        lblIntro.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
        activeSizer.Add(lblIntro, 0 , wx.EXPAND|wx.TOP, border = 20)

        activeTimeS = ''
        acMinute = (self.dictExercises[self.currentIndex]['time'])//60
        acSecond = (self.dictExercises[self.currentIndex]['time'])%60
        if(acMinute >= 10):
            activeTimeS += str(acMinute)
        else:
            activeTimeS += f'0{str(acMinute)}'

        if(acSecond >= 10):
            activeTimeS += f':{str(acSecond)}'
        else:
            activeTimeS += f':0{str(acSecond)}'  


        self.lblActiveTime = wx.StaticText(activeEx, label = activeTimeS, style = wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.lblActiveTime.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
        activeSizer.Add(self.lblActiveTime, 0 , wx.EXPAND|wx.TOP, border = 20)

        lblActiveCalories = wx.StaticText(activeEx, label = "Calories burn: 0", style = wx.ALIGN_CENTER_HORIZONTAL)
        lblActiveCalories.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
        activeSizer.Add(lblActiveCalories, 0 , wx.EXPAND|wx.TOP, border = 20)

        btnBmp = BitmapImage.create('./assets/img/pause-icon.png', 30, 30)
        btnToggle = wx.BitmapButton(activeEx, bitmap = btnBmp, size = (30, 30), style = wx.NO_BORDER)
        btnToggle.SetBackgroundColour("White")
        activeSizer.Add(btnToggle, 0 , wx.CENTER|wx.TOP, border = 30)


        exercises.SetSizer(exsSizer)
        activeEx.SetSizer(activeSizer)
        self.SetMenuBar(menuBar)
        self.SetSizer(mainSizer) 

    def updateTime(self):
        self.currentTime -=1
        if(self.currentTime < 10):
            self.lblActiveTime.SetLabel(f'00:0{self.currentTime}')   
        else:
            self.lblActiveTime.SetLabel(f'00:{self.currentTime}')    

    def updateTimeTrainings(self):
        self.trainingTime += self.dictExercises[self.currentIndex]['time']
        self.currentIndex += 1 
        if(self.currentIndex == len(self.dictExercises)):
            record = pd.read_csv('./data/trainingRecord.csv')
            today = datetime.today().strftime('%Y-%m-%d')
            data = {"id": len(record), "date": today, "time": self.trainingTime, "user_id": User.id}
            record = record.append(data, ignore_index =True)
            record.to_csv('./data/trainingRecord.csv', index = False)
            box = wx.MessageDialog(None, 'Your training is finished', 'Alert', wx.OK|wx.ICON_INFORMATION)
            box.ShowModal()
        else: threading.Timer(15, self.training).start()

    def startTimer(self):
        inter = setInterval(1, self.updateTime)
        stopTime = self.dictExercises[self.currentIndex]['time']
        t=threading.Timer(stopTime, inter.cancel)
        threading.Timer(stopTime, self.updateTimeTrainings).start()
        t.start()

    def training(self):
        try:
            self.listboxExs.SetSelection(self.currentIndex)
            self.lblActiveName.SetLabel(f"{self.dictExercises[self.currentIndex]['name']}")
            activeTimeS = ''
            acMinute = (self.dictExercises[self.currentIndex]['time'])//60
            acSecond = (self.dictExercises[self.currentIndex]['time'])%60
            if(acMinute >= 10):
                activeTimeS += str(acMinute)
            else:
                activeTimeS += f'0{str(acMinute)}'

            if(acSecond >= 10):
                activeTimeS += f':{str(acSecond)}'
            else:
                activeTimeS += f':0{str(acSecond)}' 
            self.lblActiveTime.SetLabel(activeTimeS)   
            self.currentTime = acSecond

            self.startTimer()
        except:
            raise


    def onStartTraining(self, evt):
        state = evt.GetEventObject().GetValue()
        if state == True:
            # self.btnStart.SetLabel('Stop training')
            self.training()
            self.btnStart.Hide()
        else:
            # self.btnStart.SetLabel('Start training')
            pass
 

class App(BaseApp):    
    def OnInit(self):
        self.frame = Frame(None, title = 'GymFit', size = (1000, 700))
        self.frame.SetIcon(wx.Icon('./assets/img/fitify.ico'))
        self.frame.Center()
        self.frame.Show()
        self.frame.getApp(self)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()




