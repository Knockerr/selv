import {
    pathDb
} from "$lib/icons/pathDb"

export const settingsBank = [{
        name: "Mode de jeu",
        description: "Mode de jeu par défaut pour les nouveaux joueurs",
        category: "game",
        property: "gamemode",
        type: "select",
        options: [{
                label: "Survie",
                value: "survival"
            },
            {
                label: "Créatif",
                value: "creative"
            },
            {
                label: "Aventure",
                value: "adventure"
            },
            {
                label: "Spectateur",
                value: "spectator"
            }
        ]
    },
    {
        name: "Forcer le mode de jeu",
        description: "A chaque connexion, tous les joueurs auront le mode de jeu défini ci-dessus",
        category: "game",
        property: "force-gamemode",
        type: "bool"
    },
    {
        name: "Difficulté",
        description: "Niveau de difficulté du serveur",
        category: "game",
        property: "difficulty",
        type: "select",
        options: [{
                label: "Paisible",
                value: "peaceful"
            },
            {
                label: "Facile",
                value: "easy"
            },
            {
                label: "Normal",
                value: "normal"
            },
            {
                label: "Difficile",
                value: "hard"
            },
        ]
    },
    {
        name: "Hardcore",
        description: "Active le mode hardcore",
        category: "game",
        property: "hardcore",
        type: "bool"
    },
    {
        name: "PvP",
        description: "Défini si le combat entre les joueurs est autorisé",
        category: "game",
        property: "pvp",
        type: "bool"

    },
    {
        name: "Distance de vue",
        description: "Défini la distance (en chunks) jusque laquelle les joueurs voient",
        category: "game",
        property: "view-distance",
        type: "number",
        iconPath: pathDb.pencil

    },
    {
        name: "Graine de génération",
        description: "Graine de génération du monde",
        category: "world",
        property: "level-seed",
        type: "input",
        iconPath: pathDb.pencil
    },
    {
        name: "Structures",
        description: "Défini si des structures (villages, forteresses, etc...) sont générées",
        category: "world",
        property: "generate-structures",
        type: "bool",
    },
    {
        name: "Nether",
        description: "Défini si il est possible de se rendre dans le nether",
        category: "world",
        property: "allow-nether",
        type: "bool",
    },
    {
        name: "Hauteur de construction",
        description: "Hauteur maximale de construction définie",
        category: "world",
        property: "max-build-height",
        type: "number",
        iconPath: pathDb.pencil
    },
    {
        name: "Apparition des monstres",
        description: "Défini si les monstres peuvent apparaitre",
        category: "world",
        property: "spawn-monsters",
        type: "bool"
    },
    {
        name: "Apparition des animaux",
        description: "Défini si les animaux peuvent apparaitre",
        category: "world",
        property: "spawn-animals",
        type: "bool"
    },
    {
        name: "Apparition des villageois",
        description: "Défini si les villageois peuvent apparaitre",
        category: "world",
        property: "spawn-npcs",
        type: "bool"
    },
    {
        name: "Nombre de joueurs",
        description: "Défini le nombre maximal de joueurs connectés simultanément.",
        category: "server",
        property: "max-players",
        type: "number",
    },
    {
        name: "Mode 'en ligne'",
        description: "Desactiver permet d'accepter les joueurs crackés mais cause aussi des problèmes de sécurité. En apprendre plus [lien / TODO]",
        category: "server",
        property: "online-mode",
        type: "bool",
    },
    {
        name: "MOTD",
        description: "Message de description du serveur dans le menu du jeu",
        category: "server",
        property: "motd",
        type: "input",
        iconPath: pathDb.pencil
    },
    {
        name: "Liste blanche",
        description: "Active une liste blanche, n'autorisant que certains joueur à se connecter",
        category: "server",
        property: "white-list",
        type: "bool",
    },
]