import datetime
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys
from uuid import UUID
from datetime import datetime, timezone

import platformdirs as plat
import requests
from loguru import logger

import utilities.mcUtilities as mcUtilities
from utilities import db, tunneling
from utilities.miscellaneous import getSystem, getResourceRuntimePath

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{file.name}</cyan> | "
           "{message}",
    colorize=True
)

appDir = plat.PlatformDirs(appname="Selv", appauthor=False)
serversDir = appDir.user_data_path / 'servers'
jarsDir = appDir.user_data_path / 'jars'
javaDir = appDir.user_data_path / 'JREs'
datasDir = appDir.user_data_path / 'datas'


def checkForJavaInstall(javaVersion):
    """
    Checks if java version has already been downloaded, else downloads it

    Returns : java.exe path
    """
    # Check if file has already been downloaded:
    javaFile = (javaDir / f"java{javaVersion}" / 'bin/java.exe')

    # Si le dossier n'existe pas, le télécharger
    if not javaFile.exists():
        logger.info("Le fichier java n'a pas encore été téléchargé, lancement du processus")
        # Récuperer le fichier
        javaArchive = requests.get(f'https://api.adoptium.net/v3/binary/latest/{javaVersion}/ga/windows/x64/jre/hotspot'
                                   f'/normal/eclipse')
        if javaArchive.status_code != 200:
            logger.error(f"Erreur lors de la récuperation de l'archive java {javaVersion} : {javaArchive.status_code}")

        # Réécrire le fichier
        javaDir.mkdir(parents=True, exist_ok=True)
        with open(javaDir / f'java{javaVersion}-archive.zip', "wb") as file:
            file.write(javaArchive.content)
        logger.debug("Archive java téléchargée, début de l'extraction..")

        # Extraction des fichiers
        shutil.unpack_archive((javaDir / f'java{javaVersion}-archive.zip'),
                              (javaDir / f'java{javaVersion}'))
        # Supprimer l'archive
        os.remove((javaDir / f'java{javaVersion}-archive.zip'))
        logger.debug("Extraction du fichier java réalisée avec succès.")

        # Suppression du dossier intérmediaire
        javaVersionFile = javaDir / f'java{javaVersion}'
        dossierIntermediaire = javaVersionFile / (next(javaVersionFile.iterdir()))
        for item in dossierIntermediaire.iterdir():
            shutil.move(str(item), str(javaVersionFile))
        dossierIntermediaire.rmdir()
    else:
        logger.info("Le fichier java à déja été téléchargé, saut de l'étape de téléchargement.")


def getJavaPath(mcVersion: str):
    javaVersion: int = 0
    versionNum = int(mcVersion.split('.')[1])
    if 8 <= versionNum <= 11:
        checkForJavaInstall(8)
        javaVersion = 8
    elif 12 <= versionNum <= 16:
        checkForJavaInstall(11)
        javaVersion = 11
    elif 17 <= versionNum <= 19:
        checkForJavaInstall(17)
        javaVersion = 17
    elif 20 <= versionNum:
        checkForJavaInstall(21)
        javaVersion = 21
    else:
        logger.error(f"Version du jeu {mcVersion} non reconnue..")
    return javaDir / f"java{javaVersion}" / 'bin/java.exe'


def createStartBatFile(serverName, version, maxRam, serverFileName):
    javaPath = getJavaPath(version)
    with open(serversDir / serverName / 'start.bat', "w") as file:
        file.write(f"@echo off \n\"{javaPath}\" -Xmx{maxRam}G -jar {serverFileName} --nogui")


