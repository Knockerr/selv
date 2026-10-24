<script>
  

  import { goto } from "$app/navigation";
  import Console from "$lib/components/panel/console.svelte";
  import DataDisplayer from "$lib/components/panel/dataDisplayer.svelte";
  import PanelTabList from "$lib/components/panel/panelTabList.svelte";
  import { startServer, stopServer } from "$lib/components/recurentActions.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  let serverIp = $state(10);
  let ramUsage = $state(10);
  let cpuUsage = $state(10);
  let onlinePlayers = $state(10);

  let consoleContent = $state("");

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";



  function getServerIp() {
    serverIp = fetch("http://localhost:40401/api/servers/" + uuid + "/ip", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data.ip);
        serverIp = data.ip;
      })
      .catch((err) => console.error(err));
  }

  function hookConsole() {
    const consoleWs = new WebSocket(
      `ws://localhost:40401/ws/servers/${uuid}/hooks/console`,
    );

    consoleWs.onopen = () => {
      console.info("Connected to console hook");
    };

    consoleWs.onmessage = (event) => {
      consoleContent += event.data + "\n";
      if (
        event.data.includes(
          "You need to agree to the EULA in order to run the server. Go to eula.txt for more info.",
        )
      )
        windowsManager.open("MinecraftEula-" + uuid);
    };

    consoleWs.onerror = (err) => {
      console.error("Error : ", err);
    };

    consoleWs.onclose = () => {
      console.info("Closed console webSocket.");
    };
  }

  function hookMetrics() {
    const consoleWs = new WebSocket(
      `ws://localhost:40401/ws/servers/${uuid}/hooks/metrics`,
    );

    consoleWs.onopen = () => {
      console.info("Connected to metrics hook");
    };

    consoleWs.onmessage = (event) => {
      const datas = JSON.parse(event.data);
      ramUsage = `${datas.ram}/MAX`;
      cpuUsage = `${datas.cpu}%`;
    };

    consoleWs.onerror = (err) => {
      console.error("Error : ", err);
    };

    consoleWs.onclose = () => {
      console.info("Closed metrics webSocket.");
    };
  }
</script>

<div class="container">
  <PanelTabList {uuid} />
  <div class="rightSideContainer">
    <div class="rightSideElemsContainer">
      <Console {consoleContent} {uuid} />
      <div class="executionPanel">
        <div class="buttonsRow">
          <button
            id="start"
            onclick={() => {
              startServer(uuid);
              hookConsole();
              hookMetrics();
            }}>START</button
          >
          <button
            id="stop"
            onclick={() => {
              stopServer(uuid);
            }}>STOP</button
          >
        </div>

        <ul class="datasList">
          <DataDisplayer stat="IP du serveur" bind:value={serverIp} />
          <DataDisplayer stat="Joueurs connectés" bind:value={onlinePlayers} />
          <DataDisplayer stat="Charge CPU" bind:value={cpuUsage} />
          <DataDisplayer stat="Ram utilisée" bind:value={ramUsage} />
        </ul>
      </div>
    </div>
  </div>
</div>

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
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }


  .rightSideContainer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 1;
    height: 100vh;
    width: 100%;
    gap: 20px;
  }

  .rightSideElemsContainer {
    width: 80%;
    height: 80%;
    display: flex;
    flex-direction: row;
    align-self: flex-end;
    gap: 20px;
    margin: 0;
  }

  .executionPanel {
    display: flex;
    align-items: center;
    flex-direction: column;
    flex: 1;
    width: fit-content;
    min-width: 150px;
    max-width: 250px;
  }

  .buttonsRow {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    width: 100%;
  }

  .buttonsRow button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    outline: none;
    border: none;
    width: 40%;
    height: 50px;
    border-radius: 15px;
  }

  #start {
    background-color: rgb(0, 255, 0);
  }

  #start:hover {
    background-color: rgb(0, 224, 0);
  }

  #start:active {
    background-color: rgb(0, 160, 0);
  }

  #stop {
    background-color: rgb(255, 0, 0);
  }

  #stop:hover {
    background-color: rgb(224, 0, 0);
  }

  #stop:active {
    background-color: rgb(160, 0, 0);
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
