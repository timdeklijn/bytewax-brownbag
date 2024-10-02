import json

from bytewax.connectors.kafka import KafkaError, KafkaSourceMessage
from loguru import logger


def filter_on_key(
    msg: (
        KafkaSourceMessage[bytes | None, bytes | None]
        | KafkaError[bytes | None, bytes | None]
    ),
    key: bytes,
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


def decode(
    msg: (
        KafkaSourceMessage[bytes | None, bytes | None]
        | KafkaError[bytes | None, bytes | None]
    )
) -> dict:
    """Decode a json value from a kafka message."""
    if isinstance(msg, KafkaError):
        logger.error(f"Error: {msg}")
        return {}
    if msg.value is None:
        logger.error(f"Error: value is None")
        return {}
    decoded_message = msg.value.decode("utf-8")
    return json.loads(decoded_message)
