// @ts-nocheck

import {
    windowsManager
} from "$lib/components/windowsSystem/windowsManager.svelte";
import {
    load
} from "@tauri-apps/plugin-store";
import {
    SvelteSet
} from "svelte/reactivity";

function readJsonFile(file) {
    const reader = new FileReader();
    return new Promise((resolve, reject) => {
        reader.onload = () => resolve(JSON.parse(reader.result));
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

function createFolderSystem() {
    const state = $state({
        folderDatas: load("folders.json", {
            autoSave: 1
        }) || {},
        currentPageIndex: 0,
        currentSelectedFolder: 'all',
        pageLen: 7,
        //allServers: new SvelteSet(JSON.parse(localStorage.getItem("allServers"))) || new SvelteSet(),
    });

    const serversToRender = $derived.by(() => {
        const folderDatas = state.folderDatas[state.currentSelectedFolder];

        if (!folderDatas) {
            console.warn("Empty folder");
            return []
        }

        return folderDatas.servers.slice(
            state.currentPageIndex * state.pageLen,
            state.currentPageIndex * state.pageLen + state.pageLen
        );
    });

    // Function that keeps state.allServers up to date 
    // "servers" is an array
    function editAllServers(servers) {
        let allServersVal = [];
        servers.forEach(uuid => {
            allServersVal.push(uuid);
        });
        state.allServersJson.set('content', {
            content: allServersVal
        });
        state.allServers.save();
    };

    function saveDatas() {
        console.warn("SaveDatas > ", state.allServers);
        state.folderDatas.save();
        state.allServers.save();
        // localStorage.setItem("folders", JSON.stringify(state.folderDatas));
        // localStorage.setItem("allServers", JSON.stringify([...state.allServers]));
    };

    function createFolder(folderName, isFav, servers) {
        // editAllServers(servers);
        state.folderDatas[folderName] = {
            isFolderFav: isFav,
            servers: servers
        };
        saveDatas();
    };

    // API exopsée 
    return {
        reloadDatas() {
            state.folderDatas = JSON.parse(load("folders.json"));
        },

        get serversToRender() {
            return serversToRender;
        },

        get state() {
            return state;
        },

        get folderDatas() {
            return state.folderDatas;
        },

        get foldersNames() {
            return Object.keys(state.folderDatas);
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

        editFolder(folderName, isFolderFav, servers) {
            editAllServers(servers);
            state.folderDatas = {
                ...state.folderDatas,
                [folderName]: {
                    isFolderFav,
                    servers
                }
            };

            saveDatas();
        },

        getFavoriteValue(folder) {
            if (state.folderDatas[folder] === undefined) return false;
            return state.folderDatas[folder].isFolderFav || false;
        },

        toggleFavorite(folder) {
            state.folderDatas = {
                ...state.folderDatas,
                [folder]: {
                    ...state.folderDatas[folder],
                    isFolderFav: !state.folderDatas[folder].isFolderFav
                }
            }
            saveDatas();
        },

        setFavoriteValue(folder, isFavorite) {
            state.folderDatas = {
                ...state.folderDatas,
                [folder]: {
                    ...state.folderDatas[folder],
                    isFolderFav: isFavorite
                }
            }
            saveDatas();
        },

        delete(folderName) {
            if (state.folderDatas[folderName]) {
                delete state.folderDatas[folderName];
                state.folderDatas = {
                    ...state.folderDatas
                };
                saveDatas();
            }
        },

        setPage(page) {
            const folder = state.folderDatas[state.currentSelectedFolder];
            if (!folder) return;
            const maxPageIndex = Math.ceil(folder.servers.length / state.pageLen)
            if (state.currentPageIndex <= maxPageIndex) state.currentPageIndex = page;
        },

        selectFolder(name) {
            state.currentSelectedFolder = name;
            state.currentPageIndex = 0;
        },

        nextPage() {
            const maxPageIndex = Math.ceil(state.folderDatas[state.currentSelectedFolder].servers.length / state.pageLen) - 1;
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
            const data = state.folderDatas[folder];
            if (!data) return null;
            return {
                datas() {
                    return state.folderDatas[folder]
                },
                addToFavorites() {
                    state.folderDatas[folder].isFolderFav = true;
                    return folder;
                },
                removeFromFavorites() {
                    state.folderDatas[folder].isFolderFav = false;
                    return folder;
                },
                get getServers() {
                    return state.folderDatas[folder].servers;
                },
                contains(serverUuid) {
                    return state.folderDatas[folder].servers.includes(serverUuid);
                },
                addServer(serverToAdd) {
                    state.folderDatas[folder].servers.push(serverToAdd);
                    editAllServers([serverToAdd]);
                    return folder;
                },
                removeServer(serverUuid) {
                    state.folderDatas[folder].servers = state.folderDatas[folder].servers.filter((uuid) => uuid !== serverUuid);

                    return folder;
                },
                toggleServerPresence(serverUuid) {
                    if (this.getServers.includes(serverUuid)) {
                        this.removeServer(serverUuid);
                    } else {
                        this.addServer(serverUuid);
                    }
                    saveDatas();
                },
                rename(newName) {
                    folderSystem.selectFolder("all");

                    createFolder(newName, state.folderDatas[folder].isFolderFav, state.folderDatas[folder].servers);

                    windowsManager.close("FolderWindow-" + folder);

                    folderSystem.delete(folder);

                    state.folderDatas = {
                        ...state.folderDatas
                    };

                    saveDatas();
                    folderSystem.selectFolder(newName);
                    return newName;
                }
            };
        },

        get getAllServers() {
            return state.allServers;
        },

        getFolderData(folder) {
            return state.folderDatas[folder];
        },

        resetFolder() {
            state.folderDatas = {};
            state.allServers = new SvelteSet();
            saveDatas();
            createFolder("all", true, []);
            saveDatas();
        },

        addServer(serverUuid) {
            console.log("Adding ", serverUuid, " to allServers");
            state.allServers.add(serverUuid);
            saveDatas();
        },
        forceAllFoldersEdit(allServers) {
            state.allServers = new SvelteSet(allServers);
            saveDatas();
        },
    };
}

export const folderSystem = createFolderSystem();

