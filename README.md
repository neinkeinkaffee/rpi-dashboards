# rpi-dashboards

## MQTT

```
scp mosquitto.conf pi@pi_ip:/home/pi
```
```
docker run -it -p 1883:1883 -p 9001:9001 -v /home/pi/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto
```

## InfluxDB

```
docker run -d -p 8086:8086 -v influxdb:/var/lib/influxdb --name influxdb influxdb:1.8
docker exec -it influxdb influx
```
```
create database sensors
use database sensors
create user 'telegraf' with password 'telegraf'
```

## Telegraf

```
docker run --rm telegraf telegraf config > telegraf.conf
```

```
[[inputs.mqtt_consumer]]
servers = ["tcp://rpi_ip:1883"]
topics = ["sensors"]

[[ outputs.influxdb ]]
urls = ["http://rpi_ip:8086"]
database = "sensors"
skip_database_creation = true
username = "telegraf"
password = "telegraf"
```

```
docker run  -v /home/pi/:/etc/telegraf:ro telegraf
```

## Grafana

```
docker run -d -p 3000:3000 grafana/grafana
```

## ESP8266

```
brew install esptool
esptool.py --port /serial/port erase_flash
esptool.py --port /serial/port --baud 460800 write_flash --flash_size=detect 0 /path/to/esp/binary
```

```
brew install minicom
minicom -D /serial/port
```

```
pip install adafruit-ampy
ampy --port /serial/port put config.py
ampy --port /serial/port run main.py
ampy --port /serial/port put main.py
```