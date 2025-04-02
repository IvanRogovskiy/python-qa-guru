import dotenv

dotenv.load_dotenv()

from app.database.engine import create_db_and_table

import uvicorn

from app.models.User import User
from app.routers.status_router import status_router
from app.routers.user__router import user_router
from fastapi_pagination import add_pagination

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
add_pagination(app)

if __name__ == "__main__":
    create_db_and_table()
    uvicorn.run(app, host="localhost", port=8080)
