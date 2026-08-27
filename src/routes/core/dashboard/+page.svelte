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

    // Reloading all datas automatically all 60s
    // TODO : Switch runningServers and serversUptimes endpoint from REST to WS
    const interval = setInterval(stats.reloadDashboard, 60000);

    return () => clearInterval(interval); // Bonnes pratiques Svelte (nettoyage)
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
    overflow: hidden;
  }

  .dashContainer {
    width: 100%;
    height: 100%;
    flex: 1;
    box-sizing: border-box;
    padding: 20px;
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
  }

  .titleSection {
    width: 100%;
    height: fit-content;
    margin-bottom: 20px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
  }

  .title {
    margin: 0;
    margin-left: 10px;
    font-size: 2rem;
  }

  .gridContainer {
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .userId,
  .serversNumber,
  .availability,
  .serverStats,
  .quickActions,
  .recentServers,
  .performances,
  .articles {
    grid-column: auto;
    grid-row: auto;
    min-height: 120px;
  }

  @media (min-width: 768px) {
    .dashContainer {
      padding: 30px;
    }

    .gridContainer {
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
    }

    .userId {
      display: none !important;
    }
    .performances {
      display: none !important;
    }
    .articles {
      display: none !important;
    }
    .serverStats {
      display: none !important;
    }
  }

  @media (min-width: 1200px) {
    .userId,
    .serversNumber,
    .availability,
    .serverStats,
    .quickActions,
    .recentServers,
    .performances,
    .articles {
      display: flex !important;
    }
    .dashContainer {
      padding: 40px;
      padding-top: 30px;
    }

    .title {
      font-size: 2.5rem;
    }

    .gridContainer {
      grid-template-columns: repeat(10, 1fr);
      grid-template-rows: repeat(5, 1fr);
    }

    .userId {
      grid-column: 1 / 3;
      grid-row: 1 / 3;
    }

    .serversNumber {
      grid-column: 3 / 5;
      grid-row: 1 / 2;
    }

    .availability {
      grid-column: 5 / 7;
      grid-row: 1 / 2;
    }

    .serverStats {
      grid-column: 3 / 7;
      grid-row: 2 / 3;
    }

    .quickActions {
      grid-column: 7 / 9;
      grid-row: 1 / 4;
    }

    .recentServers {
      grid-column: 9 / 11;
      grid-row: 1 / 4;
    }

    .performances {
      grid-column: 1 / 7;
      grid-row: 3 / 6;
    }

    .articles {
      grid-column: 7 / 11;
      grid-row: 4 / 6;
    }
  }
</style>
