from uuid import UUID

from fastapi import Header, APIRouter, HTTPException
from pydantic import BaseModel

from utilities import mcUtilities, tunneling
from utilities.serverUtilities import cache

# Create routeur
router = APIRouter()


class RegisterConfig(BaseModel):
    domain: str


class ChangeDomainConfig(BaseModel):
    newDomain: str


@router.post("/servers/{serverUuid}/tunnel/register")
async def registerServer(serverUuid: UUID, registerConfig: RegisterConfig, accessToken=Header(...)):
    result = cache.getCurrentServerAndSm(serverUuid)
    server: mcUtilities.Server = result["server"]
    if server.domain:
        raise HTTPException(409, "Server is already registered")
    await tunneling.registerServer(server, registerConfig.domain, accessToken)
    return {"status": "registered"}


@router.post("/servers/{serverUuid}/tunnel/unregister")
async def unregisterServer(serverUuid: UUID, accessToken=Header(...)):
    result = cache.getCurrentServerAndSm(serverUuid)
    server: mcUtilities.Server = result["server"]
    if not server.domain:
        raise HTTPException(409, "Server isn't already registered")
    await tunneling.unregisterServer(server, accessToken)
    return {"status": "unregistered"}


@router.post("/servers/{serverUuid}/tunnel/changeDomain")
async def changeDomain(serverUuid: UUID, changeConfig: ChangeDomainConfig, accessToken=Header(...)):
    result = cache.getCurrentServerAndSm(serverUuid)
    server: mcUtilities.Server = result["server"]
    await tunneling.changeDomain(server, changeConfig.newDomain, accessToken)
    return {"status": "domain_changed"}


@router.get("/servers/{uuid}/tunnel/domain")
async def getDomain(uuid: UUID):
    result = cache.getCurrentServerAndSm(uuid)
    server: mcUtilities.Server = result["server"]
    return {"domain": server.domain}


@router.post("/servers/{serverUuid}/tunnel/start")
async def startTunnelR(serverUuid: UUID, accessToken=Header(...)):
    isRegistered = await tunneling.checkRegistration(serverUuid, accessToken)
    if not isRegistered:
        raise HTTPException(404, "Cannot start tunnel if server is not registered")
    result = cache.getCurrentServerAndSm(serverUuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    tunneling.startTunnel(serverManager, accessToken)
    return {"status": "started"}


@router.post("/servers/{serverUuid}/tunnel/stop")
async def stopTunnelR(serverUuid: UUID):
    result = cache.getCurrentServerAndSm(serverUuid)
    serverManager: mcUtilities.ServerManager = result["serverManager"]
    if not serverManager.tunnelProcess:
        raise HTTPException(404, f"No tunnel seems to run for server {serverUuid}")
    tunneling.stopTunnel(serverManager)
    return {"status": "stopped"}
