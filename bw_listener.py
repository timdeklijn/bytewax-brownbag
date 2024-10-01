import json

import bytewax.operators as op
from bytewax import operators as op
from bytewax.connectors.kafka import (KafkaError, KafkaSource,
                                      KafkaSourceMessage)
from bytewax.connectors.stdio import StdOutSink
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


def decode(
    msg: (
        KafkaSourceMessage[bytes | None, bytes | None]
        | KafkaError[bytes | None, bytes | None]
    )
) -> dict:
    """Decodes the Kafka message or error into a dictionary."""
    if isinstance(msg, KafkaError):
        logger.error(f"Error: {msg}")
        return {}
    if msg.value is None:
        return {}
    decoded_message = msg.value.decode("utf-8")
    return json.loads(decoded_message)


def log_it(msg: dict) -> dict:
    """Logs the message and returns it."""
    logger.info(f"message: {json.dumps(msg, indent=2)}")
    return msg


flow = Dataflow("kafka_in_out")
stream = op.input("inp", flow, kafka_src)
output_stream = op.map("log_the_message", stream, decode)
logged_stream = op.map("logger", output_stream, log_it)
op.output("out", logged_stream, StdOutSink())
