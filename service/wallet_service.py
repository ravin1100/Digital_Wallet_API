import decimal
from custom_exception import CustomException
from model.transaction import Transaction
from model.user import User
from schema.wallet_schema import (
    WalletAddMoneyRequest,
    WalletAddMoneyResponse,
    WalletBalanceResponse,
    WalletWithdrawMoneyRequest,
    WalletWithdrawMoneyResponse,
)
from decimal import Decimal


def get_wallet_balance(user_id: int, db):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise CustomException(status_code=404, detail="User not found")

    return WalletBalanceResponse(
        user_id=user.id,
        balance=user.balance,
        last_updated=user.updated_at,
    )


def add_wallet_balance(user_id: int, wallet_request: WalletAddMoneyRequest, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise CustomException(status_code=404, detail="User not found")

    user.balance += Decimal(wallet_request.amount)
    db.commit()
    db.refresh(user)

    transaction = Transaction(
        user_id=user.id,
        amount=wallet_request.amount,
        transaction_type="CREDIT",
        description=wallet_request.description,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return WalletAddMoneyResponse(
        transaction_id=transaction.id,
        user_id=user.id,
        amount=wallet_request.amount,
        new_balance=user.balance,
        transaction_type="CREDIT",
    )


def withdraw_wallet_balance(
    user_id: int, wallet_request: WalletWithdrawMoneyRequest, db
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise CustomException(status_code=404, detail="User not found")

    if user.balance < wallet_request.amount:
        raise CustomException(status_code=400, detail="Insufficient balance")

    user.balance -= Decimal(wallet_request.amount)
    db.commit()
    db.refresh(user)

    transaction = Transaction(
        user_id=user.id,
        amount=wallet_request.amount,
        transaction_type="DEBIT",
        description=wallet_request.description,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return WalletWithdrawMoneyResponse(
        transaction_id=transaction.id,
        user_id=user.id,
        amount=wallet_request.amount,
        new_balance=user.balance,
        transaction_type="DEBIT",
    )
