import json

import bytewax.operators as op
from bytewax import operators as op
from bytewax.connectors.kafka import (KafkaError, KafkaSink, KafkaSinkMessage,
                                      KafkaSource, KafkaSourceMessage)
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow, Stream
from confluent_kafka import OFFSET_BEGINNING
from loguru import logger

from brownbag import BROKERS, KAFKA_SINK, KAFKA_SRC, TOPIC
from brownbag.utils import decode, filter_on_key


def process(msg: dict) -> float:
    """calculate the average of the list in the input dict with key 'value'"""
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
stream = op.input("inp", flow, KAFKA_SRC)
filtered = op.filter("filter_on_key", stream, lambda x: filter_on_key(x, b"list"))
output_stream = op.map("log_the_message", filtered, decode)
processed_stream = op.map("logger", output_stream, process)
kafka_stream = op.map("to_kafka", processed_stream, to_kafka)
op.output("out", kafka_stream, KAFKA_SINK)
