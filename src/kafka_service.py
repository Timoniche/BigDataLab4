import json
import os
import threading

from kafka import KafkaConsumer, KafkaProducer

from logger import Logger


class KafkaService:
    def __init__(self):
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)

        self.kafka_servers = ["kafka:9092"]
        self.topic_name = os.environ.get('TOPIC_NAME')
        self.log.info(f'Topic name: {self.topic_name}')

        self.consumer = self.setup_consumer()
        self.producer = self.setup_producer()

    def setup_consumer(self):
        consumer = KafkaConsumer(
            bootstrap_servers=self.kafka_servers,
            value_deserializer=json.loads,
            auto_offset_reset="latest",
        )
        consumer.subscribe(self.topic_name)

        return consumer

    def setup_producer(self):
        producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        return producer

    def send(self, data: dict):
        self.log.info(f'data: {data}')

        self.producer.send(self.topic_name, data)
        self._ensure_buffer_messages_sent_to_broker()

    def register_kafka_listener(self, listener):
        def poll():
            self.consumer.poll(timeout_ms=6000)
            for msg in self.consumer:
                self.log.info(f'Listening data: {msg}, data value: {msg.value}')
                listener(msg)

        t1 = threading.Thread(target=poll)
        t1.start()
        self.log.info('Started a background CONSUMER thread')

    def _ensure_buffer_messages_sent_to_broker(self):
        self.producer.flush()
