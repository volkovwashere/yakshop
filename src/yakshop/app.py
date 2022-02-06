from fastapi import FastAPI
from yakshop.utils.custom_logger import CustomLogger
from yakshop.utils.config import get_root_path
from yakshop.routes import yak_shop
import uvicorn
import os
import datetime


app = FastAPI(
    title="YakShop App",
    description="An honest Yak business.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router=yak_shop.router, prefix="/yak-shop")


@app.get("/", tags=["Root"])
async def get_root():
    return {"status_code": 200}


logger = CustomLogger.construct_logger(
    name="classifier",
    log_file_path=os.path.join(get_root_path(), "logs/app.log"),
    logger_level=20,
)
logger.log_info(
    f"At {datetime.datetime.now()} started running server at host: 127.0.0.0, port: 8000"
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
