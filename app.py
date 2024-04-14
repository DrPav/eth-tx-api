from fastapi import FastAPI
import pandas as pd
from pandasql import sqldf
from datetime import date

from logic import FILE_PATH, get_coingecko_eth_price, gas_cost_in_dollars, calculate_effective_timestamp
from models import EthTransaction, EthStats

# Use pandas and pandasql to simulate a database
eth_price = get_coingecko_eth_price(date(2023, 8, 1))
df = pd.read_csv(FILE_PATH)
df["gasCostInDollars"] = df.apply(lambda x: gas_cost_in_dollars(x["receipts_gas_used"], x["gas_price"], eth_price), axis=1)
totals = sqldf(
    """
    SELECT
        COUNT(*) as totalTransactionsInDB,
        SUM(receipts_gas_used) as totalGasUsed,
        SUM(gasCostInDollars) as totalGasCostInDollars
    FROM df
        """
)

block_totals = sqldf("SELECT block_number, COUNT(*) as txs from df group by block_number")

app = FastAPI()

@app.get("/stats")
def read_stats():
    return EthStats(**totals.to_dict(orient="records")[0]
    )

@app.get("/transactions/{hash}")
def read_item(hash: str):
    transaction_data = sqldf(f"SELECT * FROM df WHERE hash = '{hash}'").to_dict(orient="records")[0]
    block_number = transaction_data["block_number"]
    block_timestamp = pd.to_datetime(transaction_data["block_timestamp"]).to_pydatetime()
    # Calculate effective timestamp
    txs_in_block = sqldf(f"select txs from block_totals where block_number = {block_number}").to_dict(orient="records")[0]["txs"]
    effective_timestamp = calculate_effective_timestamp(block_timestamp, txs_in_block, transaction_data["transaction_index"])
    return EthTransaction(
        hash=hash,
        fromAddress=transaction_data["from_address"],
        toAddress=transaction_data["to_address"],
        blockNumber=block_number,
        executedAt=effective_timestamp.isoformat(),
        gasUsed=transaction_data["receipts_gas_used"],
        gasCostInDollars=transaction_data["gasCostInDollars"]
    )