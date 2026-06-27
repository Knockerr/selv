import asyncio
import psutil
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
import utilities.mcUtilities as mcUtilities
from utilities.serverUtilities import cache
from loguru import logger


# Create routeur
router = APIRouter()


@router.websocket("/servers/{uuid}/hooks/console")
async def consoleHook(webSocket: WebSocket, uuid: str):
    await webSocket.accept()

    curServerManager: mcUtilities.ServerManager = cache.getCurrentServerAndSm(uuid)["serverManager"]

    await curServerManager.onlineEvent.wait()
    queue = asyncio.Queue()
    curServerManager.subscribeToConsole(queue)
    try:
        logger.info("Server detected as online")

        if not curServerManager.server.isOnline:
            logger.error("Server is offline, cannot hook console")
            return

        logger.info(f"{uuid} successfully hooked to newLineInConsole")

        queue = asyncio.Queue()
        curServerManager.subscribeToConsole(queue)

        while True:
            line = await queue.get()
            if webSocket.client_state != WebSocketState.CONNECTED:
                logger.info("Websocket disconnected from ws")
                break
            await webSocket.send_text(line.strip())

        await curServerManager.handleServerAutoStop()
        await webSocket.send_text("Extinction du serveur exécutée avec succès.")
        curServerManager.unsubscribeConsole(queue)
        await webSocket.close(1000, f"Le serveur {uuid} est fermé")

    except WebSocketDisconnect:
        curServerManager.unsubscribeConsole(queue)
        logger.info(f"Console WebSocket disconnected for {uuid}")
        return

    except Exception as e:
        logger.error(f"Error in console WebSocket: {e}")


@router.websocket("/servers/{uuid}/hooks/metrics")
async def metricsHook(webSocket: WebSocket, uuid: str):
    await webSocket.accept()

    curServerManager = cache.getCurrentServerAndSm(uuid)["serverManager"]

    await curServerManager.onlineEvent.wait()

    logger.info(f"Passed onlineEvent for {uuid}")

    if not curServerManager.server.isOnline:
        logger.error("Server is offline, cannot hook console")
        return

    logger.info(f"{uuid} successfully hooked to metrics")

    p = psutil.Process(curServerManager.pid)

    while curServerManager.server.isOnline and p.is_running():
        try:
            cpu = round(p.cpu_percent(interval=1), 1)

            mem_info = p.memory_info()
            mem_gb = mem_info.rss / (1024 * 1024 * 1024)
            ram = f"{mem_gb:.2f}Go"

            await webSocket.send_json({
                "cpu": cpu,
                "ram": ram
            })
            await asyncio.sleep(1)

        except WebSocketDisconnect:
            logger.info(f"Console WebSocket disconnected for {uuid}")
            return

        except Exception as e:
            logger.error(f"Error in console WebSocket: {e}")

    await webSocket.send_json({
        "cpu": 0,
        "ram": 0
    })
    await webSocket.close(1000, f"Le serveur {uuid} est fermé")
