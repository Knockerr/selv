<script>
  // @ts-nocheck
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { online } from "svelte/reactivity/window";
  import ServerCard from "./ServerCard.svelte";

  const { folderName } = $props();

  const allServers = $derived(folderSystem.getAllServers);

  $inspect(allServers).with(() => {console.info("allServers", allServers)})

  const serversInFolder = $derived(
    folderSystem.getFolder(folderName)?.getServers || []
  );

  const otherServers = $derived(
    [...allServers].filter((uuid) => !(serversInFolder.includes(uuid)))
  );
  
  let serversName = $state({});
  $effect(() => {
    [...serversInFolder, ...otherServers].forEach((uuid) => {
      fetch(`http://127.0.0.1:8000/api/servers/${uuid}/serverListDatas`)
        .then((res) => res.json())
        .then((data) => {
          serversName[uuid] = data?.name ?? "";
        });
    });
  });

  $inspect(allServers, serversInFolder, otherServers);
</script>

<div class="container">
  <div class="component">
    {#each serversInFolder as server (server)}
      <ServerCard {folderName} serverUuid={server} serverName={serversName[server]} isInFolder={true} />
    {/each}
    <div class="separator"></div>
    {#each otherServers as server (server)}
      <ServerCard {folderName} serverUuid={server} serverName={serversName[server]} isInFolder={false} />
    {/each}
  </div>
</div>

<style>
  .container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .component {
    width: 75%;
    height: calc(fit-content);
    border: rgb(40, 43, 73) 2px solid;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    box-sizing: border-box;
    padding: 10px;
  }

  .separator {
    margin-top: 10px;
    margin-bottom: 10px;
    height: 1.8px;
    width: 85%;
    background-color: #1f2937;
    align-self: center;
  }
</style>
