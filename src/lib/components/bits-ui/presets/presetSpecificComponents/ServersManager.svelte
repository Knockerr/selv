<script>
  
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { online } from "svelte/reactivity/window";
  import ServerCard from "./ServerCard.svelte";
  import Separator from "../../baseComponents/Separator.svelte";

  const { folderName } = $props();

  const allServers = $derived(folderSystem.getAllServers);

  $inspect(allServers).with(() => {
    console.info("allServers", allServers);
  });

  const serversInFolder = $derived(
    folderSystem.getFolder(folderName)?.getServers || [],
  );

  const otherServers = $derived(
    [...allServers].filter((uuid) => !serversInFolder.includes(uuid)),
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

<div class="flex flex-col gap-1">
  <span class="text-sm font-semibold">Serveurs du dossier</span>
  <div class="component">
    {#each serversInFolder as server (server)}
      <ServerCard
        {folderName}
        serverUuid={server}
        serverName={serversName[server]}
        isInFolder={true}
      />
    {/each}
    <div class="separator"></div>
    {#each otherServers as server (server)}
      <ServerCard
        {folderName}
        serverUuid={server}
        serverName={serversName[server]}
        isInFolder={false}
      />
    {/each}
  </div>
</div>

<style>
  .component {
    width: 100%;
    height: fit-content;
    height: calc(fit-content);
    border: rgba(255, 255, 255, 0.103) 2px solid;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    box-sizing: border-box;
    padding: 10px;
    background: rgba(0, 0, 0, 0.2);
  }

  .component:hover {
    background: rgba(0, 0, 0, 0.2);
  }

  .separator {
    margin-top: 5px;
    margin-bottom: 5px;
    height: 1.8px;
    width: 85%;
    background-color: rgba(255, 255, 255, 0.103);
    align-self: center;
  }
</style>
