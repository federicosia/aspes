# entrypoints/exception_handlers.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.domain.exceptions.category import CategoryNotFound, DuplicateCategoryName


def register_handlers(app):
    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"details": str(exc)})

    @app.exception_handler(CategoryNotFound)
    async def handle_not_found(request: Request, exc: CategoryNotFound):
        return JSONResponse(status_code=404, content={"details": str(exc)})

    @app.exception_handler(DuplicateCategoryName)
    async def handle_duplicate(request: Request, exc: DuplicateCategoryName):
        return JSONResponse(status_code=409, content={"details": str(exc)})

    @app.exception_handler(Exception)
    async def handle_generic(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500, content={"details": "Internal Server Error"}
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={"details": "Validation Error"})
