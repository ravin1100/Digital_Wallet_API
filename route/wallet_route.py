import http
from fastapi import APIRouter, HTTPException

from custom_exception import CustomException
from database import get_db
from schema.user_schema import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Depends

from schema.wallet_schema import WalletAddMoneyRequest, WalletWithdrawMoneyRequest
from service import wallet_service


router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get("/{user_id}/balance", status_code=http.HTTPStatus.OK)
def get_user_balance(user_id: int, db: Session = Depends(get_db)):
    try:
        return wallet_service.get_wallet_balance(user_id, db)
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/{user_id}/add-money", status_code=http.HTTPStatus.CREATED)
def add_user_balance(
    user_id: int, wallet_request: WalletAddMoneyRequest, db: Session = Depends(get_db)
):
    try:
        return wallet_service.add_wallet_balance(user_id, wallet_request, db)
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/{user_id}/withdraw", status_code=http.HTTPStatus.CREATED)
def withdraw_user_balance(
    user_id: int,
    wallet_request: WalletWithdrawMoneyRequest,
    db: Session = Depends(get_db),
):
    try:
        return wallet_service.withdraw_wallet_balance(user_id, wallet_request, db)
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")
