# entrypoints/exception_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from domain.exceptions.category import CategoryNotFound, DuplicateCategoryName


def register_handlers(app):
    @app.exception_handler(CategoryNotFound)
    def handle_not_found(request: Request, exc: CategoryNotFound):
        return JSONResponse(status_code=404, content={"details": str(exc)})

    @app.exception_handler(DuplicateCategoryName)
    def handle_duplicate(request: Request, exc: DuplicateCategoryName):
        return JSONResponse(status_code=409, content={"details": str(exc)})
