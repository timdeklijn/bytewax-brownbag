import json

import bytewax.operators as op
from bytewax.connectors.kafka import KafkaError, KafkaSinkMessage, KafkaSourceMessage
from bytewax.dataflow import Dataflow, Stream
from loguru import logger

from brownbag import KAFKA_SINK, KAFKA_SRC
from brownbag.utils import decode, filter_on_key, to_kafka


def process(msg: dict) -> float:
    """calculate the average of the list in the input dict with key 'value'"""
    logger.info(f"list: {msg['value']}")
    avg = float(sum(msg["value"]) / len(msg["value"]))
    logger.info(f"avg: {avg}")
    return avg


def my_stream(stream):
    filtered = op.filter("filter_on_key", stream, lambda x: filter_on_key(x, b"test"))
    op.inspect("inspect", filtered)
    output_stream = op.map("decode", filtered, decode)
    processed_stream = op.map("averager", output_stream, process)
    return op.map("to_kafka", processed_stream, to_kafka)


flow = Dataflow("to_test")
stream = op.input("inp", flow, KAFKA_SRC)
op.output("out", my_stream(stream), KAFKA_SINK)


# "       KafkaSourceMessage[bytes | None, bytes | None] | KafkaError[bytes | None, bytes | None]" is incompatible with type
# "Stream[KafkaSourceMessage[bytes | None, bytes | None] | KafkaError[bytes | None, bytes | None]]"

# "KafkaSinkMessage[bytes | None, bytes | None]" is not the same as
# "Stream[KafkaSinkMessage[Unknown, Unknown]]"
