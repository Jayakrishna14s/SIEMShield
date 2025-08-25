from collections import defaultdict
from datetime import datetime, timedelta
import json
import re
import sys
from kafka import KafkaConsumer # type: ignore
import threading
import psycopg2 # type: ignore

sys.stdout.reconfigure(line_buffering=True)

KAFKA_BROKER = 'kafka:9093' 
GROUP_ID = 'multi-topic-consumer-group'


DB_HOST = "postgres"
DB_NAME = "SIEMSHIELD"
DB_USER = "Jayakrishna"
DB_PASSWORD = "root"
DB_PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

ip_hits = defaultdict(list)
BRUTE_FORCE_WINDOW = timedelta(seconds=60)  
MAX_REQUESTS_PER_IP = 5                  

def process_login_api(log):
    print(log)
    ip_match = re.search(r'^(\d+\.\d+\.\d+\.\d+)', log)
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', log)
    username_match = re.search(r'USERNAME:\s*(\S+)', log)
    
    ip = ip_match.group(1)
    timestamp_str = timestamp_match.group(1)
    username = username_match.group(1)
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    
    print(ip, timestamp, username)
    
    if username.endswith("'--"):
        print(f"SQL Injection attempt by {ip} is detected")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO THREATS (threat_id, name, ip, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (1, 'SQL_INJECTION', ip, timestamp_str))
        conn.commit()
        
        
    ip_hits[ip].append(timestamp)
    
    ip_hits[ip] = [t for t in ip_hits[ip] if t >= timestamp - BRUTE_FORCE_WINDOW]

    if len(ip_hits[ip]) > MAX_REQUESTS_PER_IP:
        print(f"🚨 Brute Force Detected: {len(ip_hits[ip])} requests from {ip} in {BRUTE_FORCE_WINDOW.total_seconds()}s")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO threats (threat_id, name, ip, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (2, 'BRUTE_FORCE', ip, timestamp_str))
        conn.commit()

def consume_login_api():
    """Consumes messages from LOGIN_API."""
    consumer = KafkaConsumer(
        'LOGIN_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    print("✅ Listening to LOGIN_API...")
    for message in consumer:
        payload = json.loads(message.value)
        raw_str = payload.get('result', {}).get('_raw', '{}')
        raw_data = json.loads(raw_str)
        line = raw_data.get('line', 'No line found')
        process_login_api(line)
        

def consume_add_user_api():
    """Consumes messages from ADD_USER_API."""
    consumer = KafkaConsumer(
        'ADD_USER_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    print("✅ Listening to ADD_USER_API...")
    for message in consumer:
        payload = json.loads(message.value)
        raw_str = payload.get('result', {}).get('_raw', '{}')
        raw_data = json.loads(raw_str)
        line = raw_data.get('line', 'No line found')
        print(line)


def consume_protected_api():
    """Consumes messages from PROTECTED_API."""
    consumer = KafkaConsumer(
        'PROTECTED_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    print("✅ Listening to PROTECTED_API...")
    for message in consumer:
        payload = json.loads(message.value)
        raw_str = payload.get('result', {}).get('_raw', '{}')
        raw_data = json.loads(raw_str)
        line = raw_data.get('line', 'No line found')
        print(line)
       
def consume_logout_api():
    """Consumes messages from LOGOUT_API."""
    consumer = KafkaConsumer(
        'LOGOUT_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    # print("✅ Listening to LOGOUT_API...")
    # for message in consumer:
    #     print(f"📥 [LOGOUT_API] Received Log: {message.value}")


def consume_home_api():
    """Consumes messages from HOME_API."""
    consumer = KafkaConsumer(
        'HOME_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    # print("✅ Listening to HOME_API...")
    # for message in consumer:
    #     print(f"📥 [HOME_API] Received Log: {message.value}")


def consume_signin_api():
    """Consumes messages from SIGNIN_API."""
    consumer = KafkaConsumer(
        'SIGNIN_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    # print("✅ Listening to SIGNIN_API...")
    # for message in consumer:
    #     print(f"📥 [SIGNIN_API] Received Log: {message.value}")


def consume_signup_api():
    """Consumes messages from SIGNUP_API."""
    consumer = KafkaConsumer(
        'SIGNUP_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    # print("✅ Listening to SIGNUP_API...")
    # for message in consumer:
    #     print(f"📥 [SIGNUP_API] Received Log: {message.value}")


def consume_profile_api():
    """Consumes messages from PROFILE_API."""
    consumer = KafkaConsumer(
        'PROFILE_API',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    # print("✅ Listening to PROFILE_API...")
    # for message in consumer:
    #     print(f"📥 [PROFILE_API] Received Log: {message.value}")


if __name__ == "__main__":
    print("🔥 Starting consumers for all 8 topics...")

    # Start each consumer in its own thread
    threading.Thread(target=consume_login_api, daemon=True).start()
    threading.Thread(target=consume_add_user_api, daemon=True).start()
    threading.Thread(target=consume_protected_api, daemon=True).start()
    threading.Thread(target=consume_logout_api, daemon=True).start()
    threading.Thread(target=consume_home_api, daemon=True).start()
    threading.Thread(target=consume_signin_api, daemon=True).start()
    threading.Thread(target=consume_signup_api, daemon=True).start()
    threading.Thread(target=consume_profile_api, daemon=True).start()

    print("🚀 All Kafka listeners started successfully! Press CTRL+C to stop.")

    # Keep the main thread alive
    while True:
        pass
