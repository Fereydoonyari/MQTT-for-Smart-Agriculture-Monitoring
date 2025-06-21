import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

broker = "localhost"
topic = "agriculture/field_data"

client = mqtt.Client("SimulatedSensor")
client.connect(broker, 1883)

def simulate_data():
    return {
        "device_id": "sim_sensor_01",
        "location": "greenhouse_A",
        "soil_moisture": random.randint(30, 70),
        "temperature": round(random.uniform(18.0, 35.0), 1),
        "light": random.randint(200, 800),
        "timestamp": datetime.utcnow().isoformat()
    }

while True:
    payload = json.dumps(simulate_data())
    client.publish(topic, payload)
    print("Published:", payload)
    time.sleep(5)