def editAutoForgeBatFile(serverName, mcVersion):
    serverPath = serversDir / serverName
    # Override les arguments de la JVM initiaux
    with open(serverPath / "user_jvm_args.txt", 'w') as argsFile:
        argsFile.write(" -Xmx4G")

    forgeVersion = getForgeVersion(mcVersion)

    # Override le start.bat pour le démarrer en noGUi est forcer l'utilisation du JRE portable installé
    with open(serverPath / "run.bat", 'w') as batFile:
        batFile.write(f"@echo off\n"
                      f"{getJavaPath(mcVersion)} @user_jvm_args.txt @libraries/net/minecraftforge/forge/{mcVersion}-{forgeVersion}/"
                      f"win_args.txt %*\n")


def getFrpcBinaryPath():
    system = getSystem()

    if system == "Windows":
        return getResourceRuntimePath("binaries/frpc/frpc.exe")
    elif system == "Linux":
        return getResourceRuntimePath("binaries/frpc/frpc")
    else:
        raise RuntimeError(f"OS non supporté: {system}")


def createFrpcFolder(server: mcUtilities.Server):
    backendRoot = pathlib.Path(__file__).resolve().parent.parent
    folderPath = pathlib.Path(server.path) / ".selv"
    frpcFolderPath = folderPath / "frpc"
    mdFilePath = folderPath / "README.md"

    # Create folders
    if not folderPath.exists():
        frpcFolderPath.mkdir(parents=True, exist_ok=True)
        mdFilePath.touch(exist_ok=True)

    # Fill md file
    mdTemplatePath = getResourceRuntimePath("templates/frpc-markdown-template.md")
    mdContent = mdTemplatePath.read_text(encoding="utf-8")

    with open(mdFilePath, "w", encoding="utf-8") as file:
        file.write(mdContent)

    # Add frpc bin in folder
    frpcBinPath = getFrpcBinaryPath()

    if getSystem() == "Windows":
        dest = frpcFolderPath / "frpc.exe"
    else:
        dest = frpcFolderPath / "frpc"

    shutil.copy(frpcBinPath, dest)


async def handleSpigotDownload(version: str):
    # Charger le fichier manifest de spigot non officiel
    with open('./orgBukkitManifest-unoff.json', 'r') as f:
        spigotManifest = json.load(f)
    # Récuperer le lien de téléchargement
    spigotServerJarLink = spigotManifest[version]['url']
    if not spigotServerJarLink:
        logger.error(f"Impossible de trouver la version {version} dans le manifest de spigot")
        return

    # Télécharger le jar
    jarFile = requests.get(spigotServerJarLink)
    if jarFile.status_code != 200:
        logger.error(f"Erreur lors du téléchargement du fichier serveur jar spigot: {jarFile.status_code}")
        return
    (jarsDir / "spigot").mkdir(parents=True, exist_ok=True)
    # Ecriture du jar
    with open(jarsDir / f"spigot/Spigot-{version}.jar", "wb") as file:
        file.write(jarFile.content)


async def handleSpigotCreation(name: str, uuid: UUID, type_: str, version: str, ram: int):
    # Vérification : Si le fichier n'est pas déja téléchargé, l'installer.
    serverFile = jarsDir / 'spigot' / f"Spigot-{version}.jar"
    if not serverFile.exists():
        logger.info(f"Aucun serveur spigot {version} n'est téléchargé. Lancement du téléchargement..")
        await handleSpigotDownload(version)
    logger.debug("Copie du fichier vanilla vers le serveur.")
    # Créer le dossier du serveur
    (serversDir / name).mkdir(parents=True, exist_ok=True)
    # Déplacer le jar serveur dans le dossier du serveur
    shutil.copy(jarsDir / 'spigot' / f'Spigot-{version}.jar', serversDir / name / f'SpigotServer-{version}.jar')

    # Récuperer la date
    creationDate: str = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Créer le fichier start.bat de lancement du serveur
    createStartBatFile(name, version, ram, f'SpigotServer-{version}.jar')

    availablePort = await tunneling.getAvailableLocalPort()

    logger.debug("Création du serveur")
    # Créer le serveur
    server = mcUtilities.Server(name, creationDate, creationDate, ram, version, type_, str(serversDir / name), uuid,
                                None, availablePort)
    server.init()
    logger.debug(f"Objet Server de {name} créé et sauvegardé.")

    return server


