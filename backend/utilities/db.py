import os
import sqlite3
import platformdirs as plat
from loguru import logger
from pathlib import Path

# Get the user app directory
appDir = plat.PlatformDirs(appname="Selv", appauthor=False)

# TODO : Create db functions "execute", "fetch", etc... to centralize db access


def initDb():
    """
    Function that create basic db table if none is defined.
    This function is executed at each start of the backend.
    """
    logger.debug("Initialising database...")
    dbPath = appDir.user_data_path / "datas.db"

    # Create file if not exists
    dbPath.parent.mkdir(parents=True, exist_ok=True)
    dbPath.touch(exist_ok=True)

    # Setup sqlite db
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    # Create servers table and its relative views
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers (
        uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        server_type TEXT NOT NULL,
        version TEXT NOT NULL,
        path TEXT NOT NULL,
        max_ram INTEGER NOT NULL,
        last_use_date TEXT,
        creation_date TEXT,
        uptime INTEGER,
        domain TEXT,
        deletion_time TEXT,
        local_port INTEGER
    );
    """)
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS activeServers AS
        SELECT * FROM servers WHERE deletion_time IS NULL;
    """)
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS deletedServers AS
        SELECT * FROM servers WHERE deletion_time IS NOT NULL;
    """)

    # Create avaiable ports table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS local_ports_list (
            port INTEGER PRIMARY KEY,
            available BOOLEAN
        );
    """)
    ports = [(port, True) for port in range(25565, 25666)]
    cursor.executemany(
        "INSERT OR IGNORE INTO local_ports_list (port, available) VALUES (?, ?)",
        ports
    )
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS available_local_ports AS
            SELECT * FROM local_ports_list WHERE available=1;
        """)

    # TODO : make sure no conflicts exists at server start between mc server and another service

    conn.commit()
    conn.close()


def getConnexion() -> sqlite3.Connection:
    conn = sqlite3.connect(appDir.user_data_path / "datas.db")
    conn.row_factory = sqlite3.Row
    return conn


def addColumn(name, type, default):
    """
    Methods specifically for devs and maintenance (i.e. update that causes db edits)
    """
    conn = getConnexion()
    cursor = conn.cursor()
    cursor.execute(f"ALTER TABLE local_ports_list ADD COLUMN {name} {type} DEFAULT {default}")
    conn.close()


def removeColumn(name):
    """
    Methods specifically for devs and maintenance (i.e. update that causes db edits)
    """
    conn = getConnexion()
    cursor = conn.cursor()
    cursor.execute(f"ALTER TABLE servers DROP COLUMN {name}")
    conn.close()


def renameColumn(name, newName):
    """
    Methods specifically for devs and maintenance (i.e. update that causes db edits)
    """
    conn = getConnexion()
    cursor = conn.cursor()
    cursor.execute(f"ALTER TABLE servers RENAME COLUMN {name} TO {newName}")
    conn.close()
