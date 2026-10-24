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



let currentManifest = $state({});
let minecraftVersions = $derived(currentManifest.software || null);


const baseDir = await localDataDir();
const localManifestBase = await join(await localDataDir(), "Selv", "manifests")

async function updateLocalManifest(newContent) {
    const manifestPath = await join(localManifestBase, "versions.json");

    const parentDir = await dirname(manifestPath);
    await mkdir(parentDir, {
        recursive: true
    });

    await writeTextFile(
        manifestPath,
        JSON.stringify(newContent),
    );
}

async function getLocalManifest() {
    const manifestPath = await join(localManifestBase, "versions.json");

    const localManifestExists = await exists(manifestPath);

    if (!localManifestExists) return;

    const localManifestContent = await readTextFile(manifestPath);

    return JSON.parse(localManifestContent);
}


async function getLatestManifest() {
    const res = await fetch("https://selvmc.com/manifest/versions.json");


    // If unable to fetch, fallback on local version of the manifest
    if (!res.ok) return;

    const remoteManifestData = await res.json();

    if (!remoteManifestData) return;

    // Getting local version of the manifest
    const localManifestContent = await getLocalManifest();

    // Checking if remote manifest is newer than local
    if (!localManifestContent || localManifestContent.schema_version >= remoteManifestData.schema_version) {
        updateLocalManifest(remoteManifestData);
        return remoteManifestData;
    }

}

export async function initMinecraftServersVersions() {
    console.info("Initializing minecraft servers versions")
    // First, try to fetch the latest version of the manifest from the official Selvmc.com website
    const remoteManifestData = await getLatestManifest();
    if (remoteManifestData) currentManifest = remoteManifestData;
    else currentManifest = await getLocalManifest();
}

export function getMinecraftVersions() {
    return minecraftVersions;
}