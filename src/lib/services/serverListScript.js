// @ts-nocheck

const myUUID =  crypto.randomUUID();
const pageNumber = document.getElementById("pageNumber");

console.info("Loading JavaScript...");

import {
    ws
} from './serverHandler/webSockets.js';

let interpretation;

/*
----------------------------------------

 -> Utilities

----------------------------------------
*/


/*
----------------------------------------

 -> Request utilities

----------------------------------------
*/

let availableHooks = ["demo"];

function hook(hook) {
    if (!availableHooks.includes(hook)) return;

    ws.send(JSON.stringify({
        "type": "hookRequest",
        "hook": hook,
    }));
    console.log("Hooked to " + hook);
}

let availableElementsToGet = ["serverIp"];

function get(get) {
    if (!availableElementsToGet.includes(get)) return;

    ws.send(JSON.stringify({
        "type": "get",
        "get": get,
        "myUUID": myUUID
    }));
    console.log("Getting " + get);
}



/*
----------------------------------------

 -> Handle entering messages.

----------------------------------------
*/

function handleHookData(payload) {
    switch (payload.hook) {
        case "demo":
            interpretation = "demo";
            break;

        default:
            console.warn("Unable to interprete hook " + payload);
            return;
    }
    console.log("Hooked understood as " + interpretation);
}

function handleGetReponse(payload) {
    switch (payload.get) {
        case "serverDatas":
            interpretation = "serverIp";
            renderServers(payload.datas);
            break;

        default:
            console.warn("Unable to interprete hook " + payload);
            return;
    }
    console.log("Hooked understood as " + interpretation);
}

function handleMessage(message) {
    console.log(`Message received on panel ${myUUID} -> ` + message);
    console.log("Interpreting..");

    let payload = JSON.parse(message);

    if (payload.serverUUID != null) return;
    if (payload.slUUID != myUUID) return;

    switch (payload.type) {
        case "hookData":
            handleHookData(payload);
            break;

        case "getResponse":
            handleGetReponse(payload);
            break;

        case "event":
            // TODO
            break;

        default:
            console.warn("Could not interprete message.. -> " + message);
            return;
    };
    console.log("Interpreted!");
    console.log("--------------------");
}



/*
----------------------------------------

 -> WebSockets Events Utilities

----------------------------------------
*/

function triggerEvent(event) {
    ws.send(JSON.stringify({
        "whichServiceAmI": "serverList",
        "type": "event",
        "event": event,
        "myUUID": myUUID
    }));
}

/*
----------------------------------------

 -> WebSockets Events

----------------------------------------
*/

ws.onopen = () => {
    console.info(`Websocket connexion established on ${myUUID} serverList!`);
    triggerEvent("serverListOpened");
};

ws.onmessage = (event) => {
    handleMessage(event.data);
};

ws.onerror = (err) => {
    console.warn(`Error on ${myUUID} -> ` + err);
};

/*
----------------------------------------

 -> Web Listeners

----------------------------------------
*/


// Fermeture de la page
window.addEventListener("beforeunload", (event) => {
});


console.log("Finished loading listeners!");
console.info("JavaScript loaded.");