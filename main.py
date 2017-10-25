# coding: utf-8
from daemonize import Daemonize
import wx
import time
import requests
import psutil
import re
import subprocess
import sys


pid = "/tmp/WidgetMonitor.pid"

# detect automatical controller
Controller = ""
detect_controller = psutil.sensors_fans()
print detect_controller
for control in detect_controller:
    Controller = control


class Fader(wx.Frame):
 
    def __init__(self):
        global label_fan
        global panel
        global ipEXT
        self.t = time.time()
        no_sys_menu = wx.CAPTION
        wx.Frame.__init__(self, None, title='WidgetMonitor', size=(200, 330), style=no_sys_menu)
        self.amount = 200
        self.delta = 5
        #self.ToggleWindowStyle(wx.STAY_ON_TOP)
        style = wx.TRANSPARENT_WINDOW if sys.platform.lower() == 'win32' else 0
        panel = wx.Panel(self, wx.ID_ANY, style=style)
        if panel.CanSetTransparent:
            panel.SetTransparent(100)
 
        self.SetTransparent(self.amount)
        self.Maximize(False)
        topSizer = wx.BoxSizer(wx.VERTICAL)
 
        ## ------- Fader Timer -------- ##
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        self.toggleBtn = wx.Button(panel, wx.ID_ANY, "Start", size=(50,50), pos=(75,0))
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)

        self.label = wx.StaticText(panel, wx.ID_ANY, label=time.ctime(), pos=(0,50), size=(200,20), style=wx.ALIGN_CENTRE)
        self.labelIpEXT = wx.StaticText(panel, wx.ID_ANY, label="Your ip Externe : 0.0.0.0", pos=(0,75), size=(200,20), style=wx.ALIGN_CENTRE)
        self.labelping = wx.StaticText(panel, wx.ID_ANY, label="check ping...", pos=(0,90), size=(200,20), style=wx.ALIGN_CENTRE)
        self.labeltemp0 = wx.StaticText(panel, wx.ID_ANY, label="temp0 : 0°C", pos=(0,110), size=(200,20), style=wx.ALIGN_CENTRE)

        #check fan speed
        correct = 0
        label_fan = {}
        data_fans = psutil.sensors_fans()
        for i in range(0, 9):
            try:
                data2 = re.sub('sfan', '', str(data_fans[Controller][i]))
                data2 = re.sub('[()]', '', str(data2))
                data2 = data2.split(",")
                data2[1] = data2[1].replace("current=", "")
                if int(data2[1]) > 0:
                    correct = correct + 1
                    print('detecte label_fan' + str(i+1))
                    label_fan[str(i)] = wx.StaticText(panel, wx.ID_ANY, label="fan "+ str(i+1) +" : "+data2[1]+" RPM", pos=(0,110+correct*20), size=(200,20), style=wx.ALIGN_CENTRE)
            except IndexError:
                break

            except KeyError:
                continue

        if correct == 0:
           correct = 1

        if correct > 1:
            # check update system
            self.labelupdate_sys = wx.StaticText(panel, wx.ID_ANY, label="checking... update", pos=(0,110+correct*30), size=(200,20), style=wx.ALIGN_CENTRE)

            # check cpu count
            self.labelinfo_sys = wx.StaticText(panel, wx.ID_ANY, label="Information system", pos=(0,110+correct*40), size=(200,20), style=wx.ALIGN_CENTRE)

            self.labelcpu_sys = wx.StaticText(panel, wx.ID_ANY, label="Number core CPU " + str(psutil.cpu_count()), pos=(0,110+correct*45), size=(200,20), style=wx.ALIGN_CENTRE)
            users = psutil.users()
            for user in users:
                self.labelusername_sys = wx.StaticText(panel, wx.ID_ANY, label="Username " + str(user[0]), pos=(0,110+correct*50), size=(200,20), style=wx.ALIGN_CENTRE)

            self.labelcopyright = wx.StaticText(panel, wx.ID_ANY, label="© vBlackOut", pos=(0,110+correct*55), size=(200,20), style=wx.ALIGN_CENTRE)
        
        else:
            # check update system
            self.labelupdate_sys = wx.StaticText(panel, wx.ID_ANY, label="checking... update", pos=(0,120+correct*30), size=(200,20), style=wx.ALIGN_CENTRE)

            # check cpu count
            self.labelinfo_sys = wx.StaticText(panel, wx.ID_ANY, label="Information system", pos=(0,130+correct*40), size=(200,20), style=wx.ALIGN_CENTRE)

            self.labelcpu_sys = wx.StaticText(panel, wx.ID_ANY, label="Number core CPU " + str(psutil.cpu_count()), pos=(0,140+correct*45), size=(200,20), style=wx.ALIGN_CENTRE)
            users = psutil.users()
            for user in users:
                self.labelusername_sys = wx.StaticText(panel, wx.ID_ANY, label="Username " + str(user[0]), pos=(0,150+correct*50), size=(200,20), style=wx.ALIGN_CENTRE)

            self.labelcopyright = wx.StaticText(panel, wx.ID_ANY, label="© vBlackOut", pos=(0,160+correct*55), size=(200,20), style=wx.ALIGN_CENTRE)


        #self.timer = wx.Timer(self, wx.ID_ANY)
        #self.timer.Start(60)
        #self.Bind(wx.EVT_TIMER, self.AlphaCycle)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)
        ## ---------------------------- ##



    def onToggle(self, event):
        btnLabel = self.toggleBtn.GetLabel()
        if btnLabel == "Start":
            print ("starting timer...")
            self.timer.Start(5000)
            self.toggleBtn.SetLabel("Stop")
        else:
            print ("timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")
 
    def update(self, event):

        if time.time()-self.t>3600 or time.time()-self.t<10:
            try:
            # get ip
                ipEXT = requests.get("https://ip4.cuby-hebergs.com")
                ipEXT = ipEXT.text 
            except:
                ipEXT = "no network"

            self.labelIpEXT.SetLabel("Your ip Externe : "+ipEXT)
            if time.time()-self.t>15:
                self.t=time.time()

        # get temperature
        data = psutil.sensors_temperatures()
        data_fans = psutil.sensors_fans()
        for i in range(0, 9):
            try:
                if Controller == "thinkpad":
                    data2 = re.sub('sfan', '', str(data_fans[Controller][i]))
                    data2 = re.sub('[()]', '', str(data2))
                    data2 = data2.split(",")
                    data2[1] = data2[1].replace("current=", "")
                    
                else:
                    data2 = re.sub('sfan', '', str(data_fans[Controller][i]))
                    data2 = re.sub('[()]', '', str(data2))
                    data2 = data2.split(",")
                    data2[1] = data2[1].replace("current=", "")

                if int(data2[1]) > 0:
                    try:
                        label_fan[str(i)].SetLabel("fan "+ str(i+1) +" : "+data2[1]+" RPM")
                    except KeyError:
                        continue
            except IndexError:
                break
            except KeyError:
                continue

        if Controller == "thinkpad":
            data2 = re.sub('shwtemp', '', str(data["acpitz"][0]))
            data2 = re.sub('[()]', '', str(data2))
            data2 = data2.split(",")
            data2[1] = data2[1].replace("current=", "")

        else:
            try:
               data2 = re.sub('shwtemp', '', str(data[Controller][0]))
               data2 = re.sub('[()]', '', str(data2))
               data2 = data2.split(",")
               data2[1] = data2[1].replace("current=", "")
            except KeyError:
               pass



        self.label.SetLabel(time.ctime())

        # Run the "ping" command
        command = "ping -c 2 www.google.com"  # the shell command
        output = subprocess.check_output(command, shell=True)

        # And interpret the output
        matches = re.findall(" time=([\d.]+) ms", output)
        matches = [float(match) for match in matches]
        ms = round(sum(matches)/len(matches),1)
        self.labelping.SetLabel("your ping : "+str(ms)+" ms")

        if ms < 200.0:
            self.labelping.SetForegroundColour((127,255,0)) # set text color
        else:
            self.labelping.SetForegroundColour((255,0,0))

        try:
            self.labeltemp0.SetLabel("Temp0 : "+data2[1]+"°C")
        except:
           pass
        try:
            if float(data2[1]) >= 0:
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

        except ValueError:
            if int(data2[1]) >= 0:
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
        
        except UnboundLocalError:
            pass

        _reg_ex_pkg = re.compile(b'^\S+\.', re.M)
        try:
           output, error = subprocess.Popen(['dnf', 'check-update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        except OSError:
           output, error = subprocess.Popen(['sudo', 'apt-get', '-u', '-V', 'update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        updates = len(_reg_ex_pkg.findall(output))
        if updates == 0:
            self.labelupdate_sys.SetLabel("No update for your system")
            self.labelupdate_sys.SetForegroundColour((127,255,0))
        else:
            self.labelupdate_sys.SetLabel("new update ("+str(updates)+") packages")
            self.labelupdate_sys.SetForegroundColour((255,150,0))
            self.toggleBtn_update = wx.Button(self, wx.ID_ANY, "Update system", size=(100,52), pos=(50,-1))
            self.toggleBtn_update.Bind(wx.EVT_BUTTON, self.UpdateSys)



    def UpdateSys(self, event):
        self.toggleBtn_update.Show(False)
        self.labelupdate_sys.SetLabel("Update progress...")
        time.sleep(2)
        output, error = subprocess.Popen(['sudo', 'dnf', 'update', "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        #print(output, error)
        self.labelupdate_sys.SetLabel("Finish")
        time.sleep(2)
        event.Skip()

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
 
def start():
    app = wx.App(False)
    frm = Fader()
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    daemon = Daemonize(app="WidgetMonitor", pid=pid, action=start)
    daemon.start()
    #start()
