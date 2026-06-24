import asyncio

import psutil
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utilities.serverUtilities import cache
from loguru import logger

# Create routeur
router = APIRouter()

@router.websocket("/servers/{uuid}/hooks/console")
async def consoleHook(webSocket: WebSocket, uuid: str):
    await webSocket.accept()

    curServerManager = cache.getCurrentServerAndSm(uuid)["serverManager"]

    await curServerManager.onlineEvent.wait()
    try:
        logger.info("Server detected as online")

        if not curServerManager.server.isOnline:
            logger.error("Server is offline, cannot hook console")
            return

        logger.info(f"{uuid} successfully hooked to newLineInConsole")

        async for line_byte in curServerManager.process.stdout:
            line = line_byte.decode().strip()
            if line:
                await webSocket.send_text(line)

        await curServerManager.handleServerAutoStop()
        await webSocket.send_text("Extinction du serveur exécutée avec succès.")
        await webSocket.close(1000, f"Le serveur {uuid} est fermé")

    except WebSocketDisconnect:
        logger.error(f"Console WebSocket disconnected for {uuid}")

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
            logger.error(f"Console WebSocket disconnected for {uuid}")
            break

        except Exception as e:
            logger.error(f"Error in console WebSocket: {e}")

    await webSocket.send_json({
        "cpu": 0,
        "ram": 0
    })
    await webSocket.close(1000, f"Le serveur {uuid} est fermé")

