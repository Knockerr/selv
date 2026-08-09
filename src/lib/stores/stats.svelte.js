import {
    SvelteSet
} from "svelte/reactivity";
import {
    folderSystem
} from "./folderSystem.svelte";

function createStatsStore() {
    let store = $state({
        lastVisitedServer: false,
        recentServers: new SvelteSet([]),
    });

    function save() {
        localStorage.setItem("statsStore", JSON.stringify({
            lastVisitedServer: store.lastVisitedServer,
            recentServers: [...store.recentServers],
            serversPerfs: [],
        }));
    }

    function load() {
        const data = localStorage.getItem("statsStore");

        if (!data) {
            return null;
        }

        const parsed = JSON.parse(data);

        return {
            lastVisitedServer: parsed.lastVisitedServer,
            recentServers: new SvelteSet(parsed.recentServers ?? [])
        };
    }

    function init() {
        if (load()) {
            store = load()
        } else {
            save()
        }
    }
    init();

    return {
        get lastVisitedServer() {
            return store.lastVisitedServer;
        },

        setLastVisitedServer(uuid) {
            store.lastVisitedServer = uuid;
            save()
        },

        get recentServers() {
            return store.recentServers
        },

        addRecentServer(uuid) {
            if (store.recentServers.has(uuid)) store.recentServers.delete(uuid);
            store.recentServers = new SvelteSet([
                uuid,
                ...store.recentServers
            ]);
            const len = store.recentServers.size
            if (len > 8) {
                store.recentServers = new SvelteSet([...store.recentServers].slice(len - 8, len));
            }
            save();
        },
        
    }
}

export const stats = createStatsStore()