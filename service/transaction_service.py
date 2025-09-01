from custom_exception import CustomException
from model.transaction import Transaction
from schema.transaction_schema import (
    TransactionBaseResponse,
    TransactionDetailResponse,
    TransactionsListResponse,
)


def get_transaction_detail(transaction_id: int, db):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise CustomException(status_code=404, detail="Transaction not found")

    return TransactionDetailResponse(
        transaction_id=transaction.id,
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        # recipient_user_id=transaction.recipient_user_id,
        # reference_transaction_id=transaction.reference_transaction_id,
        created_at=transaction.created_at,
    )


def get_user_all_transactions(db, user_id: int, page_no: int = 1, page_size: int = 10):
    if page_no < 1:
        page_no = 1

    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .offset((page_no - 1) * page_size)
        .limit(page_size)
        .all()
    )

    total = db.query(Transaction).filter(Transaction.user_id == user_id).count()

    return TransactionsListResponse(
        transactions=[
            TransactionBaseResponse(
                transaction_id=tx.id,
                transaction_type=tx.transaction_type,
                amount=tx.amount,
                description=tx.description,
                created_at=tx.created_at,
            )
            for tx in transactions
        ],
        total=total,
        page=page_no,
        limit=page_size,
    )
