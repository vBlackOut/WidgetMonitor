# coding: utf-8
import wx
import time
import requests
import psutil
import re

 
class Fader(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, title='Test', size=(200, 300))
        self.amount = 200
        self.delta = 5
        panel = wx.Panel(self, wx.ID_ANY)
 
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
        ipEXT = requests.get("http://ip4.cuby-hebergs.com")
        
        # get temperature
        data = psutil.sensors_temperatures()
        data2 = re.sub('shwtemp', '', str(data['w83793'][0]))
        data2 = re.sub('[()]', '', str(data2))
        data2 = data2.split(",")
        data2[1] = data2[1].replace("current=", "")

        self.label.SetLabel(time.ctime())
        self.labelIpEXT.SetLabel("Your ip Externe : "+ipEXT.text)
        self.labeltemp0.SetLabel("Temp0 : "+data2[1]+"°C")

    def onMouseOver(self, event):
        # mouseover changes colour of button
        self.SetTransparent(255)
        event.Skip()

    def onMouseLeave(self, event):
        # mouse not over button, back to original colour
        self.SetTransparent(150)
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
