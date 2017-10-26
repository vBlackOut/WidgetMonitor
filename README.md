<p align="center">
<h1>WidgetMonitor</h1>
</p>
  
click on button start for refresh ever 5s information 

Exclusive Update work for all fedora >= 20  

```
- check fan speed
- check update
- check your ip externe
- check system sensor temperature
- check ping
```
<table border="0" style="border:0px;border-collapse: collapse;"><tr><td><a href="url"><img align="center" src="https://www.cuby-hebergs.com/dl/images/github/WidgetMonitor/main3.png" align="left" height="400" width="400" ></a></td><td><a href="url"><img align="center" src="https://www.cuby-hebergs.com/dl/images/github/WidgetMonitor/mains3_update.png" align="left" height="400" width="400" ></a></td></tr></table>



## Requirement  
```
- Recommandation system OS : Fedora 25 or highter
- wxPython ( python -m pip install wxpython )
- psutil ( python -m pip install psutil )
- daemonize ( python -m pip install daemonize )

```
## Install via requirements.txt
```
pip install -r requirements.txt
```

## Launch 
```
git clone https://github.com/vBlackOut/WidgetMonitor
cd WidgetMonitor
(for fedora) sudo dnf install -y wxPython
sudo pip install -r requirements.txt
sudo python main.py
click Start button
```
## Bug
```

On Ubuntu 16.10 fan_sensor return {}
On Ubuntu 16.10 speed_fans return {}
On Ubuntu system update check

```
## OS work test  
Fedora 100%  
Ubuntu 50%  


Thank have fun...
