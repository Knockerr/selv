import httpx
from fastapi import HTTPException

from utilities import mcUtilities, db

remoteServerIp = "http://127.0.0.1:4555"


async def postExternalServer(endpoint, body, accessToken) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{remoteServerIp}/api/tunnels/{endpoint}", json=body, headers={
                "authorization": f"Bearer {accessToken}",
            })
    except Exception:
        raise

    return res.json()


async def registerServer(server: mcUtilities.Server, domain, accessToken):
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
