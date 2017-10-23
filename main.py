# coding: utf-8
import wx
import time
import requests
import psutil
import re
import sys

 
class Fader(wx.Frame):
 
    def __init__(self):
        global label_fan
        no_sys_menu = wx.CAPTION
        wx.Frame.__init__(self, None, title='WidgetMonitor', size=(200, 220), style=no_sys_menu)
        self.amount = 200
        self.delta = 5
        #self.ToggleWindowStyle(wx.STAY_ON_TOP)
        style = wx.TRANSPARENT_WINDOW if sys.platform.lower() == 'win32' else 0
        panel = wx.Panel(self, wx.ID_ANY, style=style)
        if panel.CanSetTransparent:
            panel.SetTransparent(100)
 
        self.SetTransparent(self.amount)
        self.Maximize(False)
 
        ## ------- Fader Timer -------- ##
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        self.toggleBtn = wx.Button(panel, wx.ID_ANY, "Start", size=(50,50), pos=(75,0))
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)

        self.label = wx.StaticText(panel, wx.ID_ANY, label=time.ctime(), pos=(0,50), size=(200,20), style=wx.ALIGN_CENTRE)
        self.labelIpEXT = wx.StaticText(panel, wx.ID_ANY, label="Your ip Externe : 0.0.0.0", pos=(0,75), size=(200,20), style=wx.ALIGN_CENTRE)
        self.labeltemp0 = wx.StaticText(panel, wx.ID_ANY, label="temp0 : 0°C", pos=(0,100), size=(200,20), style=wx.ALIGN_CENTRE)

        correct = 0
        label_fan = {}
        data_fans = psutil.sensors_fans()
        for i in range(0, 9):
            data2 = re.sub('sfan', '', str(data_fans['w83793'][i]))
            data2 = re.sub('[()]', '', str(data2))
            data2 = data2.split(",")
            data2[1] = data2[1].replace("current=", "")
            if int(data2[1]) > 0:
                correct = correct + 1
                print('detecte label_fan' + str(i+1))
                label_fan[str(i)] = wx.StaticText(panel, wx.ID_ANY, label="fan "+ str(i+1) +" : "+data2[1]+" RPM", pos=(0,100+correct*20), size=(200,20), style=wx.ALIGN_CENTRE)

        #self.timer = wx.Timer(self, wx.ID_ANY)
        #self.timer.Start(60)
        #self.Bind(wx.EVT_TIMER, self.AlphaCycle)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)
        ## ---------------------------- ##



    def onToggle(self, event):
        btnLabel = self.toggleBtn.GetLabel()
        if btnLabel == "Start":
            print "starting timer..."
            self.timer.Start(5000)
            self.toggleBtn.SetLabel("Stop")
        else:
            print "timer stopped!"
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")
 
    def update(self, event):
        # get ip
        ipEXT = requests.get("https://ip4.cuby-hebergs.com")

        # get temperature
        data = psutil.sensors_temperatures()
        data_fans = psutil.sensors_fans()
        for i in range(0, 9):
            data2 = re.sub('sfan', '', str(data_fans['w83793'][i]))
            data2 = re.sub('[()]', '', str(data2))
            data2 = data2.split(",")
            data2[1] = data2[1].replace("current=", "")
            if int(data2[1]) > 0:
                try:
                    label_fan[str(i)].SetLabel("fan "+ str(i+1) +" : "+data2[1]+" RPM")
                except KeyError:
                    continue

        data2 = re.sub('shwtemp', '', str(data['w83793'][0]))
        data2 = re.sub('[()]', '', str(data2))
        data2 = data2.split(",")
        data2[1] = data2[1].replace("current=", "")

        self.label.SetLabel(time.ctime())
        self.labelIpEXT.SetLabel("Your ip Externe : "+ipEXT.text)
        self.labeltemp0.SetLabel("Temp0 : "+data2[1]+"°C")

        if float(data2[1]) >= 0 or int(data2[1]):
            try:
                if int(data2[1]) < 55:
                    self.labeltemp0.SetForegroundColour((127,255,0)) # set text color
                if int(data2[1]) > 55:
                    self.labeltemp0.SetForegroundColour((255,150,0)) # set text color
                if int(data2[1]) > 80:
                    self.labeltemp0.SetForegroundColour((255,0,0)) # set text color
                if int(data2[1]) > 85:
                    self.labeltemp0.SetLabel("Temp0 : "+data2[1]+"°C Warning /!\\")
                    self.labeltemp0.SetForegroundColour((255,0,0)) # set text color
            except ValueError:
                if float(data2[1]) < 55:
                    self.labeltemp0.SetForegroundColour((127,255,0)) # set text color
                if float(data2[1]) > 55:
                    self.labeltemp0.SetForegroundColour((255,150,0)) # set text color
                if float(data2[1]) > 80:
                    self.labeltemp0.SetForegroundColour((255,0,0)) # set text color
                if float(data2[1]) > 85:
                    self.labeltemp0.SetLabel("Temp0 : "+data2[1]+"°C Warning /!\\")
                    self.labeltemp0.SetForegroundColour((255,0,0)) # set text color
        else:
            self.labeltemp0.SetLabel("Temp0 : Error sensors !")
            self.labeltemp0.SetForegroundColour((255,0,0)) # set text color


    def onMouseOver(self, event):
        # mouseover changes colour of button
        self.SetTransparent(255)
        event.Skip()

    def onMouseLeave(self, event):
        # mouse not over button, back to original colour
        self.SetTransparent(200)
        event.Skip()
 
    def AlphaCycle(self, evt):
        self.amount += self.delta
        if self.amount >= 255:
            self.delta = -self.delta
            self.amount = 255
        if self.amount <= 0:
            self.amount = 0
        self.SetTransparent(self.amount)
 
if __name__ == '__main__':
    app = wx.App(False)
    frm = Fader()
    frm.Show()
    app.MainLoop()
