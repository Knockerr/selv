<script>
  import { stats } from "$lib/stores/stats.svelte";
  import RecentServerItem from "../dashboardUtilities/RecentServerItem.svelte";
  import GridElem from "./gridElem.svelte";

  const recentServers = $derived(stats.recentServers);

  $inspect(recentServers);
</script>

<GridElem title="Serveurs récents">
  <div class="card" class:empty={recentServers.size === 0}>
    <div class="defaultContent">
      Aucun serveur à afficher. Crééez un serveur pour commencer.
    </div>
    {#each recentServers as uuid}
      <RecentServerItem {uuid} />
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

  .defaultContent {
    color: var(--foreground-alt);
    font-size: 0.95rem;
    position: relative;
    top: -20px;
    display: none;
    text-align: center;
    max-width: 95%;
  }

  .card.empty {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card.empty .defaultContent {
    display: inline;
  }
</style>
