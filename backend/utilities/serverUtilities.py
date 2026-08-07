import utilities.mcUtilities as mcUtilities
from uuid import UUID


# Internal cache, for optimization purposes
class Cache:
    def __init__(self):
        self.storedServers = {}
        self.storedServerManagers = {}

    def storeServer(self, server: mcUtilities.Server) -> None:
        if server.uuid in self.storedServers:
            return
        self.storedServers[server.uuid] = server

    def storeServerManager(self, serverManager: mcUtilities.ServerManager) -> None:
        if serverManager.server.uuid in self.storedServerManagers:
            return
        self.storedServerManagers[serverManager.server.uuid] = serverManager

    def isInStoredServers(self, uuid: UUID):
        return uuid in self.storedServers

    def isInStoredServerManagers(self, uuid: UUID):
        return uuid in self.storedServerManagers

    def clearCache(self):
        """
        Dangerous methode, only use it if you know what you're doing…
        """
        self.storedServers = {}
        self.storedServerManagers = {}

    def getCurrentServerAndSm(self, uuid: UUID):
        """
        Get current Server and ServerManager, weither they are stored in cache or not
        :param uuid: uuid du serveur
        :return: {"server": Server, "serverManager": ServerManager}
        """
        if not self.isInStoredServers(uuid):
            server = mcUtilities.Server(uuid=uuid)
            self.storeServer(server)

        if not self.isInStoredServerManagers(uuid):
            SM: mcUtilities.ServerManager = mcUtilities.ServerManager(server=self.storedServers[uuid])
            self.storeServerManager(SM)

        return {
            "server": self.storedServers[uuid],
            "serverManager": self.storedServerManagers[uuid]
        }


cache = Cache()
