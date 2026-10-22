import asyncio
import datetime
import pathlib
import random
import subprocess
import uuid

import httpx
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
from loguru import logger
import platformdirs as plat

from utilities import mcUtilities, db

jinjaEnv = Environment(loader=FileSystemLoader("."))

appDir = plat.PlatformDirs(appname="Selv", appauthor=False)

remoteServerIp = "https://api.selvmc.com"


async def postExternalServer(endpoint, body, accessToken) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{remoteServerIp}/api/tunnels/{endpoint}", json=body, headers={
                "authorization": f"Bearer {accessToken}",
            })
    except Exception:
        raise

    return res.json()


async def getExternalServer(endpoint, accessToken=None) -> dict:
    headers: dict = {}
    if accessToken:
        headers = {
            "authorization": f"Bearer {accessToken}",
        }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{remoteServerIp}/api/tunnels/{endpoint}", headers=headers)
    except Exception:
        raise

    return res.json()


async def registerServer(server: mcUtilities.Server, domain, accessToken):
    # Ensuring the domain is available
    try:
        domainAvailable = await checkDomainAvailability(domain)
        if not domainAvailable:
            # Raising error as frontend should prevent this from happening
            raise HTTPException(409, f"The domain {domain} is already being used ; Impossible to "
                                     f"register server with that domain.")

    except Exception as e:
        raise HTTPException(500, f"Error whilst checking domain's availability in external backend : {e}")

    try:
        await postExternalServer("register", {
            "serverUuid": str(server.uuid),
            "domain": domain,
        }, accessToken)
    except Exception as e:
        raise HTTPException(500, f"Error whilst registering server in external backend : {e}")

    try:
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE servers SET domain=? WHERE uuid=?;
        """, (domain, str(server.uuid)))
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(500, f"Error whilst registering server in db : {e}")

    server.domain = domain
    server.save()


async def unregisterServer(server: mcUtilities.Server, accessToken):
    try:
        await postExternalServer("unregister", {
            "serverUuid": str(server.uuid),
        }, accessToken)
    except Exception:
        raise
    try:
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE servers SET domain=? WHERE uuid=?;
        """, (None, str(server.uuid)))
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(500, f"Error whilst unregistering server in db : {e}")

    server.domain = None
    server.save()


async def changeDomain(server: mcUtilities.Server, newDomain, accessToken):
    logger.info(f"Changing domain {server.domain} to {newDomain} for server {server.uuid}")
    try:
        await postExternalServer("changeDomain", {
            "serverUuid": str(server.uuid),
            "newDomain": newDomain,
        }, accessToken)
    except Exception:
        raise

    try:
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE servers SET domain=? WHERE uuid=?;
        """, (newDomain, str(server.uuid)))
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(500, f"Error whilst registering server in db : {e}")


def setupTunnelConnexion(serverManager: mcUtilities.ServerManager, accessToken):
    """
    This function creates the frpc file and updates server.properties file to use its local_port value from db

    Args: accessToken only contains a str with the token, no "Bearer " prefix
    """
    server = serverManager.server
    configFolderPath = pathlib.Path(server.path) / ".selv" / "frpc"
    configPath = configFolderPath / "frpc.toml"

    # Force server to use local_port value in db
    serverManager.updateLocalPortInFiles()

    # Create file if not exists
    if not configPath.exists():
        configFolderPath.mkdir(parents=True, exist_ok=True)
        configPath.touch(exist_ok=True)

    logPath = str(appDir.user_data_path / "logs" / "frpc"
                  / f"frpc-{server.uuid}-{datetime.datetime.now().isoformat()}.log").replace("\\", "\\\\")

    logger.info(f"Creating frpc file for {server.uuid}...")
    template = jinjaEnv.get_template("frpc.toml.j2")
    fileContent = template.render(
        server_name=server.name,
        server_uuid=server.uuid,
        jwt_token=accessToken,
        local_port=server.localPort,
        log_path=logPath
    )
    with open(configPath, "w") as file:
        file.write(fileContent)
    logger.info(f"Created frpc file for {server.uuid}")


async def getAvailableLocalPort() -> int:
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE local_ports_list SET available = ?
        WHERE port = (
            SELECT port FROM available_local_ports
            LIMIT 1
        )
        RETURNING port;
    """, (False,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row is None:
        raise Exception("No more available ports")
    return row["port"]


def freeLocalPort(port):
    logger.info(f"Freeing port {port}...")
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE local_ports_list SET available = ? WHERE port=?;", (True, port))
    conn.commit()
    conn.close()
    logger.info(f"Port {port} freed")


def startTunnel(serverManager: mcUtilities.ServerManager, accessToken):
    """
    accessToken only contains a str with the token, no "Bearer " prefix
    """
    from utilities.miscellaneous import getSystem
    logger.info(f"Starting tunnel for server {serverManager.server.name} ({serverManager.server.uuid})")

    setupTunnelConnexion(serverManager, accessToken)

    frpcFolderPath = pathlib.Path(serverManager.server.path) / ".selv" / "frpc"

    frpcExePath = frpcFolderPath / "frpc.exe"
    frpcLinPath = frpcFolderPath / "frpc"
    frpcConfigPath = frpcFolderPath / "frpc.toml"

    if getSystem() == "Windows":
        tunnelProces = subprocess.Popen(
            [str(frpcExePath), "-c", str(frpcConfigPath)],
            cwd=frpcFolderPath
        )
    else:
        tunnelProces = subprocess.Popen(
            [str(frpcLinPath), "-c", str(frpcConfigPath)],
            cwd=frpcFolderPath
        )
    serverManager.tunnelProcess = tunnelProces
    logger.info("Tunnel process started")


def stopTunnel(serverManager: mcUtilities.ServerManager):
    logger.info(f"Stopping tunnel for server {serverManager.server.name} ({serverManager.server.uuid})")
    if not serverManager.tunnelProcess:
        logger.warning("Impossible to stop tunnel : None exists")

    # Stopping process
    serverManager.tunnelProcess.terminate()

    logger.info("Tunnel process stopped")


async def checkRegistration(serverUuid, accessToken):
    try:
        data = await getExternalServer(f"servers/{serverUuid}/registration", accessToken)
    except Exception as e:
        raise HTTPException(500, f"Error whilst checking server's registration in external backend : {e}")
    return data["registered"]


async def checkDomainAvailability(domain):
    try:
        data = await getExternalServer(f"domains/{domain}/availability")
    except Exception as e:
        raise
    return data["available"]
