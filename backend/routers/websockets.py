import asyncio
import time

import psutil
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from uvicorn.protocols.utils import ClientDisconnected

import utilities.mcUtilities as mcUtilities
from utilities.serverUtilities import cache
from loguru import logger
from uuid import UUID

# Create routeur
router = APIRouter()


@router.websocket("/servers/{uuid}/hooks/console")
async def consoleHook(webSocket: WebSocket, uuid: UUID):
    await webSocket.accept()

    curServerManager: mcUtilities.ServerManager = cache.getCurrentServerAndSm(uuid)["serverManager"]

    await curServerManager.onlineEvent.wait()

    logger.info("Server detected as online")

    try:
        if not curServerManager.server.isOnline:
            raise ConnectionError("Server is offline, cannot hook console")

        queue = asyncio.Queue()
        curServerManager.subscribeToConsole(queue)

        logger.info(f"{uuid} successfully hooked to console")

        async def sendLines():
            while True:
                line = await queue.get()
                if webSocket.client_state != WebSocketState.CONNECTED:
                    break
                await webSocket.send_text(line.strip())

        async def receiveCommands():
            while True:
                data = await webSocket.receive_text()
                await curServerManager.sendCommand(data)

        await asyncio.gather(sendLines(), receiveCommands())

        await curServerManager.handleServerAutoStop()
        await webSocket.send_text("Extinction du serveur exécutée avec succès.")
        await webSocket.close(1000, f"Le serveur {uuid} est fermé")
        curServerManager.unsubscribeConsole(queue)

    except WebSocketDisconnect:
        curServerManager.unsubscribeConsole(queue)
        logger.info(f"Console WebSocket disconnected for {uuid}")
        return

    except Exception as e:
        logger.error(f"Error in console WebSocket: {e}")


@router.websocket("/servers/{uuid}/hooks/metrics")
async def metricsHook(webSocket: WebSocket, uuid: UUID):
    await webSocket.accept()

    curServerManager: mcUtilities.ServerManager = cache.getCurrentServerAndSm(uuid)["serverManager"]

    await curServerManager.onlineEvent.wait()

    logger.info(f"Passed onlineEvent for {uuid}")

    if not curServerManager.server.isOnline:
        logger.error("Server is offline, cannot hook console")
        return

    logger.info(f"{uuid} successfully hooked to metrics")

    while curServerManager.server.isOnline:
        try:
            perfs = curServerManager.getPerfs()
            await webSocket.send_json(perfs)
            await asyncio.sleep(1)

        except ClientDisconnected:
            logger.info(f"Metrics WebSocket disconnected for {uuid}")
            return

        except WebSocketDisconnect:
            logger.info(f"Metrics WebSocket disconnected for {uuid}")
            return

        except Exception as e:
            logger.error(f"Error in metrics  WebSocket: {e}")

    await webSocket.send_json({
        "cpu": 0,
        "ram": 0
    })
    await webSocket.close(1000, f"Le serveur {uuid} est fermé")


@router.websocket("/servers/{uuid}/hooks/metrics")
async def metricsHook(webSocket: WebSocket, uuid: UUID):
    await webSocket.accept()

    while True:
        try:
            Ellipsis

        except WebSocketDisconnect:
            logger.info(f"Metrics WebSocket disconnected for {uuid}")
            return

        except Exception as e:
            logger.error(f"Error in metrics  WebSocket: {e}")

    await webSocket.send_json({
        "cpu": 0,
        "ram": 0
    })
    await webSocket.close(1000, f"Le serveur {uuid} est fermé")