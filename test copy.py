# hardware platform: FireBeetle-ESP32
import ssd1306
from network import WLAN, STA_IF, AP_IF
from machine import Pin, I2C, Timer,reset
from simple1 import MQTTClient
from time import sleep_ms,sleep

i2c = I2C(scl=Pin(14), sda=Pin(2), freq=100000)
s = ssd1306.SSD1306_I2C(128, 64, i2c)
SERVER = "pszvvvd.mqtt.iot.gz.baidubce.com"
PORT = 1883
CLIENT_ID = "11122223333123"
USER_NAME = "pszvvvd/esp8266_test"
PASSWORD = "KDk3WfD1HtgJVbJe"
TOPIC = "topic"
# SSID = "1"
# WLAN_PASSWORD = "12345677"
sta_if = WLAN(STA_IF)
ap_if = WLAN(AP_IF)

# if ap_if.active():
#     ap_if.active(False)
# if not sta_if.isconnected():
#     print('connecting to network...')
# sta_if.active(True)
# sta_if.connect(SSID, WLAN_PASSWORD)

def sub_cb(topic, msg):
    print("{:s},{:s}".format(topic, msg))
    s.fill(0)
    s.text("{:s}:{:s}".format(topic,msg),0,0)
    s.show()

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()


c = MQTTClient(CLIENT_ID, SERVER, PORT, user=USER_NAME, password=PASSWORD, keepalive=60)
c.set_callback(sub_cb)
c.connect()
c.subscribe(TOPIC)
c.publish(TOPIC, 'hello ESP266')
while True:
    try:
        c.wait_msg()
    except:
        restart_and_reconnect()
# t = tm1638.TM1638(0,4,5,4)
# def test(aaa):
#     s.fill(0)
#     # t.show('00000000')
#     s.text("aaa={}".format(t.keys()),10,5)
#     s.show()
#     t.show('{:8d}'.format(t.keys()))
# test(1)
# t1 = Timer(1)
# t1.init(mode=Timer.PERIODIC,period=10,callback=test)
