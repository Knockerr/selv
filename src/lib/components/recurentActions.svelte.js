import {
    supabase
} from "$lib/supabaseClient.svelte";

export const startServer = (uuid) => {
    postServer(uuid, "start")
}

export const stopServer = async (uuid) => {
    postServer(uuid, "stop")

}

export const post = async (endpoint, body) => {
    const options = {
        method: "POST",
    };

    if (body) {
        options.headers = {
            "Content-Type": "application/json",
        };
        options.body = JSON.stringify(body);
    }

    try {
        const res = await fetch(
            `http://localhost:8000/${action}`,
            options
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;
    } catch (error) {
        console.error(error);
    }
}

export const postServer = async (uuid, action, body) => {
    const options = {
        method: "POST",
    };

    if (body) {
        options.headers = {
            "Content-Type": "application/json",
        };
        options.body = JSON.stringify(body);
    }

    try {
        const res = await fetch(
            `http://localhost:8000/api/servers/${uuid}/${action}`,
            options
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;
    } catch (error) {
        console.error(error);
    }
};

export const getServer = async (uuid, endpoint) => {
    try {
        const res = await fetch(
            `http://localhost:8000/api/servers/${uuid}/${endpoint}`, {
                method: "GET"
            }
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;

    } catch (error) {
        console.error(error);
    }
};

export const getDeletedServer = async (uuid, endpoint) => {
    try {
        const res = await fetch(
            `http://localhost:8000/api/deletedServers/${uuid}/${endpoint}`, {
                method: "GET"
            }
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;

    } catch (error) {
        console.error(error);
    }
};

export const postDeletedServer = async (uuid, action, body) => {
    const options = {
        method: "POST",
    };

    if (body) {
        options.headers = {
            "Content-Type": "application/json",
        };
        options.body = JSON.stringify(body);
    }

    try {
        const res = await fetch(
            `http://localhost:8000/api/deletedServers/${uuid}/${action}`,
            options
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;
    } catch (error) {
        console.error(error);
    }
};

export const getAccessToken = async () => {
    await supabase.auth.refreshSession()
    const session = await supabase.auth.getSession()
    console.warn(session)
    // Letting time for new token to activate
    await new Promise(r => setTimeout(r, 200));

    return session.data.session.access_token;
}

export const postServerWithCredentials = async (uuid, action, body) => {
    const accessToken = await getAccessToken();
    if (!accessToken) return;
    const options = {
        method: "POST",
    };

    options.headers = {
        "Content-Type": "application/json",
        "accessToken": accessToken
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const res = await fetch(
            `http://localhost:8000/api/servers/${uuid}/${action}`,
            options
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;
    } catch (error) {
        console.error(error);
    }
};

export const getServerWitCredentials = async (uuid, endpoint) => {
    const accessToken = await getAccessToken();
    if (!accessToken) return;
    try {
        const res = await fetch(
            `http://localhost:8000/api/servers/${uuid}/${endpoint}`, {
                method: "GET",
                headers: {
                    accessToken: accessToken
                }
            }
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;

    } catch (error) {
        console.error(error);
    }
};


export const getExternalBackend = async (endpoint) => {
    const accessToken = await getAccessToken();
    if (!accessToken) return;
    try {
        const res = await fetch(
            `http://localhost:4555/api/tunnels/${endpoint}`, {
                method: "GET",
                headers: {
                    authorization: `Bearer ${accessToken}`
                }
            }
        );

        const data = await res.json();

        console.log("data -> ", data);

        return data;

    } catch (error) {
        console.error(error);
    }
};


export const formatSeconds = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;

    if (h) {

        return `${h}h${m}m${s}s`;
    } else if (m) {
        return `${m}m${s}s`;

    } else {
        return `${s}s`;

    }

}