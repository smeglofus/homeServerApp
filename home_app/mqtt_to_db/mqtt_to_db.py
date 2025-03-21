import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions

import json
import os

# MQTT nastavení
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")  # Název kontejneru
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "senzory/data")

# InfluxDB nastavení
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "moj-token")  # Nastav svůj API token
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "moje-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "sensordata")

# Připojení k InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=1000))


# Callback při připojení k MQTT brokeru
def on_connect(client, userdata, flags, rc):
    print(f"✅ Připojeno k MQTT brokeru: {MQTT_BROKER}:{MQTT_PORT}")
    client.subscribe(MQTT_TOPIC)


# Callback při příjmu zprávy z MQTT
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        print(f"📥 Přijatá data: {payload}")

        # Extrahuj hodnoty
        temperature = payload.get("temperature")
        humidity = payload.get("humidity")

        # Vytvoř bod pro InfluxDB
        point = Point("sensor_data").field("temperature", temperature).field("humidity", humidity)

        # Zapiš do InfluxDB
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print("✅ Data uložena do InfluxDB")

    except Exception as e:
        print(f"❌ Chyba při zpracování dat: {e}")


# Nastavení MQTT klienta
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Připojení k MQTT brokeru
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
