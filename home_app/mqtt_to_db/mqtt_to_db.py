import paho.mqtt.client as mqtt
import psycopg2
import os

# Připojení k PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="db",
    port=5432
)
cur = conn.cursor()

# MQTT callback pro příjem zpráv
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()

        if topic == "fermentace/senzory":
            temp, humidity = map(float, payload.split(","))
            cur.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)", (temp, humidity))
            conn.commit()
            print(f"Uloženo: Teplota={temp}°C, Vlhkost={humidity}%")
    except Exception as e:
        print(f"Chyba: {e}")

# Připojení k MQTT brokeru
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("mosquitto", 1883)
mqtt_client.subscribe("fermentace/senzory")
mqtt_client.loop_forever()
