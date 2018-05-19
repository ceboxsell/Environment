import paho.mqtt.client as mqtt
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

t = 0
h = 0
c = 0
th = "0c  0h"

def on_connect(client, userdata, flags, rc):
    con = 'Connected result '
    res = 'code {0}'.format(rc)
    # Subscribe (or renew if reconnect).
    mylcd.lcd_display_string(con, 1)
    mylcd.lcd_display_string(res, 2) 
    client.subscribe('temperature/#')
   
# Callback fires when a published message is received.
def on_temp(client, userdata, msg):
	# Decode temperature and humidity values from binary message paylod.
    #th = [float(x) for x in msg.payload.decode("utf-8")]
    global t
    global c

    t = float(msg.payload.decode("utf-8"))
    #print(t)

    if (c==0):
        c += 1
    elif (c == 1):
        display()

def on_message():
    print("there was a message")

    
def on_hum(client, userdata, msg):
    	# Decode temperature and humidity values from binary message paylod.
    #th = [float(x) for x in msg.payload.decode("utf-8")]
    global h
    global c
    
    h = float(msg.payload.decode("utf-8"))
    #print(h)
    if (c==0):
        c += 1
    elif (c == 1):
        display()

def display():
    global c
    global th
    th =  str(round(t,2)) + "c - " + str(round(h,2)) + "%" 
    mylcd.lcd_display_string("Temp & Humidity:", 1)
    #mylcd.lcd_display_string("               ", 2) 
    mylcd.lcd_display_string(th, 2)
    c == 0




client = mqtt.Client()
client.message_callback_add('temperature/humidity',on_hum)
client.message_callback_add('temperature/temp', on_temp)
client.on_connect = on_connect  # Specify on_connect callback
client.on_message = on_message  # Specify on_message callback
client.connect('localhost', 1883, 60)  # Connect to MQTT broker (also running on Pi).

# Processes MQTT network traffic, callbacks and reconnections. (Blocking)
client.loop_forever()

