from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import servers, websockets

app = FastAPI(
    title="Minecraft Panel API",
    description="API pour gérer vos serveurs Minecraft",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