async def handleVanillaDownload(version: str) -> None:
    """
    Gère le téléchargement d'une version de paper.
    """
    versionsManifestRoute = f"https://launchermeta.mojang.com/mc/game/version_manifest.json"
    # Récuperer le manifest paper de la version
    mojangVersionManifestRequest = requests.get(versionsManifestRoute)
    if mojangVersionManifestRequest.status_code != 200:
        logger.error(
            f"Erreur lors de la récuperation du manifest de mojang : {mojangVersionManifestRequest.status_code}")
        return
    mojangVersionManifest = mojangVersionManifestRequest.json()
    # Boucler sur les versions
    for currentVersion in mojangVersionManifest["versions"]:
        # Si la version correspond
        if currentVersion['id'] == version:
            # Récuperer le lien vers les données de la version
            thisVersionManifestRoute = currentVersion["url"]
            break
    else:
        # Si le fichier n'est pas trouvé
        logger.error(f"Impossible de trouver la version {version} le manifest des versions mojang..")
        return

    # Téléchargement du manifest de version
    thisVersionManifestRequest = requests.get(thisVersionManifestRoute)
    if thisVersionManifestRequest.status_code != 200:
        logger.error(f"Erreur lors du téléchargement du manifest de la version {version}:"
                     f" {thisVersionManifestRequest.status_code}")
        return

    # Récuperation dans le manifest de version de l'url de téléchargement du fichier server
    serverJarUrl = thisVersionManifestRequest.json()['downloads']['server']['url']

    # Télécharger le jar
    jarFile = requests.get(serverJarUrl)
    if jarFile.status_code != 200:
        logger.error(f"Erreur lors du téléchargement du fichier serveur jar vanilla: {jarFile.status_code}")
        return
    (jarsDir / "vanilla").mkdir(parents=True, exist_ok=True)
    # Ecriture du jar
    with open(jarsDir / f"vanilla/Vanilla-{version}.jar", "wb") as file:
        file.write(jarFile.content)


async def handleVanillaCreation(name: str, uuid: UUID, type_: str, version: str, ram: int):
    # Vérification : Si le fichier n'est pas déja téléchargé, l'installer.
    serverFile = jarsDir / 'vanilla' / f"Vanilla-{version}.jar"
    if not serverFile.exists():
        logger.info(f"Aucun serveur vanilla {version} n'est téléchargé. Lancement du téléchargement..")
        await handleVanillaDownload(version)
    logger.debug("Copie du fichier vanilla vers le serveur.")
    # Créer le dossier du serveur
    (serversDir / name).mkdir(parents=True, exist_ok=True)
    # Déplacer le jar serveur dans le dossier du serveur
    shutil.copy(jarsDir / 'vanilla' / f'Vanilla-{version}.jar', serversDir / name / f'VanillaServer-{version}.jar')

    # Récuperer la date
    creationDate: str = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Créer le fichier start.bat de lancement du serveur
    createStartBatFile(name, version, ram, f'VanillaServer-{version}.jar')

    availablePort = await tunneling.getAvailableLocalPort()

    logger.debug("Création du serveur")
    # Créer le serveur
    server = mcUtilities.Server(name, creationDate, creationDate, ram, version, type_, str(serversDir / name), uuid,
                                None, availablePort)
    server.init()
    logger.debug(f"Objet Server de {name} créé et sauvegardé.")

    return server


