from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from custom_exception import CustomException
from database import get_db
from service import transaction_service


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/detail/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    try:
        return transaction_service.get_transaction_detail(
            transaction_id=transaction_id, db=db
        )
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/{user_id}")
def get_user_transactions(
    user_id: int, page: int = 1, limit: int = 10, db: Session = Depends(get_db)
):
    try:
        return transaction_service.get_user_all_transactions(
            db, user_id=user_id, page_no=page, page_size=limit
        )
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")
