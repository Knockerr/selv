import asyncio
import pathlib

from fastapi import APIRouter, HTTPException

from utilities.serverUtilities import cache
from utilities.miscellaneous import Stats
from utilities import mcUtilities, softDelete
from pydantic import BaseModel
import utilities.serverCreator
import sqlite3
import uuid as uuidLib
from loguru import logger
import sys
import platformdirs as plat
import utilities.db as db
import utilities.tunneling as tunneling
from uuid import UUID

appDir = plat.PlatformDirs(appname="Selv", appauthor=False)
serversPath = appDir.user_data_path / "servers"

# Create routeur
router = APIRouter()


# ==========================================
# ================== GET ===================
# ==========================================

@router.get("/serversPerfs")
def getServersPerfsR():
    return {"perfs": Stats.averagePerfs}


@router.get("/deletedServers")
def getDeletedServers():
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deletedServers")
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"deletedServers": result}


@router.get("/deletedServers/{uuid}/datas")
def getDeletedServersR(uuid: UUID):
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deletedServers WHERE uuid=?", (str(uuid),))
    result = cursor.fetchone()
    conn.close()
    return {"datas": result}


@router.get("/servers")
def getServersR():
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activeServers")
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"servers": result}


@router.get("/servers/runningServers")
def getRunningServersR():
    runingServersStr = []
    for s in Stats.runningServers:
        runingServersStr.append(str(s))
    return {"runningServers": runingServersStr}


@router.get("/servers/localPath")
def getLocalPathR():
    return {"serversPath": str(serversPath)}


@router.get("/servers/stats/serversTypes")
def getServersTypesR():
    serversTypes = Stats.getServersTypesDstrib()
    return {"serversTypes": serversTypes}


@router.get("/servers/stats/totalUptime")
def getServersTotalUptimeR():
    totalUptime = Stats.getServersTotalUptime()
    return {"totalUptime": totalUptime}


@router.get("/servers/stats/serversUptimes")
def getServersUptimeR():
    serversUptimes = Stats.getServersUptime()
    return {"serversUptimes": serversUptimes}


@router.get("/servers/{uuid}/serverListDatas")
async def getServerDatas(uuid: UUID):
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activeServers WHERE UUID = ?", (str(uuid),))
    curServerDatas = dict(cursor.fetchone())
    conn.close()
    name = curServerDatas['name']
    type_ = curServerDatas['server_type']
    state = '...'  # TODO
    lastUse = curServerDatas['last_use_date']
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


@router.get("/servers/{uuid}/datas")
def getServerDatasR(uuid: UUID):
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE uuid=?", (str(uuid),))
    result = cursor.fetchone()
    conn.close()
    return {"datas": result}


