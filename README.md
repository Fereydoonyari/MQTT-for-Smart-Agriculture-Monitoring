# MQTT-for-Smart-Agriculture-Monitoring
# Fereydoon Aliyari 560068 

This project simulates a smart agriculture monitoring system using MQTT for real-time sensor data transmission. It includes :
- sensor_publisher.py : Simulates multiple soil and climate sensors, publishing data to an MQTT broker.
- sensor_subscriber.py : Subscribes to the MQTT topic, validates incoming data, and stores it in MongoDB, MySQL, and Neo4j databases.

## Features 
- Simulates multiple devices and locations (soil and climate sensors)
- Publishes sensor data to an MQTT broker
- Validates and stores data in MongoDB, MySQL, and Neo4j
- Logs all operations for monitoring and debugging

## what i used for this project : 

- Python 3.8+
- MQTT broker (Mosquitto) running on 'localhost:1883'
- MongoDB running on 'localhost:27017'
- MySQL server with a database named 'agriculture' and tables:
  - 'soil_readings'
  - 'climate_readings'
- Neo4j running on 'localhost:7687' with user 'neo4j' and password '1523415234'
- Python packages:
  - paho-mqtt
  - pymongo
  - mysql-connector-python
  - py2neo


## Database Setup
## MySQL

Create the tables in 'agriculture' database:

CREATE TABLE soil_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    soil_moisture INT NOT NULL,
    soil_temperature DECIMAL(4,1) NOT NULL,
    soil_ph DECIMAL(3,1) NOT NULL,
    soil_conductivity INT NOT NULL,
    timestamp DATETIME NOT NULL
);

CREATE TABLE climate_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    air_temperature DECIMAL(4,1) NOT NULL,
    humidity INT NOT NULL,
    light_intensity INT NOT NULL,
    wind_speed DECIMAL(4,1) NOT NULL,
    timestamp DATETIME NOT NULL
);

CREATE TABLE devices (
    device_id VARCHAR(50) PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    sensor_type ENUM('soil', 'climate') NOT NULL
);

CREATE TABLE locations (
    location_id VARCHAR(100) PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL
);

INSERT INTO locations (location_id, location_name) VALUES
('greenhouse_A', 'Greenhouse A'),
('greenhouse_B', 'Greenhouse B'),
('outdoor_field_1', 'Outdoor Field 1'),
('outdoor_field_2', 'Outdoor Field 2'),
('irrigation_zone_1', 'Irrigation Zone 1'),
('irrigation_zone_2', 'Irrigation Zone 2');

INSERT INTO devices (device_id, location, sensor_type) VALUES
('sensor_001', 'greenhouse_A', 'soil'),
('sensor_002', 'greenhouse_A', 'climate'),
('sensor_003', 'greenhouse_B', 'soil'),
('sensor_004', 'greenhouse_B', 'climate'),
('sensor_005', 'outdoor_field_1', 'soil'),
('sensor_006', 'outdoor_field_1', 'climate'),
('sensor_007', 'outdoor_field_2', 'soil'),
('sensor_008', 'outdoor_field_2', 'climate'),
('sensor_009', 'irrigation_zone_1', 'soil'),
('sensor_010', 'irrigation_zone_2', 'soil');

# mongoDB and neo4j 
- for mongoDB we use mongoDB Compass and create a connection
- for Neo4j we use Neo4j Desktop2 and create an instance for our data

