from custom_exception import CustomException
from model.transaction import Transaction
from model.user import User
from schema.transfer_schema import TransferRequest, TransferResponse
from decimal import Decimal
import uuid


def create_transfer(transfer_request: TransferRequest, db):

    sender = db.query(User).filter(User.id == transfer_request.sender_user_id).first()
    if not sender:
        raise CustomException(status_code=404, detail="Sender user not found")

    recipient = (
        db.query(User).filter(User.id == transfer_request.recipient_user_id).first()
    )
    if not recipient:
        raise CustomException(status_code=404, detail="Recipient user not found")

    if sender.balance < transfer_request.amount:
        raise CustomException(status_code=400, detail="Insufficient balance")

    # Process the transfer
    sender.balance -= Decimal(transfer_request.amount)
    recipient.balance += Decimal(transfer_request.amount)

    db.commit()
    db.refresh(sender)
    db.refresh(recipient)

    # record transaction for sender
    sender_transaction = Transaction(
        user_id=sender.id,
        recipient_id=recipient.id,
        amount=Decimal(transfer_request.amount),
        description=transfer_request.description,
        transaction_type="TRANSFER_OUT",
    )
    db.add(sender_transaction)
    db.commit()
    db.refresh(sender_transaction)

    # record transaction for receiver
    receiver_transaction = Transaction(
        user_id=recipient.id,
        recipient_id=sender.id,
        amount=Decimal(transfer_request.amount),
        description=transfer_request.description,
        transaction_type="TRANSFER_IN",
    )
    db.add(receiver_transaction)
    db.commit()
    db.refresh(receiver_transaction)

    db.commit()
    db.refresh(sender)
    db.refresh(recipient)

    return TransferResponse(
        transfer_id=str(uuid.uuid4()),
        sender_transaction_id=sender_transaction.id,
        recipient_transaction_id=receiver_transaction.id,
        amount=transfer_request.amount,
        sender_new_balance=sender.balance,
        recipient_new_balance=recipient.balance,
        status="completed",
    )
