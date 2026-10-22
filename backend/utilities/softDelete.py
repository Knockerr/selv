import os
import pathlib
import shutil
from datetime import datetime, timezone, timedelta

import platformdirs as plat
from loguru import logger

from utilities import db, tunneling

appDir = plat.PlatformDirs("App", "Selv")
deletedServersDir = appDir.user_data_path / 'deletedServers'


def softDelete(uuid):
    """
    server arg type is mcUtilities.Server
    """
    # Late import to prevent circular import
    logger.info(f"Soft deleting {uuid}")

    deletionTime = datetime.now(timezone.utc)

    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT * FROM servers WHERE uuid=?;
    """, (str(uuid),))
    serverDatas = dict(cursor.fetchone())
    conn.close()

    # Move server folder
    src = serverDatas["path"]
    dest = deletedServersDir / serverDatas["name"]
    shutil.move(src, dest)

    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE servers
        SET deletion_time=?
        WHERE uuid=?;
    """, (deletionTime.isoformat(), str(uuid),))
    conn.commit()
    conn.close()


def restore(uuid):
    logger.info(f"Restoring {uuid}")
    conn = db.getConnexion()
    cursor = conn.cursor()
    # Make sure server is still restorable:
    cursor.execute(f"""
        SELECT * FROM deletedServers WHERE uuid=?;
        """, (str(uuid),))
    serversDatas = dict(cursor.fetchone())
    serverDeletedPath = (deletedServersDir / serversDatas["name"]) or None
    if not serversDatas or not serverDeletedPath:
        logger.error(f"Impossible to restore server {uuid} : Could not get its path")
        return

    src = serverDeletedPath
    dest = serversDatas["path"]

    try:
        shutil.move(src, dest)
    except Exception as e:
        logger.error(f"Impossible to move dir to restore server {uuid} : {e}")
        return

    cursor.execute(f"""
            UPDATE servers
            SET deletionTime = NULL
            WHERE uuid=?;
        """, (str(uuid),))
    conn.commit()
    conn.close()


def fullDelete(uuid):
    conn = db.getConnexion()
    cursor = conn.cursor()
    # Getting its datas
    cursor.execute(f"SELECT * FROM deletedServers WHERE uuid=?;", (str(uuid),))
    deletedServer = dict(cursor.fetchone())

    logger.info(f"Full deleting {uuid}")

    # Completly deleting folder
    serverPath = pathlib.Path(deletedServersDir / deletedServer["name"])

    # Check that server is in deletedServers folder to prevent datas loss if path is corrupted
    if not serverPath.resolve().is_relative_to(deletedServersDir.resolve()):
        logger.error(f"Le chemin du serveur {uuid} n'est pas dans le dossier deletedServers :  {serverPath}")
        return

    try:
        shutil.rmtree(serverPath)
    except Exception as e:
        logger.error(f"Impossible to delete dir for server {uuid} : {e}")
        return

    # Get its port to add it to available ports db
    cursor.execute(f"""
            SELECT * FROM servers WHERE uuid=?;
        """, (str(uuid),))
    port = cursor.fetchone()["local_port"]

    # Delete from db
    cursor.execute(f"""
        DELETE FROM servers WHERE uuid=?;
    """, (str(uuid),))
    conn.commit()
    conn.close()

    tunneling.freeLocalPort(port)


def checkForTotalDeletion():
    """
    Functions that checks soft deleted servers to delete them completly if older than 15d
    """
    logger.debug(f"Checking soft deleted server for full delete")
    conn = db.getConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deletedServers")
    deletedServers = [dict(row) for row in cursor.fetchall()]
    logger.info(f"{deletedServers = }")
    conn.close()
    if len(deletedServers) == 0:
        return
    for deletedServer in deletedServers:
        # Check if older than 15d
        cutoff = datetime.now(timezone.utc) - timedelta(days=15)
        if "deletion_time" not in deletedServer.keys():
            continue
        deletionTime = datetime.fromisoformat(deletedServer["deletion_time"])
        if cutoff > deletionTime:
            fullDelete(deletedServer["uuid"])
