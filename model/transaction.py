from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Numeric, String, Text
from database import Base
from sqlalchemy.orm import relationship


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    reference_transaction_id = Column(
        Integer, ForeignKey("transactions.id"), nullable=True
    )
    recipient_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", foreign_keys=[user_id], back_populates="transactions")
    reference_transaction = relationship(
        "Transaction", remote_side=[id], backref="related_transactions"
    )
    recipient_user = relationship(
        "User", foreign_keys=[recipient_user_id], backref="received_transactions"
    )
