import network
esp.osdebug(None)
import gc
gc.collect()
ssid = '1'
password = '12345677'


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print(station.ifconfig())