import json

import bytewax.operators as op
from bytewax import operators as op
from bytewax.connectors.kafka import KafkaSource
from bytewax.dataflow import Dataflow, Stream
from confluent_kafka import OFFSET_BEGINNING
from loguru import logger

BROKERS = ["localhost:9092"]
IN_TOPICS = ["test-topic"]

kafka_src = KafkaSource(
    brokers=BROKERS,
    topics=IN_TOPICS,
    starting_offset=OFFSET_BEGINNING,
    tail=True,
)


def filter_stream(stream: Stream) -> bool:
    msg = stream.value.decode("utf-8")
    try:
        p = json.loads(msg)
        return True
    except json.JSONDecodeError as e:
        return False


def simply_log_it(stream: Stream) -> Stream:
    msg = stream.value.decode("utf-8")
    p = json.loads(msg)
    logger.info(f"message: {p}")


flow = Dataflow("kafka_in_out")
stream = op.input("inp", flow, kafka_src)
filtered_stream = op.filter("filter", stream, filter_stream)
output_stream = op.map("log_the_message", filtered_stream, simply_log_it)
op.inspect("inspec", output_stream)
