import {
    dirname,
    join,
    localDataDir
} from "@tauri-apps/api/path";
import {
    exists,
    mkdir,
    readTextFile,
    writeTextFile
} from "@tauri-apps/plugin-fs";
import {
    onMount
} from "svelte";
import {
    get
} from "svelte/store";

const baseDir = await localDataDir();
const localManifestBase = await join(await localDataDir(), "Selv", "manifests")

class ManifestManager {
    constructor(name, fileName = "") {
        this.name = name;
        this.manifest = {};
        this.fileName = fileName ? fileName : `${name}.json`;
        this.localPath = "";
        this.remoteUrl = `https://selvmc.com/manifest/${this.fileName}`
    }

    async init() {
        this.localPath = await join(localManifestBase, this.fileName);
    }

    async updateLocal(newContent) {
        const parentDir = await dirname(this.localPath);
        await mkdir(parentDir, {
            recursive: true
        });

        await writeTextFile(
            this.localPath,
            JSON.stringify(newContent),
        );
    }

    async getLocal() {
        await this.init();

        const localExists = await exists(this.localPath);

        if (!localExists) return;

        const content = await readTextFile(this.localPath);

        return JSON.parse(content);
    }


    async getLatest() {
        const res = await fetch(this.remoteUrl);

        // Getting local version of the manifest
        const localManifestContent = await this.getLocal();

        // If unable to fetch remote, fallback on local version of the manifest
        if (!res.ok) return localManifestContent;

        const remoteManifestData = await res.json();

        if (!remoteManifestData) return;

        // Checking if remote manifest is newer than local
        if (!localManifestContent || localManifestContent.schema_version < remoteManifestData.schema_version) {
            this.updateLocal(remoteManifestData);
            return remoteManifestData;
        } else {
            return localManifestContent;
        }

    }
}

let versionsManifest;
let versionsManifestContent;

export async function initManifests() {
    // Minecraft servers versions manifest:
    versionsManifest = new ManifestManager("versions");
    versionsManifestContent = await versionsManifest.getLatest();
};

export function getMinecraftVersions() {
    return versionsManifestContent.software;
}