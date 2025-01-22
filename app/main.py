import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import authRouter
from app.db.session import get_sessions

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
    app.state.db = get_sessions()  # Сохраняем сессию в state

    # Подключаем роутеры
    # app.include_router(usersApi.router, tags=["users"])
    # app.include_router(financeApi.router, tags=["finance"])
    app.include_router(authRouter.router)

    # Инициализация асинхронных соединений, если необходимо
    # Например: создание асинхронных подключений к базе данных
    # engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URL)
    # или любые другие ресурсы

    yield

    # Действия при остановке приложения
    logger.info("Application shutdown")

    # Закрытие асинхронных соединений и освобождение ресурсов
    # Пример: engine.dispose()


# Создаем приложение FastAPI и указываем lifespan

# Правильное добавление CORS middleware

app = FastAPI(
    title="CashFlowBudget API",
    description="API для управления расходами и доходами.",
    version="1.1.0",
    lifespan=lifespan,  # Вставляем асинхронный lifespan
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware,  # Здесь передаем сам класс без создания экземпляра
    allow_origins=["*"],  # Разрешает доступ с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все HTTP-методы
    allow_headers=["*"],  # Разрешает все заголовки
)
