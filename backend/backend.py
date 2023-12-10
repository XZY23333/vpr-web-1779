import cv2
import numpy as np
import json
import os
import base64
from kafka import KafkaProducer, KafkaConsumer
from VPRmodel import VPRmodel
from threading import Thread

# Kafka config
KAFKA_BROKER_URL = os.getenv('KAFKA_URL')  # Kafka broker address
IMAGE_TOPIC_NAME = 'image-topic'     # Kafka image topic name
RESULT_TOPIC_NAME = 'result-topic'     # Kafka result topic name

def process():
    consumer = KafkaConsumer(
        IMAGE_TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id='processor',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        message_data = json.loads(message.value)
        image_id = message_data['id']
        base64_str = message_data['base64_str']

        byte_data = base64.b64decode(base64_str)
        nparr = np.frombuffer(byte_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        print('Image id:', image_id)

        result = vpr.predict(img)

        print(result)

        message = {'id': image_id, 'result': result}

        _ = producer.send(RESULT_TOPIC_NAME, message).get(timeout=10)

        consumer.commit()

if __name__ == '__main__':
    if KAFKA_BROKER_URL is None:
        print('Environment var KAFKA_URL is not found')
        KAFKA_BROKER_URL = 'localhost:9092'

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    vpr = VPRmodel(True, 10, 'yolov5x')
    print('VRP model loaded')

    process_thread = Thread(target=process)
    process_thread.start()
