<script>
  import { onMount, untrack } from "svelte";
  import ServerStat from "../dashboardUtilities/ServerStat.svelte";
  import GridElem from "./gridElem.svelte";
  import { stats } from "$lib/stores/stats.svelte";

  let serversTypes = $state([]);
  let serversUptimes = $state([]);
  let mostUsedVersions = $state([]);

  function formatSec(sec) {
    const hours = Math.floor(sec / 3600);
    sec %= 3600;
    const minutes = Math.floor(sec / 60);
    const seconds = sec % 60;

    return `${hours != 0 ? hours : "00"}h${minutes != 0 ? minutes : "00"}m${seconds != 0 ? seconds : "00"}s`;
  }

  async function getFetch(endpoint) {
    const res = await fetch(`http://localhost:8000/api/${endpoint}`);
    const datas = await res.json();
    return datas;
  }

  async function updateDatas() {
    // Servers types:
    let serversTypesFetch = await getFetch("servers/stats/serversTypes");
    serversTypesFetch = serversTypesFetch.serversTypes;
    serversTypes = Object.entries(serversTypesFetch).map(([key, value]) => ({
      key: key,
      value: value,
    }));

    // Servers uptime:
    let serverUptimeFetch = await getFetch("servers/stats/serversUptimes");
    serverUptimeFetch = serverUptimeFetch.serversUptimes;
    let serversUptimesDatas = Object.entries(serverUptimeFetch).map(
      ([key, value]) => ({
        key: key,
        value: value,
        valueFormatted: formatSec(value),
      }),
    );
    serversUptimes = serversUptimesDatas
      .sort((a, b) => b.value - a.value)
      .slice(0, 10);
  }

  onMount(() => {
    updateDatas();
  });

  $effect(() => {
    stats.dashboardReloadTrigger;
    untrack(() => {
      updateDatas();
    });
  });
</script>

<GridElem title="Statistiques" reloadable onReload={updateDatas}>
  <div class="card">
    <ServerStat
      graphType="pie"
      data={serversTypes}
      title="Types de serveurs"
      description="Répartition des types de vos serveurs"
      tooltipLabel="Nombre de serveurs"
    />
    <ServerStat
      graphType="pie"
      data={serversUptimes}
      title="Utilisation serveur"
      description="Répartition du temps d'utilisation de vos serveurs"
      tooltipLabel="Temps d'utilisation"
    />
  </div>
</GridElem>

<style>
  .card {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;
  }
</style>
