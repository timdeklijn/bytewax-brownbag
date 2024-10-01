import json
from confluent_kafka import Producer

DATA = {"name": "simple_data", "value": 20}

producer = Producer({"bootstrap.servers":'localhost:9092'})
producer.produce(topic='test-topic', key="key", value=json.dumps(DATA))
producer.flush()
