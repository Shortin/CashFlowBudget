import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import authRouter, checkSecurityRouter, usersRouter, financesRouter

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")

    app.include_router(authRouter.router)
    app.include_router(usersRouter.router)
    # app.include_router(financesRouter.router)

    app.include_router(checkSecurityRouter.router)

    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="CashFlowBudget API",
    description="API для управления расходами и доходами.",
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/"
)
