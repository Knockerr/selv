<script>
  import { onMount } from "svelte";
  import GridElem from "./gridElem.svelte";
  import Separator from "$lib/components/bits-ui/baseComponents/Separator.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import StatDisplayer from "../dashboardUtilities/statDisplayer.svelte";

  let totalServers = $state("-");
  let runnigServers = $state("-");

  async function updateValue() {
    totalServers = folderSystem.getAllServers.size;
    // Fetch n of started servers
    // TODO : Switch to WS en centralize this kind of datas in stats store
    const res = await fetch(
      "http://localhost:8000/api/servers/runningServers",
      {
        method: "GET",
      },
    );
    const datas = await res.json();
    runnigServers = datas["runningServers"].length;
  }

  onMount(async () => {
    // Shield to prevent loading too soon
    await new Promise((res) => setTimeout(res, 150));
    updateValue();
  });
</script>

<GridElem title="Nombre de serveurs" reloadable onReload={updateValue}>
  <div class="card">
    <div class="cardSubContainer totalServersContainer">
      <StatDisplayer title="total" value={totalServers} style="padding: 0;" />
    </div>

    <div class="flex flex-row w-[50%] h-full items-center">
      <div class="separator"></div>

      <div class="cardSubContainer runingServersContainer">
        <StatDisplayer
          title="Actifs"
          value={runnigServers}
          style="padding: 0;"
        />
      </div>
    </div>
  </div></GridElem
>

<style>
  .card {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    padding: 10px;
    top: -5px;
    padding-top: 0;
    height: 100%;
    width: 100%;
  }

  .cardSubContainer {
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    padding: 0 10px;
  }

  .totalServers,
  .runingServers {
    font-size: 3rem;
  }

  .runingServersContainer {
    margin-left: 5px;
  }

  .separator {
    height: 80%;
    width: 1px;
    background-color: var(--muted);
  }

  .precision {
    color: var(--foreground);
    font-size: 1rem;
  }
</style>
