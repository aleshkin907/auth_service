from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from exceptions.exceptions import DataNotFoundException


def setup_exceptions(app: FastAPI):
    @app.exception_handler(DataNotFoundException)
    async def data_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Data not found"}
        )