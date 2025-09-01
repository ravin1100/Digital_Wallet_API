from fastapi import FastAPI

from database import create_table
from route import user_route, wallet_route, transaction_route, transfer_route

app = FastAPI(description="Digital Wallet API")


@app.on_event("startup")
def startup_event():
    create_table()


app.include_router(user_route.router)
app.include_router(wallet_route.router)
app.include_router(transaction_route.router)
app.include_router(transfer_route.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
