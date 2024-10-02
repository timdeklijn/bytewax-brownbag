import datetime
import json

import bytewax.operators as op
import bytewax.operators.windowing as win
from bytewax.dataflow import Dataflow

from brownbag import ALIGN_TO, KAFKA_SINK, KAFKA_SRC
from brownbag.utils import decode, filter_on_key, get_time, to_kafka


def add_timestamp(x: dict) -> dict:
    x["time"] = datetime.datetime.now(tz=datetime.timezone.utc)
    return x


def process(msg: tuple[str, tuple[int, list[dict]]]) -> list:
    print(msg)
    l = msg[1][1]
    return [sum([i["value"] for i in l]) / len(l), len(l)]


# Create a flow like normal
flow = Dataflow("series")
stream = op.input("inpupt", flow, KAFKA_SRC)
filtered = op.filter("filter-on-key", stream, lambda x: filter_on_key(x, b"series"))
decoded_stream = op.map("decode-the-stream", filtered, decode)

# Add timestamp to the stream so we can create a window
timed_stream = op.map("add-timestamp", decoded_stream, add_timestamp)

# We need a key, for not keep the key the same for all messages
keyed_stream = op.key_on("key-stream", timed_stream, lambda x: x["name"])

# A clock is needed to window on
clock = win.EventClock(
    get_time, wait_for_system_duration=datetime.timedelta(seconds=0.1)
)

# A sliding window groups the messages in time windows, this window overlaps
windower = win.SlidingWindower(
    length=datetime.timedelta(seconds=2),
    offset=datetime.timedelta(seconds=1),
    align_to=ALIGN_TO,
)

# Finally collect the windows
win_out = win.collect_window("collect-window", keyed_stream, clock, windower)

# For each window, process the data
win_processed = op.map("process-window", win_out.down, process)

# Send the results back to the stream
kafka_stream = op.map("to_kafka", win_processed, to_kafka)
op.output("out", kafka_stream, KAFKA_SINK)
