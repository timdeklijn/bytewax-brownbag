import bytewax.operators as op
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow

from brownbag import KAFKA_SRC
from brownbag.utils import decode

flow = Dataflow("kafka_in_out")
stream = op.input("inp", flow, KAFKA_SRC)
output_stream = op.map("decode-message", stream, decode)
op.output("out", output_stream, StdOutSink())
