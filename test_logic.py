from datetime import date, datetime, timedelta
from logic import get_coingecko_eth_price, convert_csv_row_to_json, calculate_effective_timestamp, gas_cost_in_gwei, gas_cost_in_dollars
from logic import EXPECTED_HEADER

def test_get_coingecko_eth_price():
    # Check the API price matches one of the prices shown on the website
    close_price = 1857.28
    test_date = date(2023, 8, 1)
    assert get_coingecko_eth_price(test_date) == close_price

def test_convert_csv_row_to_json():
    # Test the header
    assert convert_csv_row_to_json(EXPECTED_HEADER) is None
    # Test a row
    test_row = "0xc055b65e39c15e1bc90cb4ccb2daac6b59c02ec1aa6c4216276054b4f31ed90a,891,0x73c053dc4b54ece7ef678a6488a56b5772c0f2e84ce28caeb566086372ac2091,17818542,0,0xd5e87f1f003f222188cc8c5aeefc8b285738b7e7,0xf24a5cc235e5242d69fafbffd304f63b92ac82f9,0,1000000,23759870228,2023-08-01 07:04:59.000000 UTC,39897781882,4507347838,2,295582,295582,,,1,23759870228"
    result = convert_csv_row_to_json(test_row)
    assert result["hash"] == "0xc055b65e39c15e1bc90cb4ccb2daac6b59c02ec1aa6c4216276054b4f31ed90a"
    assert result["nonce"] == "891"
    assert result["receipts_status"] == "1"
    assert result["receipts_contract_address"] == ""
    assert result["receipts_effective_gas_price"] == "23759870228"

def test_calcualte_effective_timestamp():
    # Test the timestamp calculation
    block_timestamp = datetime(2023, 8, 1, 9, 0, 0)
    txs_inblock = 12
    # First tx should be same as block timestamp
    assert calculate_effective_timestamp(block_timestamp, txs_inblock, 0) == block_timestamp
    # Second tx should be 1 second later
    assert calculate_effective_timestamp(block_timestamp, txs_inblock, 1) == block_timestamp + timedelta(seconds=1)

def test_gas_cost_in_gwei():
    # Test the gas cost calculation. Compare the result to etherscan
    # https://etherscan.io/tx/0xc055b65e39c15e1bc90cb4ccb2daac6b59c02ec1aa6c4216276054b4f31ed90a
    assert gas_cost_in_gwei(295582, 23759870228) == 7022989.962

def test_gas_cost_in_dollars():
    # Test the gas cost calculation. Compare the result to etherscan
    # https://etherscan.io/tx/0xc055b65e39c15e1bc90cb4ccb2daac6b59c02ec1aa6c4216276054b4f31ed90a
    # Etherescan estimates the cost as $13.15 on the day of the transaction
    assert gas_cost_in_dollars(295582, 23759870228, 1872.42) == 13.15
