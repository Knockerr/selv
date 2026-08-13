<script>
  // @ts-nocheck

  import { goto } from "$app/navigation";
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import Console from "$lib/components/panel/console.svelte";
  import DataDisplayer from "$lib/components/panel/dataDisplayer.svelte";
  import PanelTabList from "$lib/components/panel/panelTabList.svelte";
  import {
  postServer,
    startServer as startServerFn,
    stopServer as stopServerFn,
  } from "$lib/components/recurentActions.svelte";
  import EulaWindow from "$lib/components/windowsSystem/WindowsBank/eulaWIndow/eulaWindow.svelte";
  import { windowsManager } from "$lib/components/windowsSystem/windowsManager.svelte";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { stats } from "$lib/stores/stats.svelte";
  import { onDestroy, onMount, untrack } from "svelte";

  let serverIp = $state("Récuperation...");
  let serverName = $state("Récuperation...");
  let ramUsage = $state("Récuperation...");
  let cpuUsage = $state("Récuperation...");
  let uptime = $state("Récuperation...");
  let onlinePlayers = $state("Récuperation...");
  let serverStatus = $state("");

  let recovery = false;

  let consoleContent = $state("");

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";

  onMount(() => {
    sidebarStore.setCurrentTab("panel", "Console");
  });

  function startServer() {
    consoleContent = "";
    startServerFn(uuid);
    serverStatus = "on";
    hookConsole();
    hookMetrics();
  }

  async function stopServer() {
    serverStatus = "closing";

    stopServerFn(uuid);

    consoleWs?.close();
    metricsWs?.close();
    serverStatus = "off";
  }

  function getServerIp() {
    serverIp = fetch("http://localhost:8000/api/servers/" + uuid + "/ip", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data.ip);
        serverIp = data.ip;
      })
      .catch((err) => console.error(err));
  }

  function capitalize(str) {
    return String(str).charAt(0).toUpperCase() + String(str).slice(1);
  }

  function getServerName() {
    fetch("http://localhost:8000/api/servers/" + uuid + "/name", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        serverName = capitalize(data.name);
      })
      .catch((err) => console.error(err));
  }

  let consoleWs = $state();
  function hookConsole() {
    consoleWs = new WebSocket(
      `ws://localhost:8000/ws/servers/${uuid}/hooks/console`,
    );

    consoleWs.onopen = () => {
      console.info("Connected to console hook");
    };

    consoleWs.onmessage = (event) => {
      consoleContent += event.data + "\n";
      // TODO (urgent) : Switch EULA check to backend side (auto check at each start of eula.txt content, prevents players opening windows by typing the str below)
      if (
        event.data.includes(
          "You need to agree to the EULA in order to run the server. Go to eula.txt for more info.",
        )
      )
        uiStore.openDialog("eulaConfirm");
    };

    consoleWs.onerror = (err) => {
      console.error("Error : ", err);
    };

    consoleWs.onclose = () => {
      console.info("Closed console webSocket.");
    };
  }

  let metricsWs;
  function hookMetrics() {
    metricsWs = new WebSocket(
      `ws://localhost:8000/ws/servers/${uuid}/hooks/metrics`,
    );

    metricsWs.onopen = () => {
      console.info("Connected to metrics hook");
    };

    metricsWs.onmessage = (event) => {
      const datas = JSON.parse(event.data);
      ramUsage = `${datas.ram}/MAX`;
      cpuUsage = `${datas.cpu}%`;
    };

    metricsWs.onerror = (err) => {
      console.error("Error : ", err);
    };

    metricsWs.onclose = () => {
      console.info("Closed metrics webSocket.");
    };
  }

  async function recoverConsoleLogs() {
    let serverLogs = [];
    await fetch("http://localhost:8000/api/servers/" + uuid + "/logs", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        serverLogs = data.logs;
        serverLogs.forEach((line) => {
          consoleContent += line;
        });
      })
      .catch((err) => console.error(err));
  }

  onMount(async () => {
    stats.setLastVisitedServer(uuid);
    stats.addRecentServer(uuid);

    // Fetch IP (temp)
    let _ = await fetch("http://localhost:8000/api/servers/" + uuid + "/ip", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data.ip);
        serverIp = data.ip;
      })
      .catch((err) => console.error(err));

    // Getting server state on Mount
    _ = await fetch("http://localhost:8000/api/servers/" + uuid + "/status", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        serverStatus = data.status;
        if (serverStatus === "on") recovery = true;
      })
      .catch((err) => console.error(err));

    if (serverStatus === "on") {
      console.info("Server status detected as on.");
      if (recovery) recoverConsoleLogs();
      hookConsole();
      hookMetrics();
    }

    getServerName();
  });

  onDestroy(() => {
    if (serverStatus === "on") {
      consoleWs.close();
      metricsWs.close();
    }
  });
