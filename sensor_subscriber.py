import paho.mqtt.client as mqtt
import json
import pymongo
import mysql.connector
from py2neo import Graph, Node

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

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Received:", data)

    mongo_collection.insert_one(data)

    sql_cursor.execute("""
        INSERT INTO readings (device_id, location, soil_moisture, temperature, light, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["device_id"],
        data["location"],
        data["soil_moisture"],
        data["temperature"],
        data["light"],
        data["timestamp"]
    ))
    sql_conn.commit()

    device = Node("Device", id=data["device_id"], location=data["location"])
    graph.merge(device, "Device", "id")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("agriculture/field_data")
client.on_message = on_message
client.loop_forever()
