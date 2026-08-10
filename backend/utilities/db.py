import sqlite3
import platformdirs as plat

# Get the user app directory
appDir = plat.PlatformDirs("mcPanel-DEV", "Knocker")


def initDb():
    """
    Function that create basic db table if none is defined.
    This function is executed at each start of the backend.
    """
    conn = sqlite3.connect(appDir.user_data_path / "datas.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers (
        uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        serverType TEXT NOT NULL,
        version TEXT NOT NULL,
        path TEXT NOT NULL,
        maxRam INTEGER NOT NULL,
        lastUseDate TEXT,
        creationDate TEXT
    );
    """)
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
    cursor.execute(f"ALTER TABLE servers ADD COLUMN {name} {type} DEFAULT {default}")
    conn.close()
