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

class ManifestManager {
    constructor(name, fileName = "") {
        this.name = name;
        this.fileName = fileName || `${name}.json`;
        this.remoteUrl = `https://selvmc.com/manifest/${this.fileName}`
    }

    async localPath() {
        return join(await localDataDir(), "Selv", "manifests", this.fileName);
    }

    async updateLocal(content) {
        const path = await this.localPath();
        await mkdir(await dirname(path), {
            recursive: true
        });
        await writeTextFile(path, JSON.stringify(content));
    }


    async getLocal() {
        try {
            const path = await this.localPath();
            if (!(await exists(path))) return null;
            return JSON.parse(await readTextFile(path));
        } catch (e) {
            console.error("Manifest local read failed:", e);
            return null;
        }
    }


    async getLatest() {
        const local = await this.getLocal();

        try {
            const res = await fetch(this.remoteUrl, {
                signal: AbortSignal.timeout(5000)
            });
            if (!res.ok) return local;
            const remote = await res.json();
            if (!remote) return local;
            if (!local || local.schema_version < remote.schema_version) {
                try {
                    await this.updateLocal(remote);
                } catch (e) {
                    console.error("Manifest write failed:", e);
                }
                return remote;
            }
            return local;
        } catch (e) {
            console.error("Manifest fetch failed", e)
            return local;
        }
    }
}

let baseDir;
let localManifestBase;

let versionsManifestContent = {};

export async function initManifests() {
    try {
        baseDir = await localDataDir();
        localManifestBase = await join(await localDataDir(), "Selv", "manifests");

        // Minecraft servers versions manifest:
        const versionsManifest = new ManifestManager("versions");
        versionsManifestContent = await versionsManifest.getLatest();
    } catch (e) {
        console.error("initManifests failed:", e);
    }
};

export function getMinecraftVersions() {
    return versionsManifestContent ?.software || {};
}