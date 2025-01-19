from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
from app.api import usersApi, financeApi
from contextlib import asynccontextmanager

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Используем lifespan event handler для инициализации и завершения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    logger.info("Application startup")

    yield

    # Действия при остановке приложения
    logger.info("Application shutdown")


# Создаем приложение FastAPI и указываем lifespan
app = FastAPI(
    title="CashFlowBudget API",
    description="API для управления расходами и доходами.",
    version="1.0.0",
    lifespan=lifespan
)

# Правильное добавление CORS middleware
app.add_middleware(
    CORSMiddleware,  # Здесь передаем сам класс без создания экземпляра
    allow_origins=["*"],  # Разрешает доступ с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все HTTP-методы
    allow_headers=["*"],  # Разрешает все заголовки
)

# Подключаем роутеры
app.include_router(usersApi.router, tags=["users"])
app.include_router(financeApi.router, tags=["finance"])


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
