import uvicorn

from models.User import User
from routers.user__router import user_router

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# from routers.user import app

app = FastAPI()

users = list[User]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error"},
    )


app.include_router(user_router)

# @app.get("/")
# def get__user():
#     return 123
#
#
# @app.post("/api/users")
# def create__user(user: User):
#     user_dict = {
#         "id": user.id,
#         "name": user.name,
#         "email": user.email
#     }
#
#     with open('users.json', 'w') as file:
#         json.dump(user_dict, file)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
