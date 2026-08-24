

import {
    load
} from "@tauri-apps/plugin-store";
import {
    SvelteSet
} from "svelte/reactivity";

function createFolderSystem() {
    // Store handling
    let store = null;
    let foldersDatas = $state({});
    let allServers = $state(new SvelteSet());

    const state = $state({
        currentPageIndex: 0,
        currentSelectedFolder: 'all',
        pageLen: 7
    });

    async function loadDatas() {
        store = await load("folders.json");
        foldersDatas = await store.get("folderDatas") || {};
        let allServersVal = await store.get("allServers")
        allServers = new SvelteSet(allServersVal)
    }
    loadDatas();

    const serversToRender = $derived.by(() => {
        if (foldersDatas === {}) return [];

        if (state.currentSelectedFolder === "all") {
            return [...allServers].slice(
                state.currentPageIndex * state.pageLen,
                state.currentPageIndex * state.pageLen + state.pageLen
            );
        };

        let folderDatas = foldersDatas[state.currentSelectedFolder];

        if (!folderDatas) {
            console.warn("Empty folder");
            return []
        }

        return folderDatas.servers.slice(
            state.currentPageIndex * state.pageLen,
            state.currentPageIndex * state.pageLen + state.pageLen
        );
    });

    async function saveDatas() {
        if (!store) return;
        if (!foldersDatas) return;
        await store.set("folderDatas", foldersDatas);
        await store.set("allServers", [...allServers]);
        await store.save();
    };

    async function createFolder(folderName, isFav, servers) {
        foldersDatas[folderName] = {
            isFolderFav: isFav,
            servers: servers
        };
        await saveDatas();
    };

    // API exopsée 
    return {
        async reloadDatas() {
            store = await load("folders.json");
            foldersDatas = store.get("folderDatas")
        },

        get serversToRender() {
            return serversToRender;
        },

        get state() {
            return state;
        },

        get folderDatas() {
            return foldersDatas;
        },

        get foldersNames() {
            return Object.keys(foldersDatas);
        },

        get currentPageIndex() {
            return state.currentPageIndex;
        },

        get currentSelectedFolder() {
            return state.currentSelectedFolder;
        },

        get serversToRenderWithDatas() {
            return serversToRenderWithDatas
        },

        createFolder(folderName, isFav, servers) {
            createFolder(folderName, isFav, servers);
        },

        async editFolder(folderName, isFolderFav, servers) {
            foldersDatas = {
                ...foldersDatas,
                [folderName]: {
                    isFolderFav,
                    servers
                }
            };

            await saveDatas();
        },

        async addServer(uuid) {
            allServers.add(uuid);
            await saveDatas();
        },

        async removeServer(uuid) {
            allServers.delete(uuid);
            // Remove server from existing folders
            Object.entries(foldersDatas).forEach(([key, val]) => {
                val.servers = val.servers.filter(server => server !== uuid);
            });
            await saveDatas();
        },

        getFavoriteValue(folder) {
            if (foldersDatas[folder] === undefined) return false;
            return foldersDatas[folder].isFolderFav || false;
        },

        async toggleFavorite(folder) {
            foldersDatas = {
                ...foldersDatas,
                [folder]: {
                    ...foldersDatas[folder],
                    isFolderFav: !foldersDatas[folder].isFolderFav
                }
            }
            await saveDatas();
        },

        async setFavoriteValue(folder, isFavorite) {
            foldersDatas = {
                ...foldersDatas,
                [folder]: {
                    ...foldersDatas[folder],
                    isFolderFav: isFavorite
                }
            }
            await saveDatas();
        },

        async delete(folderName) {
            if (foldersDatas[folderName]) {
                delete foldersDatas[folderName];
                foldersDatas = {
                    ...foldersDatas
                };
                await saveDatas();
            }
        },

        setPage(page) {
            const folder = foldersDatas[state.currentSelectedFolder];
            if (!folder) return;
            const maxPageIndex = Math.ceil(folder.servers.length / state.pageLen)
            if (state.currentPageIndex <= maxPageIndex) state.currentPageIndex = page;
        },

        selectFolder(name) {
            state.currentSelectedFolder = name;
            state.currentPageIndex = 0;
        },

        nextPage() {
            const maxPageIndex = Math.ceil(foldersDatas[state.currentSelectedFolder].servers.length / state.pageLen) - 1;
            console.warn(maxPageIndex, state.currentPageIndex)
            if (state.currentPageIndex < maxPageIndex) state.currentPageIndex++;

        },

        prevPage() {
            state.currentPageIndex = Math.max(
                0,
                state.currentPageIndex - 1
            );
        },

        getFolder(folder) {
            const data = foldersDatas[folder];
            if (!data) return null;
            return {
                datas() {
                    return foldersDatas[folder]
                },
                addToFavorites() {
                    foldersDatas[folder].isFolderFav = true;
                    return folder;
                },
                removeFromFavorites() {
                    foldersDatas[folder].isFolderFav = false;
                    return folder;
                },
                get getServers() {
                    return foldersDatas[folder].servers;
                },
                contains(serverUuid) {
                    return foldersDatas[folder].servers.includes(serverUuid);
                },
                addServer(serverToAdd) {
                    foldersDatas[folder].servers.push(serverToAdd);
                    saveDatas();
                    return folder;
                },
                removeServer(serverUuid) {
                    foldersDatas[folder].servers = foldersDatas[folder].servers.filter((uuid) => uuid !== serverUuid);
                    saveDatas();
                    return folder;
                },
                async toggleServerPresence(serverUuid) {
                    if (this.getServers.includes(serverUuid)) {
                        this.removeServer(serverUuid);
                    } else {
                        this.addServer(serverUuid);
                    }
                    await saveDatas();
                },
                async rename(newName) {
                    folderSystem.selectFolder("all");

                    await createFolder(newName, foldersDatas[folder].isFolderFav, foldersDatas[folder].servers);

                    await folderSystem.delete(folder);

                    foldersDatas = {
                        ...foldersDatas
                    };

                    await saveDatas();
                    folderSystem.selectFolder(newName);
                    return newName;
                }
            };
        },

        get getAllServers() {
            return allServers;
        },

        getFolderData(folder) {
            return foldersDatas[folder];
        },

        async resetDatas() {
            foldersDatas = {};
            allServers = new SvelteSet();
            await saveDatas();
            console.info("Full datas reset has been completed succesfully.")
        },
    };
}

export const folderSystem = createFolderSystem();