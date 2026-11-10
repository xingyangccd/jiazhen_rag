from contextlib import asynccontextmanager
from urllib.request import Request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.agents.insurance_advisor import init_insurance_agent
import app
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.modules.chat_thread.exceptions import ChatThreadNotFoundError
from  app.modules.product.router import  router as product_router
from app.modules.chat_thread.router import router as chat_thread_router
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError
from app.modules.product.router import list_products
import sys
from app.infra.checkpointer import (
    close_checkpointer,
    init_checkpointer,
)
# 初始化日志系统
configure_logging(settings.logging.level)
logger = get_logger(__name__)

# @asynccontextmanager
# async  def lifespan(app: FastAPI):
#     logger.info("项目正在初始化")
#     from app.infra.database import close_database, check_database
#     try:
#         await check_database()
#         yield
#     finally:
#         logger.info("应用关闭中... ")
#         await close_database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"【{settings.app.name}】应用启动中...")

    from app.infra.database import check_database, close_database

    try:
        # 1.检查业务数据库连接
        await check_database()

        # 2.初始化Checkpointer
        checkpointer = await init_checkpointer()

        # 3.初始化保险顾问Agent
        app.state.agent = init_insurance_agent(checkpointer)

        yield
    finally:
        logger.info("应用关闭中... ")

        # 4.关闭Checkpointer连接池
        await close_checkpointer()

        # 5.关闭SQLAlchemy连接池
        await close_database()


# 统一处理异常信息，发现是ChatThreadNotFoundError，返回对应的错误状态码和错误信息
@app.exception_handler(ChatThreadNotFoundError)
def handle_exception(request: Request, exc: Exception):
    logger.error(f"处理异常, 请求路径: {request.url}, 异常信息: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "code": "CHAT_THREAD_NOT_FOUND",
            "message": "会话不存在或者不属于当前用户"
        }
    )


@app.exception_handler(ApplicationError)
async def handle_application_error(
    request: Request,
    exc: ApplicationError, # 捕获到的异常（这里用自定义异常基类捕获，所有业务异常都会匹配到）
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, # 异常中自带status
        content={
            "code": exc.code,        # 异常中自带code
            "message": exc.message,  # 异常中自带message
        },
    )
app = FastAPI(
    title=settings.app.name,
    debug=settings.app.debug,
    lifespan=lifespan
)
app.include_router(product_router)
app.include_router(chat_thread_router)



@app.get("/health", summary="健康检测接口")
async def health_check() -> dict[str, str]:
    logger.info("执行健康检查")
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=False,
        loop= "asyncio:SelectorEventLoop" if sys.platform == "win32" else "auto",
    )