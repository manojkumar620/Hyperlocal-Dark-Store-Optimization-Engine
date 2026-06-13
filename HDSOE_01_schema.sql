CREATE DATABASE IF NOT EXISTS darkstore_analytics;
USE darkstore_analytics;

CREATE TABLE dim_store (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    capacity_limit INT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);

CREATE TABLE dim_zone (
    zone_id INT PRIMARY KEY,
    zone_name VARCHAR(100),
    demand_tier VARCHAR(20)
);

CREATE TABLE dim_rider (
    rider_id INT PRIMARY KEY,
    rider_name VARCHAR(100),
    vehicle_type VARCHAR(50)
);

CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    store_id INT,
    zone_id INT,
    rider_id INT,
    order_time DATETIME,
    delivery_time DATETIME,
    distance_km DECIMAL(5,2),
    basket_value INT,
    delivery_fee INT,
    operational_status VARCHAR(50),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id),
    FOREIGN KEY (zone_id) REFERENCES dim_zone(zone_id),
    FOREIGN KEY (rider_id) REFERENCES dim_rider(rider_id)
);

CREATE INDEX idx_zone ON fact_orders(zone_id);
CREATE INDEX idx_store ON fact_orders(store_id);
CREATE INDEX idx_rider ON fact_orders(rider_id);