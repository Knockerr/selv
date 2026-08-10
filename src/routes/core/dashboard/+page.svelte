<script>
  import Articles from "$lib/components/dashboard/grid/Articles.svelte";
  import ServersNumber from "$lib/components/dashboard/grid/serversNumber.svelte";
  import Performances from "$lib/components/dashboard/grid/performances.svelte";
  import QuickActions from "$lib/components/dashboard/grid/quickActions.svelte";
  import RecentServers from "$lib/components/dashboard/grid/RecentServers.svelte";
  import ServerStats from "$lib/components/dashboard/grid/ServerStats.svelte";
  import UserInfos from "$lib/components/dashboard/grid/userInfos.svelte";
  import Availability from "$lib/components/dashboard/grid/Availability.svelte";
  import { onMount } from "svelte";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { stats } from "$lib/stores/stats.svelte";
  onMount(() => {
    sidebarStore.setCurrentTab("main", "Dashboard");
  });
</script>

<div class="page">
  <div class="dashContainer">
    <div class="titleSection">
      <h1 class="title">Dashboard</h1>
      <div class="mr-20 flex align">
        <IconButton
          iconPath={pathDb.arrowClockwise}
          iconSize="40px"
          onclick={stats.reloadDashboard}
          spinOnClick
          color="#ddd"
        />
      </div>
    </div>
    <div class="gridContainer">
      <div class="userId"><UserInfos /></div>
      <div class="serversNumber"><ServersNumber /></div>
      <div class="availability"><Availability /></div>
      <div class="serverStats"><ServerStats /></div>
      <div class="quickActions"><QuickActions /></div>
      <div class="recentServers"><RecentServers /></div>
      <div class="performances"><Performances /></div>
      <div class="articles"><Articles /></div>
    </div>
  </div>
</div>

<style>
  .page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .dashContainer {
    width: 100%;
    flex: 1;
    box-sizing: border-box;
    padding: 50px;
    padding-top: 40px;
    display: flex;
    flex-direction: column;
  }

  .titleSection {
    width: 100%;
    height: fit-content;
    margin-bottom: 25px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .title {
    margin: 0;
    margin-left: 10px;
    font-size: 2.5rem;
  }

  .gridContainer {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(auto-fill, 150px);
    grid-template-rows: repeat(auto-fill, 150px);
    grid-gap: 20px;
  }

  /* Haut gauche : identité utilisateur, gros bloc carré */
  .userId {
    grid-column: 1 / 3;
    grid-row: 1 / 3;
  }

  /* Haut, à côté de userId : deux stats rapides côte à côte */
  .serversNumber {
    grid-column: 3 / 5;
    grid-row: 1 / 2;
  }

  .availability {
    grid-column: 5 / 7;
    grid-row: 1 / 2;
  }

  /* Sous les deux stats rapides : barre perf plus large */
  .serverStats {
    grid-column: 3 / 7;
    grid-row: 2 / 3;
  }

  /* Colonne droite : deux blocs verticaux */
  .quickActions {
    grid-column: 7 / 9;
    grid-row: 1 / 4;
  }

  .performances {
    grid-column: 1 / 7;
    grid-row: 3 / 6;
  }

  /* Bande sous userId/performances : serveurs récents */
  .recentServers {
    grid-column: 9 / 11;
    grid-row: 1 / 4;
  }

  /* Pied de page pleine largeur : articles */
  .articles {
    grid-column: 7 / 11;
    grid-row: 4 / 6;
  }
</style>
