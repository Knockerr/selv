from fastapi import APIRouter, HTTPException
from utilities.serverUtilities import cache
from utilities import mcUtilities
from pydantic import BaseModel
import utilities.serverCreator
import sqlite3
import uuid as uuidLib
from loguru import logger
import sys
import platformdirs as plat
import utilities.db as db

appDir = plat.PlatformDirs("mcPanel-DEV", "Knocker")

# Create routeur
router = APIRouter()


@router.get("/servers")
def getServersR():
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers")
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result


@router.get("/servers/{uuid}/serverListDatas")
async def getServerDatas(uuid: str):
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE UUID = ?", (uuid,))
    curServerDatas = dict(cursor.fetchone())
    conn.close()
    name = curServerDatas['name']
    type_ = curServerDatas['serverType']
    state = '...'  # TODO
    lastUse = curServerDatas['lastUseDate']
    version = curServerDatas['version']
    path = curServerDatas['path']

    return {
        'name': name,
        "type": type_,
        'state': state,
        'lastUse': lastUse,
        'version': version,
        'path': path
    }


@router.get("/servers/{uuid}/ip")
async def getServerIp(uuid: str):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    ip = curServer.getPropertiesAsDict()["server-ip"]
    port = curServer.getPropertiesAsDict()["server-port"]
    formatted: str = f"{ip}:{port} //PF"
    return {"ip": formatted}


@router.get("/servers/{uuid}/properties")
async def getServerProperties(uuid: str):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    properties = curServer.getPropertiesAsDict()
    return {"properties": properties}


@router.get("/servers/{uuid}/status")
async def getServerStatus(uuid: str):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    serverOnline = curServer.isOnline
    if serverOnline:
        return {"status": "on"}
    else:
        return {"status": "off"}


@router.get("/servers/{uuid}/logs")
async def getServerCurrentLogs(uuid: str):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    if not curServer.isOnline:
        raise HTTPException(status_code=503, detail="Serveur éteint ou indisponible")
    serverLogs = curServer.getCurrentLogs()
    return {"logs": serverLogs}


@router.post("/servers/{uuid}/start")
async def startServerR(uuid: str):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager = result["serverManager"]
    await serverManager.startServer()
    return {"status": "started", "uuid": uuid}


@router.post("/servers/{uuid}/stop")
async def stopServerR(uuid: str):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager = result["serverManager"]
    await serverManager.stopServer()
    return {"status": "stopped", "uuid": uuid}


class CommandModel(BaseModel):
    command: str


@router.post("/servers/{uuid}/sendCommand")
async def sendCommandR(uuid: str, cmd: CommandModel):
    cmd = cmd.command
    result = cache.getCurrentServerAndSm(uuid)
    serverManager = result["serverManager"]
    await serverManager.sendCommand(cmd)
    return {"status": "sent", "uuid": uuid}


class Configuration(BaseModel):
    name: str
    ram: int
    type: str
    version: str


@router.post("/servers/create")
async def createServerR(config: Configuration):
    logger.info("Server Creation Detected!")
    uuid = uuidLib.uuid4()
    utilities.serverCreator.createServer(config.name, str(uuid), config.type, config.version, config.ram)
    return {"status": "created", "uuid": str(uuid)}


class importConfig(BaseModel):
    name: str
    ram: int
    type: str
    version: str
    path: str


@router.post("/servers/import")
async def importServerR(config: importConfig):
    name = config.name
    ram = config.ram
    serverType = config.type
    version = config.version
    path = config.path

    logger.info(f"Importing server {name}")
    uuid = str(uuidLib.uuid4())
    utilities.serverCreator.importServer(name, path, ram, version, serverType, uuid)
    return {"status": "imported", "uuid": uuid}


@router.post("/servers/{uuid}/acceptEula")
async def acceptEulaR(uuid: str):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager = result["serverManager"]
    await serverManager.acceptEula()
    return {"status": "accepted", "uuid": uuid}
