from datetime import date
import json

from logic import FILE_PATH, convert_csv_row_to_json, get_coingecko_eth_price, gas_cost_in_dollars

import bytewax.operators as op
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow
from bytewax.connectors.files import FileSource

flow = Dataflow("ethereum_transactions")

input = op.input("input", flow, FileSource(FILE_PATH))

stream = op.map("parse_csv", input, convert_csv_row_to_json)
stream = op.filter("skip_header", stream, lambda x: x is not None)

# Use a single approx eth price as all the data is from the same date and the api only gives daily data
# Otherwise we could create a stream of prices
eth_price = get_coingecko_eth_price(date(2023, 8, 1))
def add_add_gas_cost_in_dollars(row: dict) -> dict:
    gas_used = int(row["receipts_gas_used"])
    gas_price = int(row["gas_price"])
    row["gas_cost_in_dollars"] = gas_cost_in_dollars(gas_used, gas_price, eth_price)
    return row

stream = op.map("add_gas_cost", stream, add_add_gas_cost_in_dollars)

op.output("out", stream, StdOutSink())


