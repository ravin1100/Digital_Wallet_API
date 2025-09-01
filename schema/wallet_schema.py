from datetime import datetime
from pydantic import BaseModel, Field


class WalletAddMoneyRequest(BaseModel):
    amount: float = Field(gt=0)
    description: str = Field(max_length=255)


class WalletWithdrawMoneyRequest(WalletAddMoneyRequest):
    pass


class WalletAddMoneyResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str


class WalletWithdrawMoneyResponse(WalletAddMoneyResponse):
    pass


class WalletBalanceResponse(BaseModel):
    user_id: int
    balance: float
    last_updated: datetime
