import {
    supabase
} from "$lib/supabaseClient.svelte";

export const startServer = (uuid) => {
    postServer(uuid, "start")
}

export const stopServer = async (uuid) => {
    postServer(uuid, "stop")

}


export const post = async (endpoint, body, headers) => {
    const options = {
        method: "POST",
        headers: {
            ...(body ? {
                "Content-Type": "application/json"
            } : {}),
            ...headers
        }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const res = await fetch(
        endpoint,
        options,
    );

    if (!res.ok) {
        let error;

        try {
            error = await res.json();
        } catch {
            error = await res.text();
        }
        console.error(`[ POST ] ${endpoint} =>`, {
            status: res.status,
            statusText: res.statusText,
            error
        });

        return;
    }

    const data = await res.json();

    console.log(`[ POST ] to ${endpoint} =>`, data);

    return data;
}

export const get = async (endpoint, headers) => {
    try {
        const res = await fetch(
            endpoint, {
                method: "GET",
                headers: headers || {}
            }
        );

        if (!res.ok) {
            let error;

            try {
                error = await res.json();
            } catch {
                error = await res.text();
            }
            console.error(`[ POST ] ${endpoint} =>`, {
                status: res.status,
                statusText: res.statusText,
                error
            });

            return;
        }


        const data = await res.json();

        console.log(`[ GET ] to ${endpoint} =>`, data);
        return data;

    } catch (error) {
        console.error(error);
    }
};

export const postServer = async (uuid, action, body) => {
    return await post(`http://localhost:8000/api/servers/${uuid}/${action}`, body)

};

export const getServer = async (uuid, endpoint) => {
    return await get(`http://localhost:8000/api/servers/${uuid}/${endpoint}`)
};

export const getDeletedServer = async (uuid, endpoint) => {
    return await get(`http://localhost:8000/api/deletedServers/${uuid}/${endpoint}`)
};

export const postDeletedServer = async (uuid, endpoint) => {
    return await post(`http://localhost:8000/api/deletedServers/${uuid}/${endpoint}`)
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

    return await post(`http://localhost:8000/api/servers/${uuid}/${action}`, body, {
        accessToken: accessToken
    })
};

export const getServerWithCredentials = async (uuid, action, body) => {
    const accessToken = await getAccessToken();
    if (!accessToken) return;

    return await get(`http://localhost:8000/api/servers/${uuid}/${action}`, body, {
        "accessToken": accessToken
    })
};

export const getExternalBackend = async (endpoint) => {
    const accessToken = await getAccessToken();
    if (!accessToken) return;
    return await get(`http://92.222.68.29:4555/api/tunnels/${endpoint}`, {
        authorization: `Bearer ${accessToken}`
    })
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