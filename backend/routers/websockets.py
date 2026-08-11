import asyncio
import time

from typing import Literal
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from starlette.websockets import WebSocketState
from uvicorn.protocols.utils import ClientDisconnected
from utilities.miscellaneous import Stats

import utilities.mcUtilities as mcUtilities
from utilities.serverUtilities import cache
from loguru import logger
from uuid import UUID
import utilities.eventBuses as eventBuses

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


@router.websocket("/servers/hooks/stats/serversPerfs")
async def serversPerfsHook(webSocket: WebSocket, delay: int = Query(1), label: bool = Query(False),
                           content: Literal["all", "last"] = Query("all")):
    await webSocket.accept()

    async for perf in Stats.trackPerfs(delay=delay, sendLabel=label, content=content):
        try:
            await webSocket.send_json(perf)

        except WebSocketDisconnect:
            logger.info(f"ServersPerfs WebSocket disconnected")
            break

        except Exception as e:
            logger.info(f"ServersPerfs WebSocket disconnected with exception : {e}")
            break


@router.websocket("/servers/{uuid}/state")
async def serverState(webSocket: WebSocket, uuid: UUID):
    await webSocket.accept()

    # Force creation of SM for server to have default value initialized
    result = cache.getCurrentServerAndSm(uuid)

    async def sendToClient(msg):
        await webSocket.send_text(msg)

    eventBus = eventBuses.getServerBus(uuid)
    eventBus.subscribe(sendToClient)

    try:
        while True:
            await webSocket.receive_text()
    except WebSocketDisconnect:
        eventBus.unsubscribe(sendToClient)
        logger.debug(f"Disconnected state ws for {uuid}")
    except Exception as e:
        logger.error(f"Error in state ws for {uuid} : {e}")
