<script>
  import { onMount, untrack } from "svelte";
  import GridElem from "./gridElem.svelte";
  import { stats } from "$lib/stores/stats.svelte";

  // TODO : Set colors to the state span automatically
  let state = $state("Opérationnel");

  function updateValue() {
    // TODO : Logic
  }

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
    <span class="state">{state}</span>
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
