""" sender.py

Simple script that will send data to a kafka topic.
"""

import json
import random
import sys
import time

import click
from confluent_kafka import Producer
from loguru import logger

from brownbag import CONFIG, TOPIC

OPTIONS = ["simple_data", "list", "series", "test"]


@click.command()
@click.option("--data", type=click.Choice(OPTIONS), required=True)
def sender(data):
    p = Producer({"bootstrap.servers": "localhost:9092"})
    match data:
        case "simple_data":
            data = {"name": "simple_data", "value": 20}
            p.produce(topic=TOPIC, key="simple_data", value=json.dumps(data))
        case "list":
            data = {"name": "list", "value": [1, 2, 3]}
            p.produce(topic=TOPIC, key="list", value=json.dumps(data))
        case "series":
            data_points = [random.randint(0, 100) for _ in range(100)]
            for d in data_points:
                data = {"name": "series", "value": d}
                p.produce(topic=TOPIC, key="series", value=json.dumps(data))
                p.flush()
                time.sleep(0.5)
            sys.exit()
        case "test":
            data = {"name": "list", "value": [8, 9, 10]}
            p.produce(topic=TOPIC, key="test", value=json.dumps(data))
    p.flush()


if __name__ == "__main__":
    sender()
