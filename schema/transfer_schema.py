from pydantic import BaseModel


class TransferRequest(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str


class TransferResponse(BaseModel):
    transfer_id: str
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: str


class TransferErrorResponse(BaseModel):
    error: str
    current_balance: float
    required_amount: float
