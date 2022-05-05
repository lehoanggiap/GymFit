import wx
from library import BitmapImage, User
from BaseScreen import *
from Home import App as HomeApp
import pandas as pd
from FillInfor import main

class Frame(BaseFrame):
    main_color = '#194270'
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__( *args, **kwargs)

    def initUI(self):
        self.setBackGroundImage()
        loginSizer = wx.BoxSizer(wx.VERTICAL)

        loginPanel = BasePanel(self)

        loginSizer.AddStretchSpacer(1)
        loginSizer.Add(loginPanel, 1, wx.ALIGN_CENTER)
        loginSizer.AddStretchSpacer(1)

        formWrapper = wx.BoxSizer(wx.VERTICAL)

        formSizer = wx.GridBagSizer(5, 12)
        lblTitle = wx.StaticText(loginPanel, label="LOGIN HERE")
        lblTitle.SetFont(wx.Font(18, wx.FONTFAMILY_MODERN, wx.BOLD, wx.NORMAL))
        lblTitle.SetForegroundColour(self.main_color)
        formSizer.Add(lblTitle, pos = (0,0), span = (1,12), flag = wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, border = 20)

        lblUserName = wx.StaticText(loginPanel, label="Username:")
        formSizer.Add(lblUserName, pos = (1,0), flag =wx.LEFT | wx.TOP |wx.BOTTOM, border=5)


        self.txtUserName = wx.TextCtrl(loginPanel)
        formSizer.Add(self.txtUserName, pos=(1, 2), span=(1, 10), flag= wx.TOP | wx.EXPAND)

        lblPass = wx.StaticText(loginPanel, label="Password:")
        formSizer.Add(lblPass, pos = (3,0), flag =wx.LEFT | wx.TOP |wx.BOTTOM, border=5)

        self.txtPass = wx.TextCtrl(loginPanel, style = wx.TE_PASSWORD)
        formSizer.Add(self.txtPass, pos=(3, 2), span=(1, 10), flag= wx.TOP | wx.EXPAND)

        btnLogin = wx.Button(loginPanel, label="Login")
        formSizer.Add(btnLogin, pos = (4,0), span = (1, 12), flag = wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, border = 20)
        btnLogin.Bind(wx.EVT_BUTTON, self.onLogin)

        questionSizer = wx.BoxSizer(wx.HORIZONTAL)
        formSizer.Add(questionSizer, pos = (5,0), span = (1,12), flag = wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, border = 15)

        lblQuestion = wx.StaticText(loginPanel, label="New user? ")
        questionSizer.Add(lblQuestion, 0, wx.ALIGN_CENTER)

        self.btnRegister = wx.Button(loginPanel, label="Register")
        questionSizer.Add(self.btnRegister, 0, wx.ALIGN_CENTER)

        self.btnRegister.Bind(wx.EVT_BUTTON, self.onRegister)

        formWrapper.Add(formSizer, 1, wx.EXPAND|wx.ALL, 10)

        loginPanel.SetSizer(formWrapper)
        self.SetSizer(loginSizer)

    def onLogin(self, evt):
        name = self.txtUserName.GetValue()
        pw = self.txtPass.GetValue()

        if(name == ''):
            box = wx.MessageDialog(None, 'Please fill your username', 'Warning', wx.OK|wx.ICON_WARNING)
            box.ShowModal()
        elif(pw == ''):
            box = wx.MessageDialog(None, 'Please fill your password', 'Warning', wx.OK|wx.ICON_WARNING)
            box.ShowModal()
        else:     
            users = pd.read_csv('./data/users.csv', dtype=str)
            user = users[(users['username'] == name) & (users['password'] == pw)]
            if(not user.empty):
                info = pd.read_csv('./data/users_info.csv', dtype=str)
                User.id = user["id"].values[0]
                User.username = user["username"].values[0]
                infoUser = info[info['user_id'] == User.id]
                self.Close()
                if(infoUser.empty):
                    main()
                else:
                    HomeApp.OnInit(self.app)

            else:
               box = wx.MessageDialog(None, 'Username or password is incorrect', 'Warning', wx.OK|wx.ICON_WARNING)
               box.ShowModal() 

    def onRegister(self, evt):
        name = self.txtUserName.GetValue()
        pw = self.txtPass.GetValue()

        if(name == ''):
            box = wx.MessageDialog(None, 'Please fill your username', 'Warning', wx.OK|wx.ICON_WARNING)
            box.ShowModal()
        elif(pw == ''):
            box = wx.MessageDialog(None, 'Please fill your password', 'Warning', wx.OK|wx.ICON_WARNING)
            box.ShowModal()
        else:     
            users = pd.read_csv('./data/users.csv')
            user = users[users['username'] == name]
            if(user.empty):
                users = users.append({"id": len(users), "username": name, "password": str(pw)}, ignore_index =True)
                users.to_csv('./data/users.csv', index = False)
                User.id = len(users)
                User.username = name
                self.Close()
                main()
            else:
               box = wx.MessageDialog(None, 'Account is already registerd', 'Warning', wx.OK|wx.ICON_WARNING)
               box.ShowModal() 

    def setBackGroundImage(self):
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground) 

    def OnEraseBackground(self, evt):
        size = self.GetSize()
        width = size[0]
        height = size[1]
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = BitmapImage.create('./assets/img/background.jpg', width, height)
        dc.DrawBitmap(bmp, 0, 0)        
        

class App(BaseApp):
    def OnInit(self):
        self.frame = Frame(None, title = 'GymFit', size = (800, 500), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.frame.SetIcon(wx.Icon('./assets/img/fitify.ico'))
        self.frame.Center()
        self.frame.Show()
        self.frame.getApp(self)
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()