<script>
  import Select from "$lib/components/bits-ui/baseComponents/select.svelte";
  import { onMount } from "svelte";
  import Linechart from "../dashboardUtilities/Linechart.svelte";
  import StatDisplayer from "../dashboardUtilities/statDisplayer.svelte";
  import GridElem from "./gridElem.svelte";

  let datas = $state([]);

  async function updateDatas() {
    const res = await fetch("http://127.0.0.1:8000/api/serversPerfs");
    const data = await res.json();
    const perfs = data.perfs;

    datas = perfs.map((perf) => ({
      time: perf.label,
      cpu: perf.cpu,
      ram: perf.ram,
    }));
  }

  onMount(() => {
    updateDatas();
    // Update every min
    setInterval(updateDatas, 60000);
  });
</script>

<GridElem title="Performances des serveurs" reloadable onReload={updateDatas}>
  <div class="card">
    <div class="valuesContainer">
      <StatDisplayer title="RAM utilisée" value="8.6" unit="Go" />
      <StatDisplayer title="CPU utilisé" value="80" unit="%" />
      <StatDisplayer title="Débit descendant" value="10" unit="Mo.s" />
      <StatDisplayer title="Débit ascendant" value="2" unit="Mo.s" />
    </div>
    <div class="graphContainer">
      <span class="graphTitle">Dernière demie-heure</span>
      <Linechart {datas} />
    </div>
  </div>
</GridElem>

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
