""" sender.py

Simple script that will send data to a kafka topic.
"""

import json

import click
from confluent_kafka import Producer
from loguru import logger

from brownbag import CONFIG, TOPIC

OPTIONS = ["simple_data", "list"]


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
    p.flush()


if __name__ == "__main__":
    sender()
