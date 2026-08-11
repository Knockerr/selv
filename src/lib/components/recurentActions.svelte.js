export const startServer = (uuid) => {
    fetch("http://localhost:8000/api/servers/" + uuid + "/start", {
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => console.log("data -> ", data))
        .catch((error) => console.error(error));
}

export const stopServer = (uuid) => {
    fetch("http://localhost:8000/api/servers/" + uuid + "/stop", {
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => console.log("data -> ", data))
        .catch((error) => console.error(error));
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