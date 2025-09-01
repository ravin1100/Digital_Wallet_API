import http
from fastapi import APIRouter, HTTPException

from custom_exception import CustomException
from database import get_db
from schema.user_schema import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Depends

from service import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=http.HTTPStatus.CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(user, db)
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user(user_id, db)
    except Exception as e:
        print(e)
        if isinstance(e, CustomException):
            raise e
        raise HTTPException(status_code=500, detail="Something went wrong")
