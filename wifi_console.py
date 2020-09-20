import network
import time
import json
import os
from str_ing.colorful_print import color_print,color_input
import str_ing.colorful_print
from str_ing.table import Table

WIFI_AUTH_MODES=["Open","WEP","WPA-PSK","WPA2-PSK","WPA/WPA2-PSK"]
class Wifi_Console:
    def __init__(self):
        self.sta_wifi=network.WLAN(network.STA_IF)
        self.ap_wifi=network.WLAN(network.AP_IF)
        self.available_wifi=[]

    def scan(self):
        color_print("Scaning Wifi...")

        self.available_wifi=[]

        available_wifi=self.sta_wifi.scan()
        available_wifi.sort(key=lambda l:l[3])
        available_wifi=available_wifi[::-1]

        max_ssid_len=max([len(i[0].decode()) for i in available_wifi])+2
        
        result=Table(["NO.","SSID","RSSI","Auth Mode"])
        for i in range(len(available_wifi)):
            _wifi=available_wifi[i]
            ssid=_wifi[0].decode()
            rssi=_wifi[3]
            try:
                authmode=WIFI_AUTH_MODES[_wifi[4]]
            except IndexError:
                authmode="Unknown:%d"%_wifi[4]
            
            self.available_wifi.append((ssid,_wifi[4]))

            line=[]
            line.append(str(i))
            line.append(ssid)
            line.append("%d dbm"%rssi)
            line.append(authmode)
            result.new_line(line)
        print(result)
    
    def connect(self):
        use_saved=0
        try:
            with open("wifi.json","r") as f:
                _wifi_dict=json.loads(f.read())
                if color_input("Do you want to connect the wifi saved?(y or N)\n>")=="y":
                    ssid=_wifi_dict["SSID"]
                    pass_word=_wifi_dict["PassWord"]
                    use_saved=1
                else:
                    raise Exception("xd")

        except Exception as err:
            if str(err)!="xd":
                color_print("Fail to load 'wifi.json'",fg="red")
            
            self.scan()

            num=int(color_input("Please enter the number of the wifi you want to connect\n>"))

            try:
                _wifi=self.available_wifi[num]
            except IndexError:
                color_print("Invalid number.",fg="red")
                return

            ssid=_wifi[0]

            if _wifi[1]:
                pass_word=color_input("Please enter the password\n>")
            else:
                pass_word=""

        if self._connect(ssid,pass_word)==0:
            return

        if not use_saved:
            save=color_input("Do you want to save this wifi?(y or N)\n>")
            if save=="y":
                with open("wifi.json","w") as f:
                    f.write(json.dumps({"SSID":ssid,"PassWord":pass_word}))
                color_print("Saved.")
        
    def _connect(self,ssid,pass_word):
        self.sta_wifi.connect(ssid,pass_word)
        color_print("Trying to connect.",end="")

        start_time=time.time()
        time_out=10
        while(self.sta_wifi.isconnected()):
            if time.time()-start_time>time_out:
                color_print("Time out, failed.",fg="red")
                return 0
            color_print(".")
            time.sleep(0.5)
        color_print("\nSuccessfully connect to %s"%ssid)
        return 1
    
    def auto_connect(self):
        self.sta_wifi.active(True)
        try:
            with open("wifi.json","r") as f:
                _wifi_dict=json.loads(f.read())
                ssid=_wifi_dict["SSID"]
                pass_word=_wifi_dict["PassWord"]
        except:
            color_print("Fail to load 'wifi.json'. Auto connect failed.",fg="red")
            return
        if self._connect(ssid,pass_word)==0:
            return
    
    def disconnect(self):
        self.sta_wifi.disconnect()
        color_print("Disconnected.")
    
    def info(self):
        color_print("\nMode info")

        table=Table(["Mode","State"])
        table.new_line(["STA",
            "Enabled" if self.sta_wifi.active() else "Disabled"
            ])
        table.new_line(["AP",
            "Enabled" if self.ap_wifi.active() else "Disabled"
            ])
        print(table)#
        
        print("\nNetwork info")
        ifcfg=self.sta_wifi.ifconfig()
        table=Table(["IP","Net Mask","Gateway","DNS"])
        table.new_line(ifcfg)
        print(table)
        
        print("\nSTA_info")
        table=Table(["Connected","SSID","RSSI"])
        table.new_line([self.sta_wifi.isconnected(),"",self.sta_wifi.rssi()])
        