</script>

<div class="container">
  <h1 class="title">{serverName}</h1>

  <div class="rightSideElemsContainer">
    <Console
      {consoleWs}
      {consoleContent}
      {uuid}
      bind:content={consoleContent}
    />
    <div class="executionPanel">
      <div class="buttonsRow">
        <Button
          onclick={() => {
            startServer();
          }}
          style="width: 85px; height:45px; background-color:rgba(80, 80, 255, 0.9); letter-spacing:1px;"
          disabled={!(serverStatus === "off")}
          iconPath="">START</Button
        >
        <Button
          onclick={() => {
            stopServer();
          }}
          style="width: 85px; height:45px; background-color:rgba(255, 25, 25, 0.8); letter-spacing:1px;"
          disabled={!(serverStatus === "on")}
          iconPath="">STOP</Button
        >
      </div>

      <ul class="datasList">
        <DataDisplayer stat="IP du serveur" bind:value={serverIp} />
        <DataDisplayer stat="Disponibilité" bind:value={uptime} />
        <DataDisplayer stat="Joueurs connectés" bind:value={onlinePlayers} />
        <DataDisplayer stat="Charge CPU" bind:value={cpuUsage} />
        <DataDisplayer stat="Ram utilisée" bind:value={ramUsage} />
      </ul>
    </div>
  </div>
</div>

<Confirm 
  title="EULA"
  description="En cliquant sur 'accepter', vous confirmez accepter l'EULA de Minecraft (https://aka.ms/MinecraftEULA)"
  onConfirm={() => postServer(uuid, "acceptEula")}
  name="eulaConfirm"
/>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Funnel+Sans:ital,wght@0,300..800;1,300..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Zain:ital,wght@0,200;0,300;0,400;0,700;0,800;0,900;1,300;1,400&family=Zalando+Sans:ital,wght@0,200..900;1,200..900&display=swap");

  :root {
    --interFont: "Inter", sans-serif;
    --zalondoFont: "Zalando Sans", sans-serif;
    --zainFont: "Zain", sans-serif;
    --funnelFont: "Funnel Sans", sans-serif;
    --robotoFont: "Roboto", sans-serif;
  }

  .container {
    background-color: #030712;
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
  }

  .title {
    width: 100%;
    padding: 5px 50px;
    box-sizing: border-box;
    font-family: var(--robotFont);
    font-size: 3rem;
    font-weight: 500;
  }

  .rightSideElemsContainer {
    width: 80%;
    height: 100%;
    display: flex;
    flex-direction: row;
    align-self: flex-end;
    gap: 20px;
    margin: 0;
    position: relative;
    left: -5%;
    margin-bottom: 5%;
  }

  .executionPanel {
    display: flex;
    align-items: center;
    flex-direction: column;
    flex: 1;
    width: fit-content;
    min-width: 150px;
    max-width: 250px;
    height: 80%;
    padding-top: 10px;
  }

  .buttonsRow {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    width: 100%;
  }

  .datasList {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
    gap: 20px;
  }
</style>
