from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions.exceptions import DataNotFoundException, ForbiddenException, InvalidTokenException, InvalidTokenTypeException, InvalidUserDataException, NotAuthenticatedException


def setup_exceptions(app: FastAPI):
    @app.exception_handler(DataNotFoundException)
    async def data_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Data not found"}
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
            request: Request, exc: InvalidTokenException
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": f"Invalid token."},
            )
        
    @app.exception_handler(NotAuthenticatedException)
    async def not_authenticated_exception_handler(
            request: Request, exc: NotAuthenticatedException
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": f"Not authenticated."},
            )
        
    @app.exception_handler(InvalidTokenTypeException)
    async def invalid_token_type_exception_handler(
            request: Request, exc: InvalidTokenTypeException
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": f"Invalid token type {exc.current_token_type} expected {exc.token_type}."},
            )
    
    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(
            request: Request, exc: ForbiddenException
        ):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Forbidden."},
            )
    
    @app.exception_handler(InvalidUserDataException)
    async def invalid_user_data_exception_handler(
            request: Request, exc: InvalidUserDataException
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": f"Invalid user data."},
            )
    