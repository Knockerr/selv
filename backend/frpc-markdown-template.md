# Dossier mcPanel

Dans un principe de transparence, l'utilité de ce dossier et des fichiers qu'il contient sera détaillé ici.

Ce dossier est en effet généré par mcPanel pour son bon fonctionnement et les fonctionnalités que le logiciel propose.

## Structure:
```
mcPanel/
├── frpc/
│   ├── frpc.exe
│   └── frpc.toml
└── README.md
```

## Détail du contenu:

---


### Frpc
Ce dossier permet le bon fonctionnement du système de *tunnel* de vos serveurs.
C'est ce principe même qui vous permet à vos joueurs de se connecter à votre serveur de manière sécurisée en passant par une adresse IP.

**Fonctionnement:**

Ce système repose sur le projet open-source reconnu [Fast Reverse Proxy (ou frp)](https://github.com/fatedier/frp).

Deux fichiers sont présents dans le dossier: frpc.exe et frpc.toml

Frpc.exe est le programme établissant la connexion sécurisée entre ton serveur et mcPanel, pour que vos joueurs puissent toujours le rejoindre.

Le fichier frpc.toml contient la configuration de la connexion au serveur distant.
Ce dernier contient également un jeton d'authentification privé lié à ton compte. Ne partage" pas son contenu (capture d'écran, forum, etc...).

Ces fichiers sont régénérés automatiquement à chaque démarrage du ton serveur.

---