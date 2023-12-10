from flask import Flask, request, jsonify, render_template
from kafka import KafkaProducer, KafkaConsumer
import numpy as np
import uuid
import json
import cv2
import base64
import os
from threading import Thread, Lock
from queue import Queue, Empty

app = Flask(__name__)

# Kafka config
KAFKA_BROKER_URL = os.getenv('KAFKA_URL')  # Kafka broker address
IMAGE_TOPIC_NAME = 'image-topic'     # Kafka image topic name
RESULT_TOPIC_NAME = 'result-topic'     # Kafka result topic name
IMAGE_MSG_MAX_SIZE = 10 * 1024 * 1024


def resize_image(image, target_size=(640, 480)):
    h, w = image.shape[:2]
    scale = max(target_size[0] / w, target_size[1] / h)

    resized_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    h, w = resized_image.shape[:2]
    startx = w//2 - target_size[0]//2
    starty = h//2 - target_size[1]//2

    return resized_image[starty:starty+target_size[1], startx:startx+target_size[0]]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image was uploaded"}), 400

    filestr = request.files['image'].read()
    npimg = np.frombuffer(filestr, np.uint8)
    img = resize_image(cv2.imdecode(npimg, cv2.IMREAD_COLOR))
    _, buffer = cv2.imencode('.jpg', img)
    base64_str = base64.b64encode(buffer.tobytes()).decode('utf-8')
    image_id = str(uuid.uuid4())

    que = Queue()

    with result_lock:
        result_buffer[image_id] = que

    message = {'id': image_id, 'base64_str': base64_str}
    _ = producer.send(IMAGE_TOPIC_NAME, message).get(timeout=10)

    print('Image id:', image_id)

    try:
        result = que.get(timeout=30)
    except Empty:
        result = 'ML nodes error (timeout)!'

    with result_lock:
        result_buffer.pop(image_id)

    return jsonify({"message": result})


def retrieve_result():
    consumer = KafkaConsumer(
        RESULT_TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id='retriever',
        auto_offset_reset='latest'
    )
    for message in consumer:
        message_data = json.loads(message.value)
        img_id = message_data['id']
        result = message_data['result']

        print('Result received:', img_id, result)

        with result_lock:
            if img_id in result_buffer:
                result_buffer[img_id].put(result)
            else:
                print('Result ignored')
        
        consumer.commit()


if __name__ == '__main__':
    if KAFKA_BROKER_URL is None:
        print('Environment var KAFKA_URL is not found')
        KAFKA_BROKER_URL = 'localhost:9092'

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        max_request_size=IMAGE_MSG_MAX_SIZE
    )

    result_buffer = {}
    result_lock = Lock()
    retrieve_thread = Thread(target=retrieve_result, daemon=True)
    retrieve_thread.start()

    app.run(debug=False, host='0.0.0.0', port='5000')
