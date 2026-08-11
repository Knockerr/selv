import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import servers, websockets
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import utilities.db as dbManager
import uvicorn
import utilities.miscellaneous
from utilities import softDelete
from utilities.miscellaneous import Stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = asyncio.create_task(Stats.startPerfsLoop())
    yield


app = FastAPI(
    title="Minecraft Panel API",
    description="API pour gérer vos serveurs Minecraft",
    version="1.0.0",
    lifespan=lifespan,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

app.include_router(servers.router, prefix="/api", tags=["servers"])
app.include_router(websockets.router, prefix="/ws", tags=["websockets"])


@app.get("/")
def root():
    return {
        "message": "Minecraft Panel API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    dbManager.initDb()
    softDelete.checkForTotalDeletion()
    utilities.miscellaneous.initLogger()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
