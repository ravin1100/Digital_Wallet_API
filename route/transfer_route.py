import http
from fastapi import APIRouter, HTTPException

from custom_exception import CustomException
from database import get_db
from schema.transfer_schema import TransferRequest
from sqlalchemy.orm import Session
from fastapi import Depends

from service import transfer_service


router = APIRouter(prefix="/transfer", tags=["Transfer"])


@router.post("/", status_code=http.HTTPStatus.CREATED)
def create_transfer(transfer_request: TransferRequest, db: Session = Depends(get_db)):
    try:
        return transfer_service.create_transfer(transfer_request, db)
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")
