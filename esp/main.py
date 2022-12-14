import dht
import machine
import network

from config import broker_ip, wlan_ssid, wlan_password
from time import sleep
from umqtt.simple import MQTTClient

dht_data_pin = 4
client_id = "esp"
keepalive = 30

dht22 = dht.DHT22(machine.Pin(dht_data_pin))
wlan = network.WLAN(network.STA_IF)
client = MQTTClient(client_id, broker_ip, keepalive=keepalive)

while True:
    try:
        wlan.connect(wlan_ssid, wlan_password)
        client.connect()
        while True:
            try:
                dht22.measure()
                reading = f"temp,location=home value={dht22.temperature()}"
                client.publish("sensors", reading.encode("utf-8"))
                sleep(15)
            except Exception as e:
                raise RuntimeException(f"Error while publishing reading: {e}")
    except RuntimeException as e:
        print(e)
        sleep(5)



