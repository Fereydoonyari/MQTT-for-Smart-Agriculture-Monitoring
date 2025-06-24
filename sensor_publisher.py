import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime, UTC

broker = "localhost"
topic = "agriculture/field_data"

DEVICES = [
    {"device_id": "sensor_001", "location": "greenhouse_A", "sensor_type": "soil"},
    {"device_id": "sensor_002", "location": "greenhouse_A", "sensor_type": "climate"},
    {"device_id": "sensor_003", "location": "greenhouse_B", "sensor_type": "soil"},
    {"device_id": "sensor_004", "location": "greenhouse_B", "sensor_type": "climate"},
    {"device_id": "sensor_005", "location": "outdoor_field_1", "sensor_type": "soil"},
    {"device_id": "sensor_006", "location": "outdoor_field_1", "sensor_type": "climate"},
    {"device_id": "sensor_007", "location": "outdoor_field_2", "sensor_type": "soil"},
    {"device_id": "sensor_008", "location": "outdoor_field_2", "sensor_type": "climate"},
    {"device_id": "sensor_009", "location": "irrigation_zone_1", "sensor_type": "soil"},
    {"device_id": "sensor_010", "location": "irrigation_zone_2", "sensor_type": "soil"},
]

client = mqtt.Client("SimulatedSensor")
client.connect(broker, 1883)

def simulate_soil_sensor_data(device_id, location):
    return {
        "device_id": device_id,
        "location": location,
        "sensor_type": "soil",
        "soil_moisture": random.randint(20, 85),
        "soil_temperature": round(random.uniform(10.0, 35.0), 1), 
        "soil_ph": round(random.uniform(5.5, 7.5), 1), 
        "soil_conductivity": random.randint(100, 2000), 
        "timestamp": datetime.now(UTC).isoformat()
    }

def simulate_climate_sensor_data(device_id, location):
    return {
        "device_id": device_id,
        "location": location,
        "sensor_type": "climate",
        "air_temperature": round(random.uniform(15.0, 40.0), 1),
        "humidity": random.randint(30, 90),  
        "light_intensity": random.randint(0, 1200),  
        "wind_speed": round(random.uniform(0, 25.0), 1),  
        "timestamp": datetime.now(UTC).isoformat()
    }

def simulate_data():
    device = random.choice(DEVICES)
    
    if device["sensor_type"] == "soil":
        return simulate_soil_sensor_data(device["device_id"], device["location"])
    else:
        return simulate_climate_sensor_data(device["device_id"], device["location"])

print("Starting sensor simulation with multiple devices and locations")
print(f"Available devices: {len(DEVICES)}")
for device in DEVICES:
    print(f"  - {device['device_id']} at {device['location']} ({device['sensor_type']} sensor)")

try:
    while True:
        payload = json.dumps(simulate_data())
        client.publish(topic, payload)
        print("Published:", payload)
        time.sleep(3)
except KeyboardInterrupt:
    print("\nSimulation stopped by user")
    client.disconnect()
