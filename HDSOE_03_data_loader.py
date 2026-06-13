import mysql.connector
from datetime import datetime, timedelta
import random
import logging

logging.basicConfig(level=logging.INFO)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="manoj123",
    database="darkstore_analytics"
)
cursor = conn.cursor()

logging.info("Inserting dimension data...")

cursor.executemany("INSERT IGNORE INTO dim_zone VALUES (%s, %s, %s)", [
    (1, 'Velachery Hub', 'TIER_1_CRITICAL'),
    (2, 'Adyar Core', 'TIER_2_HIGH'),
    (3, 'OMR Sholinganallur', 'TIER_3_MODERATE')
])

cursor.executemany("INSERT IGNORE INTO dim_store VALUES (%s, %s, %s, %s, %s)", [
    (10, 'DarkStore-Velachery', 1000, 12.9796, 80.2185),
    (20, 'DarkStore-Adyar', 1500, 13.0063, 80.2574)
])

cursor.executemany("INSERT IGNORE INTO dim_rider VALUES (%s, %s, %s)", [
    (100, 'Rider Vignesh', 'EV_SCOOTER'),
    (200, 'Rider Kumar', 'PETROL_BIKE')
])

logging.info("Generating orders...")

base_time = datetime(2026, 6, 1, 18, 0, 0)
orders = []

for i in range(1000, 1200):
    o_id = i
    c_id = random.randint(5000, 6000)
    
    z_id = random.choices([1, 2, 3], weights=[70, 20, 10], k=1)[0] 
    s_id = 10 if z_id == 1 else 20
    r_id = random.choice([100, 200])
    
    o_time = base_time + timedelta(minutes=random.randint(1, 240))
    dist = round(random.uniform(1.5, 6.5), 2)
    basket = random.randint(300, 1200)
    fee = int(30 + (dist * 5))
    
    if z_id == 1:
        status = "BREACHED_SLA" if random.random() > 0.4 else "DELIVERED"
        d_time = o_time + timedelta(minutes=random.randint(40, 65))
    else:
        status = "DELIVERED"
        d_time = o_time + timedelta(minutes=random.randint(15, 30))
        
    orders.append((o_id, c_id, s_id, z_id, r_id, o_time, d_time, dist, basket, fee, status))

cursor.executemany("""INSERT IGNORE INTO fact_orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", orders)

conn.commit()
logging.info("Data load successful!!")

cursor.close()
conn.close()