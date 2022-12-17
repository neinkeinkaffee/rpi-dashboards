import dht
import machine
import network

from config import broker_ip, wlan_ssid, wlan_password
from time import sleep
from umqtt.simple import MQTTClient

dht_data_pin = 4
read_interval = 15
client_id = "esp"
keepalive = 30

dht22 = dht.DHT22(machine.Pin(dht_data_pin))
ap = network.WLAN(network.AP_IF)
ap.active(False)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
client = MQTTClient(client_id, broker_ip, keepalive=keepalive)

while True:
    while True:
        print("Establishing network connection")
        wlan.connect(wlan_ssid, wlan_password)
        if wlan.isconnected():
            print("Network connection established")
            break
        print("Couldn't establish network connection, retrying in 5 seconds")
        sleep(5)
    while True:
        try:
            error = client.connect()
            print(f"Connection to MQTT broker at {broker_ip} established")
            break
        except Exception as e:
            print(f"Error connecting to MQTT broker at {broker_ip}: {e}")
            sleep(5)
    while True:
        try:
            dht22.measure()
            reading = f"temp,location=home value={dht22.temperature()}"
            print(reading)
            client.publish("sensors", reading.encode("utf-8"))
            sleep(read_interval)
        except Exception as e:
            print(f"Error publishing reading: {e}")
            break



