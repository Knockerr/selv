<script>
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import ContextMenu from "../../ContextMenu.svelte";
  import { contextManager } from "../../contextMenuManager.svelte";
  import FolderContextMenuFolderItem from "../FolderContextMenuFolderItem.svelte";

  const { serverUuid, posx, posy } = $props();

  const contextId = $derived("folderContextMenu-" + serverUuid);

  const isOpen = $derived(contextManager.openMenu === contextId);

  const folders = $derived(folderSystem.foldersNames);
</script>

{#if isOpen}
  <ContextMenu {posx} {posy} {contextId}>
    {#each folders as folder (folder)}
      <FolderContextMenuFolderItem {serverUuid} folderName={folder} />
    {/each}
  </ContextMenu>
{/if}

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
</style>
