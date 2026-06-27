import asyncio
import os
import pathlib
import sys
from asyncio.subprocess import Process
import psutil
from loguru import logger
import utilities.db as db

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{file.name}</cyan> | "
           "{message}",
    colorize=True
)


# ----------------------------------------
# ----------------------------------------
# ----------------------------------------


def findSpecifiedFileByExtension(extension: str = None, folderPath: str = None) -> str:
    # ETAT : Ok
    # DOC : Ok
    """
    Cette fonction permet de trouver un fichier avec une certaine extension dans un dossier.

    :param extension: str -> Extension du fichier à trouver (par exemple '.bat', '.json').
    :param folderPath: str -> Chemin du dossier dans lequel chercher le fichier.
    :return: str -> Chemin complet du fichier trouvé.
    :raise ValueError: Une erreur si aucun fichier avec l'extension n'est trouvé.
    :raise FileNotFoundError: Une erreur si l'extension ou le chemin du dossier n'est pas fourni.
    """
    if extension is None or folderPath is None:
        raise ValueError("Erreur : Extension ou chemin du dossier non fourni ou nul.")
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.endswith(extension):
                return os.path.join(root, file)

    raise FileNotFoundError(f"Erreur : Aucun fichier avec l'extension '{extension}' trouvé dans {folderPath}.")


async def executeFileAndTrackOutput(serverPath: str = None, fileToExecute: str = None) -> Process:
    """
    Cette fonction execute un fichier et traque sa sortie.
    :param serverPath: str -> Le chemin du serveur.
    :param fileToExecute: str -> Le fichier à executer.
    """
    process = await asyncio.create_subprocess_exec(
        fileToExecute,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        stdin=asyncio.subprocess.PIPE,
        cwd=serverPath,
    )
    return process


class ServerManager:
    """
    Cette classe permet de gérer ses serveurs.
    Une instance de ServerManager doit être créée par serveur.
    :param server: Server -> Le serveur auquel le ServerManager sera affecté.
    :raise ValueError: si le serveur précisé lors de l'initialisation n'est pas une instance de "Server".
    """

    def __init__(self, server: "Server" = None):
        self.server = server
        self.process = None
        if self.server is None or type(self.server) is not Server:
            raise ValueError("le serveur précisé n'est pas de type valide ou précisé.")
        self.onlineEvent = asyncio.Event()
        self.pid: int = 0
        self.consoleSubscribers: list = []

    async def addLineInConsole(self, textToWrite: str):
        self.process.stdin.write(textToWrite.encode() + b"\n")
        await self.process.stdin.drain()  # force l'envoi

    async def startServer(self) -> None:
        """
        Démarre le serveur auquel le ServerManager est affecté.
        """
        if self.server.isOnline:
            logger.warning("Impossible to start the server - it is already online")
            return
        logger.info("Trying to start the server..")
        serverBat = findSpecifiedFileByExtension("bat", self.server.serverPath)
        self.process = await executeFileAndTrackOutput(self.server.serverPath, serverBat)
        _ = asyncio.create_task(self.trackConsole())

        await asyncio.sleep(1)

        parent = psutil.Process(self.process.pid)
        java_pid = None

        for child in parent.children(recursive=True):
            if 'java' in child.name().lower():
                java_pid = child.pid
                logger.info(f"Found Java process with PID: {java_pid}")
                break

        if java_pid is None:
            logger.error("No Java process found, using cmd PID as fallback")
            self.pid = self.process.pid
        else:
            self.pid = java_pid

        logger.info(f"Server started with PID: {self.pid}")
        self.server.isOnline = True
        self.onlineEvent.set()

    async def stopServer(self):
        """
        Méthode pour arreter le serveur auquel le ServerManager est affecté.
        :return:
        """
        logger.info("Trying to stop the server..")
        if not self.server.isOnline:
            logger.warning("Impossible to stop the server - it is offline")
            return

        try:
            await self.sendCommand(command="stop")
        except Exception as e:
            print(f"Unexpected exception encoutered while stopping server : {e}")
        else:
            logger.info("Server stopped correctly")
            self.onlineEvent.clear()
            self.server.isOnline = False
        return

    async def handleServerAutoStop(self):
        logger.info("Server stopped correctly")
        self.onlineEvent.clear()
        self.server.isOnline = False

    async def restartServer(self):
        await self.stopServer()
        while True:
            if "ThreadedAnvilChunkStorage: All dimensions are saved" not in self.getServerLastConsoleEntry():
                continue
            else:
                break
        await self.startServer()

    async def sendCommand(self, command: str):
        """
        Méthode pour executer une commande sur le serveur auquel le ServerManager est affecté.
        :raise ConnectionError -> Si le serveur n'est pas lancé.
        """
        if self.process is None:
            raise ConnectionError("Erreur -> le server n'est pas lancé actuellement.")
        self.process.stdin.write((command + "\n").encode())
        await self.process.stdin.drain()

    async def getServerLastConsoleEntry(self) -> str:
        """
        Cette méthode permet  d'obtenir la dernière ligne de la console du serveur.
        :return: le dernier message envoyé dans la console du serveur auquel le ServerManager est associé.
        """
        line = await self.process.stdout.readline()
        line = line.decode()
        if not line:
            return ""
        return line.strip()

    async def acceptEula(self):
        with open(pathlib.Path(self.server.serverPath) / "eula.txt", "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith("eula="):
                lines[i] = "eula=true\n"
                break

        with open(pathlib.Path(self.server.serverPath) / "eula.txt", "w") as file:
            file.writelines(lines)

    async def trackConsole(self):
        logger.debug(f"Now tracking console")
        async for line_byte in self.process.stdout:
            line = line_byte.decode().strip()
            if line:
                for queue in self.consoleSubscribers:
                    await queue.put(line)

    def subscribeToConsole(self, queue: asyncio.Queue):
        logger.debug(f"New queue subscribed to console")
        self.consoleSubscribers.append(queue)

    def unsubscribeConsole(self, q: asyncio.Queue):
        logger.debug(f"Queue unsubscribed to console")
        self.consoleSubscribers.remove(q)


# ----------------------------------------
# ----------------------------------------
# ----------------------------------------


class Server:
    # DOC : Ok
    """
    Cet objet représente un serveur minecraft. Elle possède comme attributs :
     - name: str -> le nom du serveur.
     - creationDate: str -> date de création du serveur // Format AAAAMMDDHHMM
     - lastUseDate: str -> date de dernière utilisation ddu server // Format AAAAMMDDHHMM
     - maxRam: str -> la ram allouée au serveur.
     - version: str -> la version du serveur.
     - serverType: str -> le "type" de serveur (vanilla, forge, spigot, sponge).
     - serverPath: str -> le chemin du serveur.
     - uuid: str -> l'identifiant unique du serveur. C'est lui qu'on utilise pour représenter le fichier dans le Json.
    \n
    Ses méthodes :
     - getdatas -> Retournes les données du serveur sous forme de dictionnaire. \n
     - save -> Sauvegarder les données du serveur dans le fichier Json. \n
     - loadDatas -> Récupere les données sous forme de dictionnaire et mets a jour les attributs du serveur avec
       ces dernières.
     - edit[attribut à modifier] -> Modifie les données du serveur et les mets a jour dans le fichier Json.

     .. note::
        Créer une instance de cette classe en ne précisant que l'uuid va automatiquement lancer une récuperation
        automatique de données depuis le fichier Json.


    """

    def __init__(self, name: str = None,
                 creationDate: str = None,
                 lastUseDate: str = None,
                 maxRam: int = None,
                 version: str = None,
                 serverType: str = None,
                 path: str = None,
                 uuid: str = None):

        self.uuid: str = uuid
        self.name: str = name
        self.creationDate = creationDate
        self.lastUseDate = lastUseDate
        self.maxRam: int = maxRam
        self.version: str = version
        self.serverType: str = serverType
        self.serverPath: str = path
        self.isOnline: bool = False

        self.batPath: str
        self.propertiesPath: str

        if all(x is None for x in [name, maxRam, version, serverType, path]):
            print("Aucune des valeurs ne sont définies. Tentative de récuperation des données automatique")
            conn = db.getConnexion()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM servers WHERE uuid = ?", (self.uuid,))
            serverInstance = cursor.fetchone()
            conn.close()
            if self.uuid is None or serverInstance is None:
                print("UUID de serveur non fournie ou non reconnune. Echec de la tentative de récuperation "
                      "automatique de données. Merci de fournir un UUID correcte.")
                return
            self.loadDatas()
            print("Récuperation des données du serveur réussie.")

        if self.serverPath is not None:
            self.batPath = findSpecifiedFileByExtension('.bat', self.serverPath)
        else:
            self.batPath = None

    def init(self) -> None:
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO servers (uuid, name, lastUseDate, maxRam, version, serverType, serverPath) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.uuid, self.name, self.lastUseDate, self.maxRam, self.version, self.serverType, self.serverPath))
        conn.commit()
        conn.close()

    def save(self) -> None:
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE servers 
            SET name = ?, lastUseDate = ?, maxRam = ?,  version = ?, sTye = ?, serverPath = ?
            WHERE uuid = {self.uuid}
        """, (self.name, self.lastUseDate, self.maxRam, self.version, self.serverType, self.serverPath))
        conn.commit()
        conn.close()

    def getPropertiesPath(self):
        return findSpecifiedFileByExtension('.properties', self.serverPath)

    def loadDatas(self) -> None:
        # ETAT : Ok
        # DOC : Ok

        """
        Cette fonction permet de mettre a jour les attributs du serveur en récuperant les données depuis le fichiers
        Json.
        """
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servers WHERE uuid = ?", (self.uuid,))
        servers = cursor.fetchone()
        conn.close()

        self.name: str = servers["name"]
        self.creationDate = servers["creationDate"]
        self.lastUseDate = servers["lastUseDate"]
        self.maxRam: int = servers["maxRam"]
        self.version: str = servers["version"]
        self.serverType: str = servers["serverType"]
        self.serverPath: str = servers["serverPath"]

    def getPropertiesAsDict(self) -> {str: str}:
        dict_ = {}
        with open(self.getPropertiesPath(), 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == r"#":
                    continue
                try:
                    key, value = line.split("=", 1)
                except ValueError as e:
                    logger.error(f"Error while parsing properties.properties as dict -> {e}")
                dict_[str(key).strip()] = str(value).strip()

        return dict_

    def getCurrentLogs(self):
        """
        Fonction qui récupère le contenu des dernières logs du serveur
        """
        eulaLatestLogPath = pathlib.Path(self.serverPath) / "logs/latest.log"
        if not eulaLatestLogPath.exists():
            logger.error("Aucun fichier de logs n'a pu être récupéré")
            return
        with open(eulaLatestLogPath) as file:
            logs = file.readlines()
        return logs


# --DEPRECATED
# Global Service Object. Il n'a qu'un interet simple et ne sera instancié qu'une fois lors de l'init du logiciel.
"""class Global:
    Alias GSO -> Global Service Ojbect.
    Cet objet n'a qu'un interet simple mais est tout de même nécessaire au bon fonctionnement du serveur.
    Il à comme attribut le chemin du serveur, que l'on peut récuperer via la méthode : getJsonPath.
    .. note::
        Il est très fortement recommandé de n'instancier qu'une fois cet objet lors de l'initialisation du logiciel.

    # TODO créer une instance du GSO dans l'init du software.
    def __init__(self, jsonPath: str = None):
        self.jsonPath: str = jsonPath

    def getJsonPath(self):
        if self.jsonPath is None:
            print('Erreur : impossible d\' accdéder au fichier Json.')
        return self.jsonPath"""

# if __name__ == '__main__':
# globalService = Global(jsonPath="datas.json")