async def handlePaperDownload(version: str) -> None:
    """
    Gère le téléchargement d'une version de paper.
    """
    # Déterminer la route api qui sera utilisée :
    apiRoute = f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds"
    # Récuperer le manifest paper de la version
    paperVersionManifestRequest = requests.get(apiRoute)
    if paperVersionManifestRequest.status_code != 200:
        logger.error(f"Erreur lors de la récuperation du manifest de paper : {paperVersionManifestRequest.status_code}")
        return
    paperVersionManifest = paperVersionManifestRequest.json()
    # Récuperer le lien de téléchargement
    jarFileLink = paperVersionManifest[0]['downloads']["server:default"]["url"]
    # Télécharger le jar
    jarFile = requests.get(jarFileLink)
    if jarFile.status_code != 200:
        logger.error(f"Erreur lors du téléchargement du fichier jar de paper: {jarFile.status_code}")
        return
    (jarsDir / "paper").mkdir(parents=True, exist_ok=True)
    # Ecriture du jar
    with open(jarsDir / f"paper/Paper-{version}.jar", "wb") as file:
        file.write(jarFile.content)


async def handlePaperCreation(name: str, uuid: UUID, type_: str, version: str, ram: int):
    # Shield qui empeche le téléchargement de versions non prises en charge
    if version.split('.')[1] < '12':
        logger.error("Seul les versions supérieur a la 1.12 sont stable et suportées par paper.")
        return
    # Vérification : Si le fichier n'est pas déja téléchargé, l'installer.
    serverFile = jarsDir / 'paper' / f"Paper-{version}.jar"
    if not serverFile.exists():
        logger.info(f"Aucun serveur paper {version} n'est téléchargé. Lancement du téléchargement..")
        await handlePaperDownload(version)
    logger.debug("Copie du fichier paper vers le serveur.")
    # Créer le dossier du serveur
    (serversDir / name).mkdir(parents=True, exist_ok=True)
    # Déplacer le jar serveur dans le dossier du serveur
    shutil.copy(jarsDir / 'paper' / f'Paper-{version}.jar', serversDir / name / f'PaperServer-{version}.jar')

    # Récuperer la date
    creationDate: str = datetime.now(timezone.utc).isoformat(timespec="seconds")

    logger.info(f"{creationDate = }")

    # Créer le fichier start.bat de lancement du serveur
    createStartBatFile(name, version, ram, f'PaperServer-{version}.jar')

    availablePort = await tunneling.getAvailableLocalPort()

    logger.debug("Création du serveur")
    # Créer le serveur
    server = mcUtilities.Server(name, creationDate, creationDate, ram, version, type_, str(serversDir / name), uuid,
                                None, availablePort)
    server.init()
    logger.debug(f"Objet Server de {name} créé et sauvegardé.")

    return server


async def getForgeVersion(version):
    # Déterminer la route api qui sera utilisée :
    forgeManifestRoute = f"https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json"
    # Récuperer le manifest paper de la version
    forgeManifestRequest = requests.get(forgeManifestRoute)
    if forgeManifestRequest.status_code != 200:
        logger.error(f"Erreur lors de la récuperation du manifest de forge : {forgeManifestRequest.status_code}")
        return
    forgeManifest = forgeManifestRequest.json()
    # Récuperer les données de versions
    forgeVersions = forgeManifest['promos']
    # Regarder si une version recommandée existe pour cette version :
    if f'{version}-recommended' in forgeVersions:
        # Si une version recommandée existe, la prendre
        return forgeVersions[f'{version}-recommended']
    elif f'{version}-latest' in forgeVersions:
        # Fallback sur la latest
        return forgeVersions[f'{version}-latest']
    else:
        logger.error(f"Err forgeNoSupport: Forge ne supporte pas la version {version}, adapter les fichiers de config "
                     f"front")
        return


async def handleForgeDownload(version: str):
    """
       Gère le téléchargement d'une version de forge.
       """
    forgeVersion = getForgeVersion(version)
    # Forger l'url du jar
    jarFileLink = (f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{forgeVersion}/"
                   f"forge-{version}-{forgeVersion}-installer.jar")
    # Télécharger le jar
    jarFile = requests.get(jarFileLink)
    if jarFile.status_code != 200:
        logger.error(f"Erreur lors du téléchargement du fichier jar de forge: {jarFile.status_code}")
        return
    (jarsDir / "forge").mkdir(parents=True, exist_ok=True)
    # Ecriture du jar
    with open(jarsDir / f"forge/ForgeInstaller-{version}.jar", "wb") as file:
        file.write(jarFile.content)


