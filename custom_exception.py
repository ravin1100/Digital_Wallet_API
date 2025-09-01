from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, status_code: int = 400, detail: str = "Something Went Wrong"):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail
