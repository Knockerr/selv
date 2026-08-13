import asyncio
import os
import pathlib
import sys
from asyncio.subprocess import Process
from typing import Literal

import psutil
from loguru import logger
import utilities.db as db
from uuid import UUID, uuid4
from datetime import datetime, timezone
import shutil
import utilities.eventBuses as eventBuses
from utilities import softDelete


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


async def executeFileAndTrackOutput(path: str = None, fileToExecute: str = None) -> Process:
    """
    Cette fonction execute un fichier et traque sa sortie.
    :param path: str -> Le chemin du serveur.
    :param fileToExecute: str -> Le fichier à executer.
    """
    process = await asyncio.create_subprocess_exec(
        fileToExecute,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        stdin=asyncio.subprocess.PIPE,
        cwd=path,
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
        self.process: Process | None = None
        if self.server is None or type(self.server) is not Server:
            raise ValueError("le serveur précisé n'est pas de type valide ou précisé.")
        self.onlineEvent = asyncio.Event()
        self.pid: int = 0
        self.consoleSubscribers: list = []
        self.updateMaxRam()
        self.psutilsProcess: psutil.Process | None = None
        self.stateBus = eventBuses.getServerBus(self.server.uuid)
        self.stateBus.setValue("stopped")

        try:
            self.cpuCores: int = os.cpu_count()
        except Exception as e:
            logger.error(f"Unable to get n of cpus : {e}")

    async def addLineInConsole(self, textToWrite: str):
        self.process.stdin.write(textToWrite.encode() + b"\n")
        await self.process.stdin.drain()

    async def startServer(self) -> None:
        """
        Démarre le serveur auquel le ServerManager est affecté.
        """
        from utilities.miscellaneous import Stats
        self.server.lastUseDate = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self.server.save()
        if self.server.isOnline:
            logger.warning("Impossible to start the server - it is already online")
            return
        logger.info("Trying to start the server..")
        serverBat = findSpecifiedFileByExtension("bat", self.server.path)
        self.process = await executeFileAndTrackOutput(self.server.path, serverBat)
        _ = asyncio.create_task(self.trackConsole())
        _ = asyncio.create_task(self.stateBus.broadcast("running"))

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
        self.server.startTime = datetime.now(timezone.utc)
        self.psutilsProcess = psutil.Process(self.pid)
        self.server.isOnline = True
        self.onlineEvent.set()
        Stats.runningServers.append(self.server.uuid)

    async def stopServer(self):
        from utilities.miscellaneous import Stats
        """
        Méthode pour arreter le serveur auquel le ServerManager est affecté.
        :return:
        """
        logger.info("Trying to stop the server..")
        if not self.server.isOnline:
            logger.warning("Impossible to stop the server - it is offline")
            return

        try:
            self.server.isOnline = False
            _ = asyncio.create_task(self.stateBus.broadcast("stopped"))
            self.server.updateUptime()
            await self.sendCommand(command="stop")
            await self.process.wait()
            self.onlineEvent.clear()
        except Exception as e:
            print(f"Unexpected exception encoutered while stopping server : {e}")
        else:
            logger.info("Server stopped correctly")
            Stats.runningServers.remove(self.server.uuid)
        self.psutilsProcess = None
        self.pid = None
        return

    async def handleServerAutoStop(self):
        from utilities.miscellaneous import Stats
        logger.info("Server stopped correctly")
        self.server.updateUptime()
        self.onlineEvent.clear()
        await self.process.wait()
        self.stateBus.broadcast("stopped")
        self.server.isOnline = False
        Stats.runningServers.remove(self.server.uuid)

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
        with open(pathlib.Path(self.server.path) / "eula.txt", "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith("eula="):
                lines[i] = "eula=true\n"
                break

        with open(pathlib.Path(self.server.path) / "eula.txt", "w") as file:
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

    def updateMaxRam(self):
        batFile = pathlib.Path(findSpecifiedFileByExtension("bat", self.server.path))
        if not batFile.exists():
            logger.warning(f"No bat file seems to exist for {self.server.name}")
        batFileContent = batFile.read_text().split(r" ")
        for arg in batFileContent:
            if arg.startswith("-Xmx"):
                self.server.maxRam = arg[4:]
                break
        else:
            logger.error("No max ram is indicated. One must be provided.")

    def setProperty(self, property, value):
        value = str(value).lower()
        propertiesPath = (pathlib.Path(self.server.propertiesPath) or
                          findSpecifiedFileByExtension(".properties", self.server.path))
        if not propertiesPath.exists():
            logger.error(f"Server.properties file path for {self.server.name} does not exist.")
            return

        with open(propertiesPath, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(property + r"="):
                lines[i] = f"{property}={value}\n"
                logger.debug(
                    f"Replaced the value of property {property} to {value} for {self.server.name}"
                )
                break
        else:
            logger.error(f"Impossible to find property {property} in server.properties for {self.server.name}")
            return

        with open(propertiesPath, "w") as file:
            file.writelines(lines)

    def getPerfs(self):
        if not self.psutilsProcess:
            raise ConnectionError("Can't get perfs of offline server")

        cpu = round(self.psutilsProcess.cpu_percent(interval=None), 1)
        # Formatting cpu usage to be a percentage (1-100). TODO : Give the option to choose format in settings
        cpuForm = round(cpu / self.cpuCores, 2)

        mem_info = self.psutilsProcess.memory_info()
        mem_gb = mem_info.rss / (1024 * 1024 * 1024)
        memForm = f"{mem_gb:.2f}"

        return {
            "cpu": cpuForm,
            "ram": memForm,
        }


# ----------------------------------------
# ----------------------------------------
# ----------------------------------------


def correctMissingProperties(properties, server):
    """
    Contexte: Certaines versions de serveur aléatoires ne contiennent pas toutes les propriétés (bien que celles-ci
    fonctionnent malgré tout; elles ne sont juste plus dans la liste du server.properties initial.). Cette fonction
    permet de corriger le fichier si il en manque
    """

    expectedProperties = {
        "gamemode": "survival",
        "force-gamemode": "false",
        "difficulty": "easy",
        "hardcore": "false",
        "pvp": "true",
        "view-distance": "10",
        "level-seed": "",
        "generate-structures": "true",
        "allow-nether": "true",
        "max-build-height": "256",
        "spawn-monsters": "true",
        "spawn-animals": "true",
        "spawn-npcs": "true",
        "max-players": "20",
        "online-mode": "true",
        "motd": "A Minecraft Server",
        "white-list": "false"
    }

    missingProperties = []
    if not all(expectedProperties.keys()) in properties.keys():
        for expectedProperty in expectedProperties.keys():
            if expectedProperty not in properties.keys():
                missingProperties.append(expectedProperty)

        for missingProperty in missingProperties:
            with open(server.getPropertiesPath(), "a") as file:
                file.write(f"{missingProperty}={expectedProperties[missingProperty]}\n")
            properties[missingProperty] = expectedProperties[missingProperty]
    return properties


class Server:
    # DOC : Ok
    """
    Cet objet représente un serveur minecraft. Elle possède comme attributs :
     - name: str -> le nom du serveur.
     - creationDate: str -> date de création du serveur // Format ISO
     - lastUseDate: str -> date de dernière utilisation ddu server // Format ISO
     - maxRam: str -> la ram allouée au serveur.
     - version: str -> la version du serveur.
     - serverType: str -> le "type" de serveur (vanilla, forge, spigot, sponge).
     - path: str -> le chemin du serveur.
     - uuid: UUID -> l'identifiant unique du serveur. C'est lui qu'on utilise pour représenter le fichier dans le Json.
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
                 uuid: UUID = None):

        self.uuid: UUID = uuid
        self.name: str = name
        self.creationDate = creationDate
        self.lastUseDate = lastUseDate
        self.maxRam: int = maxRam
        self.version: str = version
        self.serverType: str = serverType
        self.path: str = path
        self.isOnline: bool = False
        self.uptime: int = 0
        self.startTime = None

        self.batPath: str
        self.propertiesPath: str

        if all(x is None for x in [name, maxRam, version, serverType, path]):
            logger.debug("Aucune des valeurs ne sont définies. Tentative de récuperation des données automatique")
            conn = db.getConnexion()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM activeServers WHERE uuid = ?", (str(self.uuid),))
            serverInstance = cursor.fetchone()
            conn.close()
            if self.uuid is None or serverInstance is None:
                logger.error("UUID de serveur non fournie ou non reconnune. Echec de la tentative de récuperation "
                             "automatique de données. Merci de fournir un UUID correcte.")
                return
            self.loadDatas()
            logger.info("Récuperation des données du serveur réussie.")

        if self.path is not None:
            self.batPath = findSpecifiedFileByExtension('.bat', self.path)
            self.propertiesPath = findSpecifiedFileByExtension('.properties', self.path)
        else:
            logger.warning(f"No bat or properties path seems to exist for server {self.name}")
            self.batPath = None
            self.propertiesPath = None

    def init(self) -> None:
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO servers (uuid, name, lastUseDate, maxRam, version, serverType, path, uptime) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(self.uuid), self.name, self.lastUseDate, self.maxRam, self.version, self.serverType, self.path,
              self.uptime))
        conn.commit()
        conn.close()

    def save(self) -> None:
        conn = db.getConnexion()
        cursor = conn.cursor()
        uuidStr = str(self.uuid)
        cursor.execute(f"""
            UPDATE servers 
            SET name = ?, lastUseDate = ?, maxRam = ?,  version = ?, serverType = ?, path = ?, uptime = ?
            WHERE uuid = ?
        """, (
            self.name, self.lastUseDate, self.maxRam, self.version, self.serverType, str(self.path), self.uptime,
            uuidStr))
        conn.commit()
        conn.close()

    def getPropertiesPath(self):
        return findSpecifiedFileByExtension('.properties', self.path)

    def updateUptime(self):
        if not self.startTime:
            # Prevents case of error on start that would risk to reset datas
            return
        diff: int = round((datetime.now(timezone.utc) - self.startTime).total_seconds())
        self.uptime += diff
        logger.warning(f"{self.uptime=}")
        self.save()

    def loadDatas(self) -> None:
        # ETAT : Ok
        # DOC : Ok

        """
        Cette fonction permet de mettre a jour les attributs du serveur en récuperant les données depuis la bdd sqlite
        """
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activeServers WHERE uuid = ?", (str(self.uuid),))
        server = cursor.fetchone()
        conn.close()

        self.name: str = server["name"]
        self.creationDate = server["creationDate"]
        self.lastUseDate = server["lastUseDate"]
        self.maxRam: int = server["maxRam"]
        self.version: str = server["version"]
        self.serverType: str = server["serverType"]
        self.path: str = server["path"]
        self.uptime: int = server["uptime"]

    def getPropertiesAsDict(self) -> {str: str}:
        propertiesPath = pathlib.Path(self.getPropertiesPath())
        if not propertiesPath.exists():
            # TODO : Handle case where the server isn't fully created in the frontend
            return {}
        properties = {}
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
                properties[str(key).strip()] = str(value).strip()
        properties = correctMissingProperties(properties, self)
        return properties

    def getCurrentLogs(self):
        """
        Fonction qui récupère le contenu des dernières logs du serveur
        """
        eulaLatestLogPath = pathlib.Path(self.path) / "logs/latest.log"
        if not eulaLatestLogPath.exists():
            logger.error("Aucun fichier de logs n'a pu être récupéré")
            return
        with open(eulaLatestLogPath) as file:
            logs = file.readlines()
        return logs

    def rename(self, newName: str, deep: bool = True):
        """
        Deep means that the name of the server will be changed in the files too
        """
        if not newName:
            return
        # Old name kept in memory in case of error in renaming of the files (allow to cancel everything, makes method)
        #  atomic
        oldName = self.name
        self.name = newName
        self.save()
        if deep:
            oldPath = self.path
            # Constructing new path
            newPath = self.path.split("\\")
            newPath[-1] = newName
            newPath = pathlib.Path("\\".join(newPath))
            # Renaming file
            try:
                os.rename(oldPath, newPath)
            except Exception as e:
                logger.error(f"Impossible to rename server {self.uuid} files : {e}")
                self.name = oldName
                return
            self.path = newPath
            self.save()

    def duplicate(self, duplicateName):
        """
        Returns: The duplicated server uuid
        """
        creationDate: str = datetime.now(timezone.utc).isoformat(timespec="seconds")
        source = self.path
        # Constructing new server path
        dest = self.path.split("\\")
        dest[-1] = duplicateName
        dest = pathlib.Path("\\".join(dest))

        # Creating new server
        try:
            shutil.copytree(source, dest, dirs_exist_ok=True)
        except Exception as e:
            logger.error(f"Impossible to duplicate server {self.uuid} files : {e}")
            return

        newServerPath = str(dest)
        newServerUuid = uuid4()
        newServer: Server = Server(duplicateName, creationDate, creationDate, self.maxRam, self.version,
                                   self.serverType, newServerPath, newServerUuid)
        newServer.init()
        return newServerUuid

    def _isEulaAccepted(self):
        # Check if Eula file
        eulaPath = pathlib.Path(self.path) / "eula.txt"
        if not eulaPath.exists():
            return False
        with open(eulaPath, "r") as file:
            for line in file.readlines():
                if line.startswith("eula"):
                    line.split("=")
                    valueText = line[1].lower()
                    if valueText == "true":
                        value = True
                    else:
                        value = False
                    return value

    def getCreationStep(self):
        step: Literal["serverFile", "waitingEula", "created"]
        if len(os.listdir(self.path)) < 4:
            # If there are 3 files only (or less) server is considered as not even started
            step = "serverFile"
        elif not self._isEulaAccepted:
            step = "waitingEula"
        else:
            step = "created"

        self.creationStep = step


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
