import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
import {
    init
} from "$lib/logger.svelte";

init();

const errorWs = new WebSocket(
    "ws://localhost:8000/ws/errorHandling/subscribe",
);

errorWs.onopen = () => {
    console.log("Created error ws succesfully");

};

errorWs.onmessage = async (event) => {
    console.warn("Error received from py backend");
    const data = event.data;
    // Wait to make sure that detailed backend error takes priority over js fetch error msg
    await new Promise(r => setTimeout(r, 500))
    uiStore.reportError(`[BACKEND] ${data}`);
};