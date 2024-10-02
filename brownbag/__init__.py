import datetime

from bytewax.connectors.kafka import KafkaSink, KafkaSource
from confluent_kafka import OFFSET_BEGINNING

BROKERS = ["localhost:9092"]
TOPIC = "test-topic"
TOPICS = [TOPIC]
CONFIG = {"bootstrap.servers": "localhost:9092"}

KAFKA_SINK = KafkaSink(brokers=BROKERS, topic=TOPIC)

KAFKA_SRC = KafkaSource(
    brokers=BROKERS,
    topics=TOPICS,
    starting_offset=OFFSET_BEGINNING,
    tail=True,
)

ALIGN_TO = datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc)
