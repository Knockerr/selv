<script>
  import { stats } from "$lib/stores/stats.svelte";
  import RecentServerItem from "../dashboardUtilities/RecentServerItem.svelte";
  import GridElem from "./gridElem.svelte";

  const recentServers = $derived(stats.recentServers);
</script>

<GridElem title="Serveurs récents">
  <div class="card">
    {#each recentServers as uuid}
      <RecentServerItem {uuid}/>
    {/each}
  </div>
</GridElem>

<style>
  .card {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 11px;
  }
</style>
