<script>
  import Select from "$lib/components/bits-ui/baseComponents/select.svelte";
  import { onDestroy, onMount, untrack } from "svelte";
  import Linechart from "../dashboardUtilities/Linechart.svelte";
  import StatDisplayer from "../dashboardUtilities/statDisplayer.svelte";
  import GridElem from "./gridElem.svelte";
  import { stats } from "$lib/stores/stats.svelte";

  let componentKey = $state(0);

  let datas = $state([]);
  let cpu = $state("--");
  let ram = $state("--");

  let datasWs;
  function hookServersPerfsDatas() {
    datasWs = new WebSocket(
      "ws://localhost:8000/ws/servers/hooks/stats/serversPerfs?delay=1&content=last",
    );

    datasWs.onopen = () => {
      console.info("Connected to servers perfs (datas) hook");
    };

    datasWs.onmessage = (event) => {
      const data = JSON.parse(event.data);
      cpu = data.cpu;
      ram = data.ram;
    };

    datasWs.onerror = (err) => {
      console.error("Error : ", err);
    };

    datasWs.onclose = () => {
      console.info("Closed servers perfs (datas) webSocket.");
    };
  }

  let graphWs;
  function hookServersPerfsGraph() {
    graphWs = new WebSocket(
      "ws://localhost:8000/ws/servers/hooks/stats/serversPerfs?delay=2&label=true",
    );

    graphWs.onopen = () => {
      console.info("Connected to servers perfs (graph) hook");
    };

    graphWs.onmessage = (event) => {
      const data = JSON.parse(event.data);
      datas = data.map((perf) => ({
        time: perf.label,
        cpu: perf.cpu,
        ram: perf.ram,
      }));
    };

    graphWs.onerror = (err) => {
      console.error("Error : ", err);
    };

    graphWs.onclose = () => {
      console.info("Closed servers perfs (graph) webSocket.");
    };
  }

  const reloadKey = () => (componentKey += 1);

  onDestroy(() => {
    datasWs.close();
    graphWs.close();
  });

  onMount(() => {
    hookServersPerfsDatas();
    hookServersPerfsGraph();
  });
</script>

{#key componentKey}
  <GridElem title="Performances des serveurs" reloadable onReload={reloadKey}>
    <div class="card">
      <div class="valuesContainer">
        <StatDisplayer title="RAM utilisée" value={ram} unit="Go" />
        <StatDisplayer title="CPU utilisé" value={cpu} unit="%" />
        <StatDisplayer title="Débit descendant" value="10" unit="Mo.s" />
        <StatDisplayer title="Débit ascendant" value="2" unit="Mo.s" />
      </div>
      <div class="graphContainer">
        <span class="graphTitle">Dernière demie-heure</span>
        <Linechart {datas} />
      </div>
    </div>
  </GridElem>
{/key}

<style>
  .card {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 11px;
  }

  .valuesContainer,
  .graphContainer {
    height: 100%;
  }

  .valuesContainer {
    width: 20%;
    padding-left: 15px;
  }

  .graphContainer {
    position: relative;
    flex: 1;
    box-sizing: border-box;
    padding: 20px;
  }

  .graphTitle {
    position: absolute;
    top: -20px;
    right: 60px;
    font-size: 1rem;
  }
</style>
