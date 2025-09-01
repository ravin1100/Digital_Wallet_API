from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TransactionBaseResponse(BaseModel):
    transaction_id: int
    transaction_type: str
    amount: float
    description: str
    created_at: datetime


class TransactionsListResponse(BaseModel):
    transactions: list[TransactionBaseResponse]
    total: int
    page: int
    limit: int


class TransactionDetailResponse(TransactionBaseResponse):
    user_id: int
    recipient_user_id: Optional[int] = None
    reference_transaction_id: Optional[int] = None
