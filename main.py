# main.py
from fastapi import FastAPI
from app.entrypoints.routers import category, transaction

app = FastAPI(title="aspes")

app.include_router(category.router, prefix="/api/v1")
app.include_router(transaction.router, prefix="/api/v1")
