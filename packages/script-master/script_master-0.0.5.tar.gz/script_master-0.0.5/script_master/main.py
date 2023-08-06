from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from script_master import const
from script_master.logger import logger
from script_master.service import scheduler
from script_master.settings import Settings
from script_master.utils import run_in_background_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("===== Script Master =====")
    logger.info(f"HOME DIRECTORY: {const.get_homepath()}")
    # logger.info(f"Swagger: http://{}:{}/docs")
    # logger.info(f"Api docs: http://{}:{}/redoc\n")

    for k, v in Settings().dict().items():
        logger.info(f"{k.upper()}={v}")

    const.get_homepath().mkdir(exist_ok=True)
    Path(Settings().VARIABLES_DIR).mkdir(exist_ok=True)
    Path(Settings().NOTEBOOK_DIR).mkdir(exist_ok=True)
    Path(Settings().ARCHIVE_NOTEBOOK_DIR).mkdir(exist_ok=True)
    Path(Settings().LOGS_DIR).mkdir(exist_ok=True)

    run_in_background_task(scheduler())

    yield


app = FastAPI(debug=Settings().debug, lifespan=lifespan)


if __name__ == "__main__":
    # Run debug.
    server = uvicorn.Server(
        Settings().for_uvicorn(
            app=app, host="localhost", port=const.DEFAULT_PORT, reload=True
        )
    )
    server.run()
