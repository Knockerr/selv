from fastapi import APIRouter
from utilities.serverUtilities import cache
from utilities import mcUtilities
from pydantic import BaseModel
import utilities.serverCreator
import sqlite3
import uuid as uuidLib
from loguru import logger
import sys
import platformdirs as plat

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{file.name}</cyan> | "
           "{message}",
    colorize=True
)

appDir = plat.PlatformDirs("mcPanel-DEV", "Knocker")

# Create routeur
router = APIRouter()


def getNewCursor() -> sqlite3.Cursor:
    conn = sqlite3.connect(appDir.user_data_path / "servers.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return cursor


@router.get("/servers")
def getServersR():
    cursor = getNewCursor()
    cursor.execute("SELECT * FROM servers")
    return [dict(row) for row in cursor.fetchall()]


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


@router.get("/servers/{uuid}/serverListDatas")
async def getServerDatas(uuid: str):
    cursor = getNewCursor()
    cursor.execute("SELECT * FROM servers WHERE UUID = ?", (uuid,))
    curServerDatas = dict(cursor.fetchone())
    name = curServerDatas['name']
    type_ = curServerDatas['sType']
    state = '...'  # TODO
    lastUse = curServerDatas['lastUseDate']
    version = curServerDatas['version']
    path = curServerDatas['serverPath']

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


@router.post("/servers/{uuid}/acceptEula")
async def acceptEulaR(uuid: str):
    result = cache.getCurrentServerAndSm(uuid)
    serverManager = result["serverManager"]
    await serverManager.acceptEula()
    return {"status": "accepted", "uuid": uuid}
