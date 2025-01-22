import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import authRouter, checkSecurityRouter, usersRouter

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Используем lifespan event handler для инициализации и завершения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    logger.info("Application startup")

    # Подключаем роутеры
    app.include_router(authRouter.router)
    app.include_router(usersRouter.router)

    app.include_router(checkSecurityRouter.router)

    yield
    # Действия при остановке приложения
    logger.info("Application shutdown")


app = FastAPI(
    title="CashFlowBudget API",
    description="API для управления расходами и доходами.",
    version="1.1.0",
    lifespan=lifespan,  # Вставляем асинхронный lifespan
    docs_url="/"
)
