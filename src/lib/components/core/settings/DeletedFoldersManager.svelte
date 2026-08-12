<script>
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import ServerFullDeletionConfirm from "$lib/components/bits-ui/presets/ServerFullDeletionConfirm.svelte";
  import Tile from "$lib/components/bits-ui/Tile.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import {
    getServer,
    postDeletedServer,
  } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { onMount } from "svelte";

  let deletedServers = $state([]);
  let confirmOpen = $state(false);

  async function updateDeletedServers() {
    const res = await fetch("http://localhost:8000/api/deletedServers", {
      method: "GET",
    });
    if (!res.ok) {
      console.error("Impossible to fetch deletedServers", res);
    }
    const data = await res.json();

    deletedServers = data.deletedServers;
  }

  async function restoreServer(uuid) {
    const res = await postDeletedServer(uuid, "restore");
    folderSystem.addServer(uuid);
    updateDeletedServers();
  }

  onMount(() => {
    updateDeletedServers();
  });

  $effect(() => {
    if (!confirmOpen) updateDeletedServers();
  });
</script>

<div class="component">
  {#if deletedServers.length != 0}
    {#each deletedServers as server}
      <Tile label={server.name} noHover>
        <div class="buttonsContainer">
          <IconButton
            iconPath={pathDb.undo}
            color="var(--foreground)"
            onclick={() => {
              restoreServer(server.uuid);
            }}
          />
          <IconButton
            iconPath={pathDb.garbage}
            color="var(--dangerous)"
            onclick={() => {
              uiStore.setCurrentUuid(server.uuid);
              uiStore.openDialog("serverFullDeletionConfirm");
            }}
          />
        </div>
      </Tile>
    {/each}
  {:else}
    <span class="empty">Vous n'avez aucun serveur supprimé.</span>
  {/if}
</div>

<ServerFullDeletionConfirm bind:open={confirmOpen} />

<style>
  .component {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .buttonsContainer {
    display: flex;
    flex-direction: row;
    gap: 5px;
  }

  .empty {
    font-size: 1rem;
    color: var(--foreground-alt);
  }
</style>
