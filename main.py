# main.py
from fastapi import FastAPI

from app.entrypoints.exceptions_handler import register_handlers
from app.entrypoints.routers import auth, category, transaction

app = FastAPI(title="aspes")
register_handlers(app)
app.include_router(category.router, prefix="/api/v1")
app.include_router(transaction.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
