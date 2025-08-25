
# from flask import Flask, request, jsonify
# from kafka import KafkaProducer
# import json
# from datetime import datetime

# app = Flask(__name__)

# # Kafka Configuration
# KAFKA_BROKER = 'kafka:9093'  # Update if running Kafka on a different host
# KAFKA_TOPIC = 'logs'

# # Initialize Kafka Producer
# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BROKER,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# @app.route('/webhook', methods=['POST'])
# def webhook_listener():
#     if request.method == 'POST':
#         try:
#             # Get log data from request
#             log_data = request.json
#             if not log_data:
#                 return jsonify({"error": "No data received"}), 400
            
#             # Print received logs with timestamp
#             print(f"[{datetime.now()}] - Received Log:")
#             print(json.dumps(log_data, indent=4))

#             # Publish log to Kafka topic
#             producer.send(KAFKA_TOPIC, log_data)
#             producer.flush()

#             print(f"Log published to Kafka topic '{KAFKA_TOPIC}' successfully")

#             # Acknowledge receipt
#             return jsonify({"message": "Log received and published to Kafka successfully"}), 200
        
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return jsonify({"error": "Internal Server Error"}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
from datetime import datetime

app = Flask(__name__)

# Kafka Configuration
KAFKA_BROKER = 'kafka:9093'  # Update if running Kafka on a different host

# Valid Kafka topics
TOPICS = {
    "LOGIN_API",
    "ADD_USER_API",
    "PROTECTED_API",
    "LOGOUT_API",
    "HOME_API",
    "SIGNIN_API",
    "SIGNUP_API",
    "PROFILE_API",
}

# Initialize Kafka Producers for each topic
producers = {
    topic: KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    for topic in TOPICS
}


# Generic Webhook Endpoint to Handle All Routes
@app.route('/webhook/<action>', methods=['POST'])
def webhook_listener(action):
    try:
        # Check if the action is a valid Kafka topic
        topic_name = action.upper()  # Convert to uppercase to ensure case-insensitivity

        if topic_name not in TOPICS:
            return jsonify({"error": f"Invalid topic '{topic_name}'"}), 404

        # Get log data from request
        log_data = request.json
        if not log_data or not isinstance(log_data, dict):
            return jsonify({"error": "Invalid or no data received"}), 400

        # Add metadata to log data
        log_data.update({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "api_title": topic_name,
        })

        # Print received log with metadata
        print(f"[{log_data['timestamp']}] - Received Log: {json.dumps(log_data, indent=4)}")

        # Send log to respective Kafka topic
        producer = producers[topic_name]
        producer.send(topic_name, log_data)
        producer.flush()

        print(f"Log published to Kafka topic '{topic_name}' successfully")

        # Acknowledge receipt
        return jsonify({"message": f"Log received and published to '{topic_name}' successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)