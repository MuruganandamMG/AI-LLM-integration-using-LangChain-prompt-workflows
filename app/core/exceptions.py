from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class PlatformException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

async def platform_exception_handler(request: Request, exc: PlatformException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.message}
    )
