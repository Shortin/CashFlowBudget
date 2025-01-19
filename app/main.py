from fastapi import FastAPI

from app.api import users

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# Подключаем маршруты для семей, ролей, пользователей, расходов и доходов
app.include_router(users.router, tags=["users"])
# app.include_router(budget.router, prefix="/budget", tags=["budget"])
