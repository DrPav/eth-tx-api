from datetime import datetime, timedelta, date
import requests

FILE_PATH = 'data/ethereum_txs.csv'
EXPECTED_HEADER = 'hash,nonce,block_hash,block_number,transaction_index,from_address,to_address,value,gas,gas_price,block_timestamp,max_fee_per_gas,max_priority_fee_per_gas,transaction_type,receipts_cumulative_gas_used,receipts_gas_used,receipts_contract_address,receipts_root,receipts_status,receipts_effective_gas_price'

def get_coingecko_eth_price(historic_date: date) -> float:
    # date is in format of dd-mm-yyyy for the API
    params = {
        "date": historic_date.strftime('%d-%m-%Y'),
        "localization": False
    }
    r = requests.get("https://api.coingecko.com/api/v3/coins/ethereum/history", params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to get data from Coingecko API: {r.status_code}")
    data = r.json()
    eth_price = data["market_data"]["current_price"]["usd"]
    eth_price = round(eth_price, 2)
    return(eth_price)

def convert_csv_row_to_json(row: str) -> dict:
    row_items = row.split(",")
    columns = EXPECTED_HEADER.split(",") 
    if row_items == columns:
        return None
    data = {}
    for i, column in enumerate(columns):
        data[column] = row_items[i]
    return data

def calculate_effective_timestamp(block_timestamp: datetime, txs_inblock: int, tx_index: int):
    blocktime_seconds = 12.0
    seconds_offset = blocktime_seconds / txs_inblock * tx_index
    return block_timestamp + timedelta(seconds=seconds_offset)

def gas_cost_in_gwei(gas_used: int, gas_price: int) -> float:
    if gas_used < 1:
        raise ValueError("Gas used must be greater than 0")
    if gas_price < 0: # can gas price be zero?
        raise ValueError("Gas price must be positive")

    # Convert gas price from integer to gwei
    gas_price_gwei = gas_price * 1e-9
    return round(gas_used * gas_price_gwei, 3)

def gas_cost_in_dollars(gas_used: int, gas_price: int, eth_price: float) -> float:
    if gas_used < 1:
        raise ValueError("Gas used must be greater than 0")
    if gas_price < 0: # can gas price be zero?
        raise ValueError("Gas price must be positive")
    if eth_price < 0:
        raise ValueError("ETH price must be positive")
    
    return round(gas_used * gas_price * 1e-18* eth_price, 2)