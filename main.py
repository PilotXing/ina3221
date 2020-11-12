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

sta_if = WLAN(STA_IF)
ap_if = WLAN(AP_IF)



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
        c.check_msg()
    except OSError as e:
        restart_and_reconnect()
