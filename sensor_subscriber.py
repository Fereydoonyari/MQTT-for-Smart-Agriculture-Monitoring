import paho.mqtt.client as mqtt
import json
import pymongo
import mysql.connector
from py2neo import Graph, Node
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["agriculture"]
    mongo_collection = mongo_db["sensor_data"]
    
    sql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1523415234",
        database="agriculture"
    )
    sql_cursor = sql_conn.cursor()
    
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "1523415234"))
    
    logger.info("All database connections established successfully")
except Exception as e:
    logger.error(f"Database connection error: {e}")
    exit(1)

def validate_sensor_data(data):
    required_fields = ["device_id", "location", "sensor_type", "timestamp"]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    if data["sensor_type"] not in ["soil", "climate"]:
        return False, f"Invalid sensor type: {data['sensor_type']}"
    
    return True, "Data is valid"

def store_soil_sensor_data(data):
    try:
        mongo_collection.insert_one(data)
        
        sql_cursor.execute("""
            INSERT INTO soil_readings (device_id, location, soil_moisture, soil_temperature, 
                                     soil_ph, soil_conductivity, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["device_id"],
            data["location"],
            data["soil_moisture"],
            data["soil_temperature"],
            data["soil_ph"],
            data["soil_conductivity"],
            data["timestamp"]
        ))
        sql_conn.commit()
        
        device = Node("Device", 
                     id=data["device_id"], 
                     location=data["location"],
                     sensor_type=data["sensor_type"])
        graph.merge(device, "Device", "id")
        
        location = Node("Location", name=data["location"])
        graph.merge(location, "Location", "name")
        
        graph.run("""
            MATCH (d:Device {id: $device_id})
            MATCH (l:Location {name: $location})
            MERGE (d)-[:LOCATED_AT]->(l)
        """, device_id=data["device_id"], location=data["location"])
        
        logger.info(f"Stored soil sensor data from {data['device_id']} at {data['location']}")
        
    except Exception as e:
        logger.error(f"Error storing soil sensor data: {e}")

def store_climate_sensor_data(data):
    try:
        mongo_collection.insert_one(data)
        
        sql_cursor.execute("""
            INSERT INTO climate_readings (device_id, location, air_temperature, humidity, 
                                        light_intensity, wind_speed, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["device_id"],
            data["location"],
            data["air_temperature"],
            data["humidity"],
            data["light_intensity"],
            data["wind_speed"],
            data["timestamp"]
        ))
        sql_conn.commit()
        
        device = Node("Device", 
                     id=data["device_id"], 
                     location=data["location"],
                     sensor_type=data["sensor_type"])
        graph.merge(device, "Device", "id")
        
        location = Node("Location", name=data["location"])
        graph.merge(location, "Location", "name")
        
        graph.run("""
            MATCH (d:Device {id: $device_id})
            MATCH (l:Location {name: $location})
            MERGE (d)-[:LOCATED_AT]->(l)
        """, device_id=data["device_id"], location=data["location"])
        
        logger.info(f"Stored climate sensor data from {data['device_id']} at {data['location']}")
        
    except Exception as e:
        logger.error(f"Error storing climate sensor data: {e}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        logger.info(f"Received data from {data.get('device_id', 'unknown')} at {data.get('location', 'unknown')}")
        is_valid, message = validate_sensor_data(data)
        if not is_valid:
            logger.error(f"Invalid data received: {message}")
            return
        if data["sensor_type"] == "soil":
            store_soil_sensor_data(data)
        elif data["sensor_type"] == "climate":
            store_climate_sensor_data(data)
        else:
            logger.error(f"Unknown sensor type: {data['sensor_type']}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("agriculture/field_data")
logger.info("Connected and subscribed to agriculture/field_data topic")

try:
    client.loop_forever()
except KeyboardInterrupt:
    logger.info("Shutting down subscriber...")
    client.disconnect()
    sql_conn.close()
    mongo_client.close()
except Exception as e:
    logger.error(f"Error in MQTT client: {e}")
