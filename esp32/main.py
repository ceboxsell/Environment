


import time
import ubinascii
import micropython
import machine
from machine import Pin
import dht

from uqmtt.robust import MQTTClient


from lib import ConnectWifi
ConnectWifi.connect()

d = dht.DHT22(machine.Pin(16))

SERVER = "192.168.86.232"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
KEEPALIVE = 60
TOPIC = b"temp"
LED_PIN = 2
TOUCH_PIN = 15
#LED = "blue"
led_flashing = 0
led_status = 0
connected = False

d.measure()
temp = d.temperature()
humidity = d.humidity()
print('Hum ' + str(humidity) + ' Temp ' + str(temp))


def settimeout(duration): 
    pass

#def short_blink():
#    for i in range(4):
#        led.value(1)
#        time.sleep_ms(100)
#        led.value(0)
#        time.sleep_ms(100)

def sub_cb(topic, msg):
#    global led_flashing
#    print((topic, msg))
    #msg = json.loads(msg)

    #if msg["state"]["reported"]["channel"] == HAT_COLOUR:
        #if msg["state"]["reported"]["status"] == 1:
 #   if msg == b"on":
        #led.value(1)
 #       led_flashing = 1
        #elif msg["state"]["reported"]["status"] == 0:
        #led.value(0)
#        temp = d.temperature()
#        humidity = d.humidity()
        client.publish(topic=b"temp", msg=str(temp))
        client.publish(topic=b"humidity", msg=str(humidity))
#    elif msg != b"on":
#        led_flashing = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT, value=1)
touch = machine.TouchPad(machine.Pin(TOUCH_PIN))

client = MQTTClient(CLIENT_ID, SERVER, keepalive = KEEPALIVE)
client.DEBUG = True
client.settimeout = settimeout
client.set_callback(sub_cb)
#client.connect()
#client.subscribe(TOPIC, qos=1)
print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC))

try:
    while 1:

        if not connected:
            client.connect()

            #short_blink()

            connected = True
            last_publish = 0
            last_ping = time.ticks_ms()

            client.subscribe(TOPIC, qos=1)
            client.publish(topic=b"temp", msg=str(temp))
            client.publish(topic=b"humidity", msg=str(humidity))
            #client.publish(topic=b"led", msg="off")
        else:

            # Periodically ping the broker consistently with the "keepalive"
            # argument used when connecting.  If this isn't done, the broker will
            # disconnect when the client has been idle for 1.5x the keepalive
            # time.
            if time.ticks_ms() - last_ping >= KEEPALIVE * 1000:
                 client.ping()
                 last_ping = time.ticks_ms()
            time.sleep(4)
            d.measure()
            temp = d.temperature()
            humidity = d.humidity()
            print('Hum ' + str(humidity) + ' Temp ' + str(temp))
            client.publish(topic=b"temp", msg=str(temp))
            client.publish(topic=b"humidity", msg=str(humidity))

        # turn off LED with touch
        #if led_flashing == 1 and touch.read() < 1200:
        #    led_flashing = 0
        #    client.publish(topic=b"led", msg="off")

        # flashing logic
        #if led_flashing == 1:
        #    led.value(1)
        #    led_status = 1
        #    time.sleep(0.1)
        #    led.value(0)
        #    led_status = 0
        #    time.sleep(0.1)
        #elif led_flashing == 0 and led_status == 1:
         #   led.value(0)
        #else:
        #    time.sleep(0.1)

        # check message
        try:
            client.check_msg()
        except OSError as e:
            if str(e) == '-1':
                client.disconnect()
                connected = False
                continue
            
finally:
    client.disconnect()


