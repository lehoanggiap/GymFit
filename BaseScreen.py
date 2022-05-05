import wx

class BasePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(BasePanel, self).__init__(parent, *args, **kwargs)   


class BaseFrame(wx.Frame):
    main_color = '#194270'
    def __init__(self, *args, **kwargs):
        super(BaseFrame, self).__init__( *args, **kwargs)

        self.initUI()

    def initUI(self):
        pass

    def getApp(self, app):
        self.app = app 

class BaseApp(wx.App):
    def OnInit(self):
        pass
        
            
    