<script>
  import { onMount, untrack } from "svelte";
  import GridElem from "./gridElem.svelte";
  import { stats } from "$lib/stores/stats.svelte";
  import { get } from "$lib/components/recurentActions.svelte";

  // TODO : Set colors to the state span automatically
  let state = $state("operational");
  let stateDisplay = $derived(
    {
      operational: "Opérationnel",
      partial_outage: "Perturbée",
      maintenance: "Maintenance",
      major_outage: "Indisponible",
      no_internet: "Hors ligne",
    }[state],
  );
  let stateColor = $derived(
    {
      operational: "var(--foreground)",
      partial_outage: "#ff8000",
      maintenance: "#ff8000",
      major_outage: "var(--dangerous)",
      no_internet: "var(--dangerous)",
    }[state],
  );

  async function checkInternet() {
    try {
      await fetch("https://google.com", {
        method: "HEAD",
        mode: "no-cors",
        cache: "no-store",
      });
      return true;
    } catch (error) {
      return false;
    }
  }

  async function updateValue() {
    const isConnected = await checkInternet();
    if (!isConnected) {
      state = "no_internet";
      return;
    }
    try {
      const res = await fetch("https://api.selvmc.com/status");
      if (!res.ok) throw Error();

      const data = await res.json();
      if (!data) throw Error();

      state = data.status;
    } catch {
      state = "major_outage";
    }
  }

  $inspect(state).with(() => {
    console.warn("STATET > " + state);
  });

  onMount(() => {
    updateValue();
  });

  $effect(() => {
    stats.dashboardReloadTrigger;
    untrack(() => {
      updateValue();
    });
  });
</script>

<GridElem title="Disponibilité" reloadable onReload={updateValue}>
  <div class="card">
    <span class="state" style:color={stateColor}>{stateDisplay}</span>
  </div>
</GridElem>

<style>
  .card {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    box-sizing: border-box;
    padding: 10px;
    padding-top: 0;
    height: 100%;
    width: 100%;
  }

  span {
    font-size: 2.75rem;
    position: relative;
    top: -10px;
  }
</style>
