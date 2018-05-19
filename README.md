# Environment

pip3 install paho_mqtt

install i2c driver from Adafruit.

install mosquitto on pi for the broker and then the paho client to talk to it.
ESP32 saves memory by only sending binary data to the broker  so on it your topic is binary but send your data as is it is stored in binary so you need to convert on the pi.

add on callbacks are setup to handle the temperature/ queues under the topic, each fires individually hence the count to see when both are updated then we call the display update

Uses i2c backpack for 16*2 LCD with driver from Adafruit i2c LCD driver.


ESP32 files are there, use esptool to flash firmware and uPyCraft to download files etc is easy as.
