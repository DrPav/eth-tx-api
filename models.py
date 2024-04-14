from pydantic import BaseModel

class EthTransaction(BaseModel):
    hash: str
    fromAddress: str
    toAddress: str
    blockNumber: int
    executedAt: str
    gasUsed: int
    gasCostInDollars: float

class EthStats(BaseModel):
    totalTransactionsInDB: int
    totalGasUsed: int
    totalGasCostInDollars: float