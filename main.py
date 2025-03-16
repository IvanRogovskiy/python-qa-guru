import uvicorn

from models.User import User
from routers.status_router import status_router
from routers.user__router import user_router

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

users = list[User]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error"},
    )


app.include_router(user_router)
app.include_router(status_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
