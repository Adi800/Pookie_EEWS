CREATE DATABASE seismic_data;
USE seismic_data;

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    magnitude FLOAT,
    depth FLOAT,
    epicenter VARCHAR(100),
    affected_range FLOAT
);

CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50) UNIQUE,
    location VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    email VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    notification_radius FLOAT
);
