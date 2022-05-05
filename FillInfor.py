import wx
from BaseScreen import *
from library import User
import pandas as pd
from Home import App as HomeApp
class Frame(BaseFrame):
    sex = ''
    def __init__(self, parent, title):
        super(Frame, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(7, 10)
        panel.SetBackgroundColour((208, 241, 251))

        intro = wx.StaticText(panel, label='PERSONAL INFORMATION')
        sizer.Add(intro, pos=(0,0), flag=wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, span=(1, 10), border=15)

        intro1 = wx.StaticText(panel, label='Please provide some information to help us build the best schedule for you')
        sizer.Add(intro1, pos=(1, 0), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, span=(1, 10),
                  border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 10),flag=wx.EXPAND | wx.BOTTOM, border=10)

        text2 = wx.StaticText(panel, label="Height:")
        sizer.Add(text2, pos=(3, 0), flag=wx.LEFT | wx.TOP |wx.BOTTOM, border=5)

        self.txtheight = wx.TextCtrl(panel)
        sizer.Add(self.txtheight, pos=(3, 2), span=(1, 4), flag=wx.TOP | wx.EXPAND)

        text2_2 = wx.StaticText(panel, label="centimetres")
        sizer.Add(text2_2, pos=(3, 6), flag=wx.LEFT | wx.TOP |wx.BOTTOM , border=5)

        text3 = wx.StaticText(panel, label="Weight:")
        sizer.Add(text3, pos=(4, 0), flag=wx.LEFT | wx.TOP |wx.BOTTOM, border=5)

        self.txtweight = wx.TextCtrl(panel)
        sizer.Add(self.txtweight, pos=(4, 2), span=(1, 4), flag=wx.TOP | wx.EXPAND)

        text3_2 = wx.StaticText(panel, label="kilograms")
        sizer.Add(text3_2, pos=(4, 6), flag=wx.LEFT | wx.TOP |wx.BOTTOM , border=5)

        text4 = wx.StaticText(panel, label="Age")
        sizer.Add(text4, pos=(5, 0), flag=wx.LEFT | wx.TOP |wx.BOTTOM, border=5)

        notice = wx.StaticText(panel, label="* Please notice that your age must be older than 12 years old")
        sizer.Add(notice, pos=(6, 0), flag=wx.TOP | wx.LEFT, span=(1, 5),border=5)
        notice.SetForegroundColour("Blue")

        self.txtage = wx.TextCtrl(panel)
        sizer.Add(self.txtage, pos=(5, 2), span=(1, 4), flag=wx.TOP | wx.EXPAND)

        text4_2 = wx.StaticText(panel, label="years old")
        sizer.Add(text4_2, pos=(5, 6), flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=5)

        sb = wx.StaticBox(panel, label="Gender")

        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        boxsizer.Add(wx.RadioButton(panel, label="Male"),
                     flag=wx.LEFT | wx.TOP | wx.BOTTOM| wx.RB_GROUP, border=5)
        boxsizer.Add(wx.RadioButton(panel, label="Female"),
                     flag=wx.LEFT, border=5)
        self.Bind(wx.EVT_RADIOBUTTON, self.onCheck)             

        sizer.Add(boxsizer, pos=(7, 0), span=(1, 10),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        self.btnSubmit = wx.Button(panel, label="Continue")
        sizer.Add(self.btnSubmit, pos=(8, 3), span=(1, 1),
                  flag=wx.BOTTOM|wx.LEFT, border=10)
        self.btnSubmit.Bind(wx.EVT_BUTTON, self.onSubmit)          

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)
        sizer.Fit(self)


    def onCheck(self, evt):
        rb = evt.GetEventObject()
        self.sex = rb.GetLabel()
        

    def onSubmit(self, evt):
        height = self.txtheight.GetValue().strip()
        weight = self.txtweight.GetValue().strip()
        age = self.txtage.GetValue().strip()
        inputs = [height, weight, age]
        fields = ['height', 'weight', 'age']
        info = pd.read_csv('./data/users_info.csv', dtype=str)
        res = {'id': len(info)}

        for field, input in zip(fields, inputs):
            if(input == ''):
                box = wx.MessageDialog(None, f'Please fill your {field}', 'Warning', wx.OK|wx.ICON_WARNING)
                box.ShowModal() 
                break
            else:  
                try:  
                    try:
                        temp = int(input)
                    except:
                        try:
                            if(field == 'age'):
                                raise
                            temp = float(input)
                        except:
                            box = wx.MessageDialog(None, f'Your {field} must be number', 'Warning', wx.OK|wx.ICON_WARNING)
                            box.ShowModal()   
                            raise ValueError("Invalid input")
                    if(field == 'height'):
                        if(not (temp > 120 and temp < 200)):
                            box = wx.MessageDialog(None, f'Your {field} must greater than 120 and lower than 200', 'Warning', wx.OK|wx.ICON_WARNING)
                            box.ShowModal()       
                            raise ValueError("Invalid input")
                    elif(field == 'weight'):
                        if(not (temp > 50 and temp < 150)):   
                            box = wx.MessageDialog(None, f'Your {field} must greater than 50 and lower than 150', 'Warning', wx.OK|wx.ICON_WARNING)
                            box.ShowModal()       
                            raise ValueError("Invalid input")  
                    elif(field == 'age'):
                        if(not (temp > 12 and temp < 60)):   
                            box = wx.MessageDialog(None, f'Your {field} must greater than 12 and lower than 60', 'Warning', wx.OK|wx.ICON_WARNING)
                            box.ShowModal()       
                            raise ValueError("Invalid input")    
                    res[field] = temp
                except Exception as e:
                    raise e        
        else:
            if(self.sex != ''):
                res['sex'] = self.sex
                res['user_id'] = User.id
                info = info.append(res , ignore_index =True)
                info.to_csv('./data/users_info.csv', index = False)
                self.Close()
                HomeApp.OnInit(self.app)
            else:
                box = wx.MessageDialog(None, "Please choose your sex before continuing", 'Warning', wx.OK|wx.ICON_WARNING)
                box.ShowModal()          

        

      
         
    
class App(BaseApp):
    def OnInit(self):
        self.frame = Frame(None, title = 'GymFit')
        self.frame.SetIcon(wx.Icon('./assets/img/fitify.ico'))
        self.frame.Center()
        self.frame.Show()
        self.frame.getApp(self)
        return True
def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()