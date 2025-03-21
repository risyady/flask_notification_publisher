import pika
import json
from flask import Flask, request, jsonify
from config import Config

app = Flask(__name__)

def get_rabbitmq_connection():
    params = pika.URLParameters(Config.RABBITMQ_URL)
    return pika.BlockingConnection(params)

@app.route('/publish', methods=['POST'])
def publish_message():
    try:
        data = request.json
        message = json.dumps(data)

        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Pastikan exchange ada
        channel.exchange_declare(exchange=Config.EXCHANGE_NAME, exchange_type='fanout', durable=True)

        # Publish pesan ke exchange
        channel.basic_publish(exchange=Config.EXCHANGE_NAME, routing_key='', body=message)

        connection.close()
        return jsonify({"message": "Message published successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

