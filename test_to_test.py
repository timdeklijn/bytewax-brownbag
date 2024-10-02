import json

import bytewax.operators as op
from bytewax.connectors.kafka import KafkaSinkMessage
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, TestingSource, run_main

from to_test import my_stream


def source():
    for i in [[1, 2, 3], [4, 5, 6]]:
        yield KafkaSinkMessage(
            key=b"test",
            value=bytes(json.dumps({"name": "testing", "value": i}), "utf-8"),
        )


def test_my_stream():
    capture = []
    flow = Dataflow("test-flow")
    stream = op.input("input", flow, TestingSource(source()))
    op.output("output", my_stream(stream), TestingSink(capture))

    run_main(flow)
    expected = [2.0, 5.0]
    for m, e in zip(capture, expected):
        assert json.loads(m.value)["value"] == e