async def handleForgeCreation(name: str, uuid: UUID, type_: str, version: str, ram: int):
    # Vérification : Si le fichier n'est pas déja téléchargé, l'installer.
    serverFile = jarsDir / 'forge' / f"ForgeInstaller-{version}.jar"
    if not serverFile.exists():
        logger.info(f"Aucun serveur forge {version} n'est téléchargé. Lancement du téléchargement..")
        await handleForgeDownload(version)
    logger.debug("Copie du fichier installeur forge vers le serveur.")
    # Créer le dossier du serveur
    (serversDir / name).mkdir(parents=True, exist_ok=True)
    # Déplacer le jar serveur dans le dossier du serveur
    shutil.copy(jarsDir / 'forge' / f'ForgeInstaller-{version}.jar', serversDir / name / f'ForgeInstaller.jar')
    # Executer l'installeur nouvellement créé
    subprocess.run(
        [str(getJavaPath(version)), "-jar", "ForgeInstaller.jar", "--installServer"],
        cwd=(serversDir / name)
    )

    os.remove(serversDir / name / "ForgeInstaller.jar")

    # Si la version de forge est supérieur ou égale à 1.17, un bat sera généré automatiquement
    if int(version.split('.')[1]) < 17:
        # Créer le fichier start.bat de lancement du serveur
        createStartBatFile(name, version, ram, f'minecraft_server.{version}.jar')
    else:
        # Il est cependant nécessaire de modifier le fichier bat généré
        editAutoForgeBatFile(name, version)

    # Récuperer la date
    creationDate: str = datetime.now(timezone.utc).isoformat(timespec="seconds")

    availablePort = await tunneling.getAvailableLocalPort()

    logger.debug("Création du serveur")
    # Créer le serveur
    server = mcUtilities.Server(name, creationDate, creationDate, ram, version, type_, str(serversDir / name), uuid,
                                None, availablePort)
    server.init()
    logger.debug(f"Objet Server de {name} créé et sauvegardé.")

    return server


async def createServer(name: str, uuid: UUID, type_: str, version: str, ram: int):
    match type_:
        case "vanilla":
            server = await handleVanillaCreation(name, uuid, type_, version, ram)
        case "spigot":
            server = await handleSpigotCreation(name, uuid, type_, version, ram)
        case "paper":
            server = await handlePaperCreation(name, uuid, type_, version, ram)
        case "forge":
            server = await handleForgeCreation(name, uuid, type_, version, ram)
        case _:
            logger.error(f"Le type du serveur n'a pas été reconnu. Type : {type_}")
            return
    createFrpcFolder(server)


def getServerRam(name, path):
    batFile = pathlib.Path(mcUtilities.findSpecifiedFileByExtension("bat", path))
    if not batFile.exists():
        logger.warning(f"No bat file seems to exist for {name}")
    batFileContent = batFile.read_text().split(r"\n")
    startCommandArgs = batFileContent[1].split(" ")
    for arg in startCommandArgs:
        if arg.startswith("-Xmx"):
            return arg[4:]
    else:
        logger.error("No max ram is indicated. One must be provided.")
        return "askUser"


def importServer(name: str, path: str | pathlib.Path, ram, version, serverType, uuid):
    # TODO: Create a system that automatically gets servers datas
    # Récuperer la date
    creationDate: str = datetime.now(timezone.utc).isoformat(timespec="seconds")

    logger.debug("Création du serveur")
    # Créer le serveur
    server = mcUtilities.Server(name, creationDate, creationDate, ram, version, serverType, path, uuid)
    server.init()
    logger.debug(f"Objet Server de {name} créé et sauvegardé.")
