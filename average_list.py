import json

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from loguru import logger

from brownbag import KAFKA_SINK, KAFKA_SRC
from brownbag.utils import decode, filter_on_key, to_kafka


def process(msg: dict) -> float:
    """calculate the average of the list in the input dict with key 'value'"""
    logger.info(f"list: {msg['value']}")
    avg = float(sum(msg["value"]) / len(msg["value"]))
    logger.info(f"avg: {avg}")
    return avg


flow = Dataflow("list_averager")
stream = op.input("inp", flow, KAFKA_SRC)
filtered = op.filter("filter_on_key", stream, lambda x: filter_on_key(x, b"list"))
output_stream = op.map("log_the_message", filtered, decode)
processed_stream = op.map("averager", output_stream, process)
kafka_stream = op.map("to_kafka", processed_stream, to_kafka)
op.output("out", kafka_stream, KAFKA_SINK)
