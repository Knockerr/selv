import asyncio
import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse

from routers import servers, websockets, tunneling, testing
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import utilities.db as dbManager
import uvicorn
import utilities.miscellaneous
from utilities import softDelete, mcUtilities, eventBuses
from utilities.miscellaneous import Stats
import os
import signal
import platformdirs as plat

from utilities.serverUtilities import cache

appDir = plat.PlatformDirs(appname="Selv", appauthor=False)
logsPath = appDir.user_data_path / "logs/backend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = asyncio.create_task(Stats.startPerfsLoop())
    yield


app = FastAPI(
    title="Selv intern API",
    description="A custom built API by Selv that manages your Minecraft servers with ease.",
    version="1.0.0",
    lifespan=lifespan,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=[
                "tauri://localhost",
                "http://tauri.localhost",
                "http://localhost:1420",  # Dev
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

app.include_router(testing.router, prefix="/test", tags=["testing"])
app.include_router(servers.router, prefix="/api", tags=["servers"])
app.include_router(tunneling.router, prefix="/api", tags=["tunneling"])
app.include_router(websockets.router, prefix="/ws", tags=["websockets"])


@app.get("/")
def root():
    return {
        "message": "A custom built API by Selv that manages your Minecraft servers with ease.",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post("/shutdown")
async def shutdown():
    # Close all running servers
    runningServersObjects: list[mcUtilities.ServerManager] = []
    for serverUuid in Stats.runningServers:
        result = cache.getCurrentServerAndSm(serverUuid)
        serverManager: mcUtilities.ServerManager = result["serverManager"]
        if serverManager.server.isOnline:
            runningServersObjects.append(serverManager)

    stopRunningServersList = [server.stopServer() for server in runningServersObjects]
    # TODO : Better error handling
    results = await asyncio.gather(*stopRunningServersList)

    async def kill():
        """
        Kills backend after a few seconds so that api call can answer before shutdown
        """
        await asyncio.sleep(0.5)
        # Closing the process in itself
        os.kill(os.getpid(), signal.SIGTERM)

    _ = asyncio.create_task(kill())
    return {"status": "Stopping.."}


@app.get("/logs/download")
async def downloadBackendLogs():
    date = datetime.datetime.now()
    dateFormatted = f"{date.year:02}-{date.month:02}-{date.day:02}"
    return FileResponse(logsPath / f"logs-{dateFormatted}.log", filename="backend.log")


@app.exception_handler(Exception)
async def exceptionHandler(request: Request, exception: Exception):
    logger.opt(exception=exception).error(f"Unhandled error on {request.method} {request.url}")
    await eventBuses.errorBus.broadcast(str(exception))
    logger.info("Broadcasting error to user")
    return JSONResponse(status_code=500, content={"detail": "Une erreur interne est survenue"})


@app.middleware("http")
async def onRequest(request: Request, call_next):
    logger.debug(f"Request received : {request.url}")
    response = await call_next(request)
    return response


if __name__ == "__main__":
    dbManager.initDb()
    softDelete.checkForTotalDeletion()
    utilities.miscellaneous.initLogger()
    uvicorn.run(app, host="127.0.0.1", port=40401, reload=False)