@router.get("/servers/{uuid}/creationStep")
async def getCreationStep(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    creationStep = curServer.getCreationStep()
    return {"creationStep": creationStep}


@router.get("/servers/{uuid}/creationStep")
async def getCreationStep(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    creationStep = curServer.getCreationStep()
    return {"creationStep": creationStep}


@router.get("/servers/{uuid}/propertiesInfos")
async def getPropertiesInfos(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    path = curServer.propertiesPath
    exist = path and pathlib.Path(path).exists()
    return {"path": path, "exist": exist}


@router.get("/servers/{uuid}/ip")
async def getServerIp(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    ip = curServer.getPropertiesAsDict()["server-ip"]
    port = curServer.getPropertiesAsDict()["server-port"]
    formatted: str = f"{ip}:{port} //PF"
    return {"ip": formatted}


@router.get("/servers/{uuid}/name")
async def getServerName(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    return {"name": curServer.name}


@router.get("/servers/{uuid}/properties")
async def getServerProperties(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    properties = curServer.getPropertiesAsDict()
    return {"properties": properties}


@router.get("/servers/{uuid}/status")
async def getServerStatus(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    serverOnline = curServer.isOnline
    if serverOnline:
        return {"status": "on"}
    else:
        return {"status": "off"}


@router.get("/servers/{uuid}/logs")
async def getServerCurrentLogs(uuid: UUID):
    curServer: mcUtilities.Server = cache.getCurrentServerAndSm(uuid)["server"]
    if not curServer.isOnline:
        raise HTTPException(status_code=503, detail="Serveur éteint ou indisponible")
    serverLogs = curServer.getCurrentLogs()
    return {"logs": serverLogs}


# ==========================================
# ================== POST ==================
# ==========================================

@router.post("/servers/stopAll")
async def stopAllR():
    for serverUuid in Stats.runningServers:
        result = cache.getCurrentServerAndSm(serverUuid)
        serverManager: mcUtilities.ServerManager = result["serverManager"]
        if serverManager.server.isOnline:
            _ = asyncio.create_task(serverManager.stopServer())
    return {"status": "stopped"}


@router.post("/servers/{uuid}/start")
async def startServerR(uuid: UUID):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    _ = asyncio.create_task(serverManager.startServer())
    return {"status": "started", "uuid": uuid}


@router.post("/servers/{uuid}/restart")
async def restartServerR(uuid: UUID):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    _ = asyncio.create_task(serverManager.restartServer())
    return {"status": "restarted", "uuid": uuid}


@router.post("/servers/{uuid}/stop")
async def stopServerR(uuid: UUID):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    await serverManager.stopServer()
    return {"status": "stopped", "uuid": uuid}


class Configuration(BaseModel):
    name: str
    ram: int
    type: str
    version: str
    owner: str


@router.post("/servers/create")
async def createServerR(config: Configuration):
    logger.info("Server Creation Detected!")
    uuid = uuidLib.uuid4()
    await utilities.serverCreator.createServer(config.name, uuid, config.type, config.version, config.ram, config.owner)
    return {"status": "created", "uuid": str(uuid)}


class importConfig(BaseModel):
    name: str
    ram: int
    type: str
    version: str
    path: str
    owner: str


@router.post("/servers/import")
async def importServerR(config: importConfig):
    name = config.name
    ram = config.ram
    serverType = config.type
    version = config.version
    path = config.path
    owner = config.owner

    logger.info(f"Importing server {name}")
    uuid = str(uuidLib.uuid4())
    utilities.serverCreator.importServer(name, path, ram, version, serverType, uuid, owner)
    return {"status": "imported", "uuid": uuid}


@router.post("/servers/{uuid}/acceptEula")
async def acceptEulaR(uuid: UUID):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    await serverManager.acceptEula()
    return {"status": "accepted", "uuid": uuid}


class propertyConfig(BaseModel):
    datas: dict


@router.post("/servers/{uuid}/editProperties")
async def editPropertiesR(uuid: UUID, propertyConfig: propertyConfig):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    datas = propertyConfig.datas
    print(datas)
    for property, value in datas.items():
        serverManager.setProperty(property, value)
    return {"status": "edited", "uuid": uuid}


class RenameConfig(BaseModel):
    newName: str


@router.post("/servers/{uuid}/rename")
async def renameR(uuid: UUID, renameConfig: RenameConfig):
    result = cache.getCurrentServerAndSm(uuid)
    server: mcUtilities.Server = result["server"]
    newName = renameConfig.newName
    # TODO : Give choice to user to rename files or not
    server.rename(newName, deep=True)
    return {"status": "renamed", "uuid": uuid}


class DuplicateConfig(BaseModel):
    dupName: str


@router.post("/servers/{uuid}/duplicate")
async def duplicateR(uuid: UUID, duplicateConfig: DuplicateConfig):
    result = cache.getCurrentServerAndSm(uuid)
    server: mcUtilities.Server = result["server"]
    dupName = duplicateConfig.dupName
    newServerUuid = server.duplicate(dupName)
    return {"status": "duplicated", "uuid": uuid, "newServerUuid": newServerUuid}


@router.post("/servers/{uuid}/softDelete")
async def softDelR(uuid: UUID):
    softDelete.softDelete(uuid)
    return {"status": "softDeleted", "uuid": uuid}


@router.post("/deletedServers/{uuid}/fullDelete")
async def fullDeleteR(uuid: UUID):
    softDelete.fullDelete(uuid)
    return {"status": "softDeleted", "uuid": uuid}


@router.post("/deletedServers/{uuid}/restore")
async def restoreR(uuid: UUID):
    softDelete.restore(uuid)
    return {"status": "softDeleted", "uuid": uuid}
