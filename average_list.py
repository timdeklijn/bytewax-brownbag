import json

import bytewax.operators as op
from bytewax import operators as op
from bytewax.connectors.kafka import (KafkaError, KafkaSink, KafkaSinkMessage,
                                      KafkaSource, KafkaSourceMessage)
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow, Stream
from confluent_kafka import OFFSET_BEGINNING
from loguru import logger

BROKERS = ["localhost:9092"]
TOPICS = ["test-topic"]

kafka_src = KafkaSource(
    brokers=BROKERS,
    topics=TOPICS,
    starting_offset=OFFSET_BEGINNING,
    tail=True,
)


# TODO: move this into some shared file
def filter_on_key(
    msg: (
        KafkaSourceMessage[bytes | None, bytes | None]
        | KafkaError[bytes | None, bytes | None]
    )
) -> bool:
    """filter on key"""
    if isinstance(msg, KafkaError):
        logger.error(f"Error: {msg}")
        return False
    if msg.value is None:
        logger.error(f"Error: value is None")
        return False
    if msg.key != b"list":
        return False
    return True


# TODO: move this into some shared file
def decode(
    msg: (
        KafkaSourceMessage[bytes | None, bytes | None]
        | KafkaError[bytes | None, bytes | None]
    )
) -> dict:
    if isinstance(msg, KafkaError):
        logger.error(f"Error: {msg}")
        return {}
    if msg.value is None:
        logger.error(f"Error: value is None")
        return {}
    decoded_message = msg.value.decode("utf-8")
    return json.loads(decoded_message)


def process(msg: dict) -> float:
    logger.info(f"list: {msg['value']}")
    avg = float(sum(msg["value"]) / len(msg["value"]))
    logger.info(f"avg: {avg}")
    return avg


def to_kafka(msg: float) -> KafkaSinkMessage:
    """Convert a feature event (bytes) to a KafkaSinkMessage"""
    return KafkaSinkMessage(
        key="avg_out", value=json.dumps({"name": "average", "value": msg})
    )


flow = Dataflow("list_averager")
stream = op.input("inp", flow, kafka_src)
filtered = op.filter("filter_on_key", stream, filter_on_key)
output_stream = op.map("log_the_message", filtered, decode)
processed_stream = op.map("logger", output_stream, process)
kafka_stream = op.map("to_kafka", processed_stream, to_kafka)
op.output("out", kafka_stream, KafkaSink(brokers=BROKERS, topic=TOPICS[0]))
